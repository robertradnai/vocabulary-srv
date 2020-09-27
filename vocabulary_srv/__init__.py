import os

import flask_wtf
from flask import Flask, render_template_string
from flask_security import auth_required, SQLAlchemySessionUserDatastore,\
    Security, hash_password, current_user
from .database import get_db_session, init_db, init_app
from .models import User, Role

security = None

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Generate a nice key using secrets.token_urlsafe()
        SECRET_KEY=os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw'),
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        DEBUG=True,
        # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
        # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
        SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634'),

        # no forms so no concept of flashing
        SECURITY_FLASH_MESSAGES = False,

        # Need to be able to route backend flask API calls. Use 'accounts'
        # to be the Flask-Security endpoints.
        SECURITY_URL_PREFIX = '/api/accounts',

        # Turn on all the great Flask-Security features
        SECURITY_RECOVERABLE = True,
        SECURITY_TRACKABLE = True,
        SECURITY_CHANGEABLE = True,
        SECURITY_CONFIRMABLE = False,
        SECURITY_REGISTERABLE = True, # TODO disable this before public test!
        SECURITY_UNIFIED_SIGNIN = False,

        # These need to be defined to handle redirects
        # As defined in the API documentation - they will receive the relevant context
        SECURITY_POST_CONFIRM_VIEW = "/confirmed",
        SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error",
        SECURITY_RESET_VIEW = "/reset-password",
        SECURITY_RESET_ERROR_VIEW = "/reset-password",
        SECURITY_REDIRECT_BEHAVIOR = "spa",

        # CSRF protection is critical for all session-based browser UIs

        # enforce CSRF protection for session / browser - but allow token-based
        # API calls to go through
        SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"],
        SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True,

        # Send Cookie with csrf-token. This is the default for Axios and Angular.
        SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"},
        WTF_CSRF_CHECK_DEFAULT = False,
        WTF_CSRF_TIME_LIMIT = None,

        SECURITY_REDIRECT_HOST = 'localhost:8080'

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    with app.app_context():
        # Setup Flask-Security
        # In your app
        # Enable CSRF on all api endpoints.
        flask_wtf.CSRFProtect(app)
        user_datastore = SQLAlchemySessionUserDatastore(get_db_session(), User, Role)
        global security
        security = Security(app, user_datastore)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Create a user to test with
    @app.before_first_request
    def create_user():
        init_db()
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
        get_db_session().commit()

    # Views
    @app.route("/")
    @auth_required()
    def home():
        return render_template_string('Hello {{email}} !', email=current_user.email)

    init_app(app)

    # apply the blueprints to the app
    #from vocabulary_srv import auth, blog

    #app.register_blueprint(auth.bp)
    #app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app