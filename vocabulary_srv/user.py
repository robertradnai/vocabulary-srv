import logging
from typing import Optional, Callable

from flask import request, current_app, g, Response, Blueprint, jsonify, session
from werkzeug.utils import redirect
import jwt
import uuid
import datetime
import functools
from requests_oauthlib import OAuth2Session
import requests

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register-guest', methods=('POST',))
def register_guest():

    guest_user = GuestUserFactory.generate()
    res = {
        "guestJwt": guest_user.get_jwt(current_app.config["SECRET_KEY"]),
        "guestJwtBody": guest_user.get_jwt_body()
    }
    current_app.logger.debug(f"JWT token created: {res['guestJwt']}")

    return jsonify(res)


@bp.route("/sign_in", methods=("GET",))
def oauth_test_sign_in():

    # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#web-application-flow
    oauth2_session = OAuth2Session(current_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"],
                                   redirect_uri=current_app.config["AWS_COGNITO_REDIRECT_URL"])
    authorization_url, state = oauth2_session.authorization_url(current_app.config["AWS_COGNITO_DOMAIN"]+"/login")
    session['oauth_state'] = state
    return redirect(authorization_url)


@bp.route('/aws_cognito_redirect')
def aws_cognito_redirect():

    oauth2_session = OAuth2Session(current_app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"],
                                   state=session['oauth_state'],
                                   redirect_uri=current_app.config["AWS_COGNITO_REDIRECT_URL"])
    token = oauth2_session.fetch_token(token_url=current_app.config["AWS_COGNITO_DOMAIN"]+"/oauth2/token",
                                       client_secret=current_app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"],
                                       authorization_response=request.url)
    access_token = token["access_token"]

    returned_content = f"""
    Redirecting after login...
    <script>
        localStorage.setItem('user_access_token', '{access_token}');
        window.location.replace("/vocabulary");
    </script> 
    """

    return Response(returned_content)


class User:
    def __init__(self, user_id: str):
        self._id: str = user_id

    @property
    def id(self) -> str:
        return self._id


class GuestUser(User):
    def __init__(self, id: str, expires: str):
        super().__init__(id)

        self.expires = expires

    def get_jwt(self, secret_key) -> str:
        return jwt.encode(self.get_jwt_body(), secret_key, algorithm='HS256')

    def get_jwt_body(self) -> dict:
        return {"guestUserId": self.id, "expires": self.expires}


class GuestUserFactory:
    @staticmethod
    def generate() -> GuestUser:
        expires_at = (datetime.datetime.now().replace(microsecond=0)
                      + datetime.timedelta(hours=2))
        return GuestUser(str(uuid.uuid1()), expires_at.isoformat())

    @staticmethod
    def from_jwt(jwt_string: str, secret_key: str) -> GuestUser:
        decoded_body = jwt.decode(jwt_string, secret_key, algorithms=['HS256'])
        return GuestUser(decoded_body["guestUserId"], decoded_body["expires"])


def get_user() -> Optional[User]:
    return g.user


def set_user(user: Optional[User]):
    g.user = user


def load_user():

    guest_token: Optional[str] = request.headers.get("Guest-Authentication-Token")
    oauth_token: Optional[str] = request.headers.get("Authorization")

    if oauth_token is not None:
        request_func = requests.request if not current_app.config["TESTING"] \
            else _mock_userinfo_response
        set_user(load_oauth_user(request_func, oauth_token))
    elif guest_token is not None and guest_token != "null":
        current_app.logger.debug(f"Validating received guest-JWT: {guest_token}")
        set_user(GuestUserFactory.from_jwt(guest_token, current_app.config["SECRET_KEY"]))
        current_app.logger.debug(f"Request received from user ID {get_user().id}")
    else:
        set_user(None)


def load_oauth_user(request_func: Callable, authorization_header: str) -> Optional[User]:

    aws_oauth_endpoint = current_app.config["AWS_COGNITO_DOMAIN"]
    resp = request_func("GET", f"{aws_oauth_endpoint}/oauth2/userInfo",
                        headers={"Authorization": f"{authorization_header}"})

    if resp.status_code == 200:
        user_id = str(resp.json()["username"])
        logging.debug(f"Got user from OAuth endpoint: {user_id}")
        return User(user_id=user_id)

    else:
        return None


def _mock_userinfo_response(request_type, url, headers):

    class MockResponse():
        status_code: int = 200
        def json(self) -> dict:
            return {"username": "test_user_1"}
    return MockResponse()


def login_required(view):
    """Make sure that the user identity object is accessible
    by the wrapped function."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # TODO create a generic user object
        #assert type(get_user()) is User

        if get_user() is None:
            return Response(status=401)
        else:
            return view(**kwargs)

    return wrapped_view


@login_required
@bp.route("/profile", methods=("GET",))
def user_profile():
    return jsonify({"username": get_user().id})
