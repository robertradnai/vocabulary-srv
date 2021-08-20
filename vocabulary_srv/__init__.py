import os
from http.client import HTTPException
from logging.config import dictConfig as loggingDictConfig

from flask import Flask, jsonify, g, request, Response

from vocabulary_srv.dataaccess import IWordCollectionsDao
from .database import db
from .database import init_db, init_app, DbWordListStorage

loggingDictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': "INFO",
        'handlers': ['wsgi']
    }
})


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True, instance_path=os.getcwd())

    if app.config.get("DEBUG"):
        app.logger.setLevel("DEBUG")

    app.config.from_mapping(
        SHARED_WORKBOOKS_PATH="shared_collections",
        SHARED_WORKBOOKS_METADATA="shared_collections_metadata.yml",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile(os.path.join(app.instance_path, "config.py"))
    else:
        app.config.from_mapping(test_config)
        app.logger.debug("Loaded test configuration.")

    # Check if the necessary files are present
    list_metadata_path = os.path.join(app.instance_path, app.config.get("SHARED_WORKBOOKS_METADATA"))
    if not os.path.isfile(list_metadata_path):
        raise FileNotFoundError(f"Word list metadata wasn't found at {list_metadata_path}")

    list_folder_path = os.path.join(app.instance_path, app.config.get("SHARED_WORKBOOKS_PATH"))
    if not os.path.isdir(list_folder_path):
        raise FileNotFoundError(f"Word lists folder wasn't found at {list_folder_path}")

    # Check if connection string is defined
    if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
        exc_msg = "SQLALCHEMY_DATABASE_URI is not set, terminating app..."
        app.logger.debug(exc_msg)  # Gunicorn doesn't print exception message, so I print it here additionally
        raise ValueError(exc_msg)

    if app.config.get("SECRET_KEY") is None and app.testing:
        app.config["SECRET_KEY"] = os.urandom(24)
        app.logger.debug("Debug or test mode detected, generating secret key...")

    if app.config.get("SECRET_KEY") is None and not (app.debug or app.testing):
        exc_msg = "Secret key isn't found in the provided configuration for production app!"
        app.logger.debug(exc_msg)
        raise ValueError(exc_msg)

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # The db engine needs to know about the models
    from . import dbmodels
    db.init_app(app)

    # Routes for the application
    from . import routesforquiz
    app.register_blueprint(routesforquiz.bp)

    from . import user
    app.register_blueprint(user.bp)

    # Version information for testing the deployment system
    @app.route("/hello")
    def hello():
        return jsonify({"build": "2020-12-25 test"})

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            return e

        app.logger.exception(f"Error while handling request {request.url}")

        # Handle non-HTTP errors
        return Response(status=500)

    init_app(app)  # Register database command for flask

    return app


def get_word_lists_dao():
    if "word_lists_dao" not in g:
        g.word_lists_dao = DbWordListStorage()
    return g.word_lists_dao
