from random import randint
from flask import request, current_app, g, Response, Blueprint, jsonify
import jwt
import uuid
import datetime
import functools

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


def get_user() -> User:
    return g.user


def set_user(user: User):
    g.user = user


def load_user():
    if "Guest-Authentication-Token" in request.headers.keys():
        guest_jwt = request.headers["Guest-Authentication-Token"]

        current_app.logger.debug(f"Validating received guest-JWT: {guest_jwt}")
        set_user(GuestUserFactory.from_jwt(guest_jwt, current_app.config["SECRET_KEY"]))
        current_app.logger.debug(f"Request received from ID {get_user().id}")

    else:
        set_user(None)


def login_required(view):
    """When the user uses the demo, a (guest) JWT identifies the user so that their progress
    can be saved on the server. This wrapper provides the guest user ID to the routes"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if "Guest-Authentication-Token" in request.headers.keys():
            return view(**kwargs)
        else:
            return Response(status=401)

    return wrapped_view
