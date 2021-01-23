import os
from logging.config import dictConfig

from flask import Flask, jsonify, g

from vocabulary_mgr.dataaccess import IWordCollectionsDao
from .database import db
from .database import get_db_session, init_db, init_app, DbWordCollectionStorage

dictConfig({
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
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

security = None


def create_app(test_config=None, config_filename=None):
    """Create and configure an instance of the Flask application."""


    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SHARED_WORKBOOKS_PATH="shared_collections",
        SHARED_WORKBOOKS_METADATA="shared_collections_metadata.yml",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Loading configuration
    # Test config has a priority over the configuration file
    # In order to enable easy tweaking of app configuration
    # From the command line
    if config_filename is not None:
        config_path=os.path.join(app.instance_path, config_filename)
        if os.path.isfile(config_path):
            app.config.from_pyfile(config_path)
            print(f"Loaded configuration from {config_path}.")
        else:
            raise Exception(f"Configuration file at {config_path} is missing or access isn't granted, terminating...")
    else:
        print(f"No configuration file was provided.")

    if test_config is not None:
        app.config.from_mapping(test_config)
        print("Loaded test configuration.")

    # Check if connection string is defined
    if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
        raise Exception("SQLALCHEMY_DATABASE_URI is not set, terminating app...")
        # TODO change to sys.exit or similar

    if app.config.get("SECRET_KEY") is None and (app.debug or app.testing):
        app.config["SECRET_KEY"] = os.urandom(24)
        print("Debug or test mode detected, generating secret key...")
    else:
        raise Exception("Secret key isn't found in the provided configuration for production app!")

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # The db engine needs to know about the models
    from . import models
    db.init_app(app)

    # Routes for the application
    from .routes import quiz
    app.register_blueprint(quiz.bp)

    # Version information for testing the deployment system
    @app.route("/hello")
    def hello():
        return jsonify({"build": "2020-12-25 test"})

    init_app(app) # Register database command for flask

    return app


def get_storage_manager() -> IWordCollectionsDao:
    if "storage_mgr" not in g:
        g.storage_mgr = DbWordCollectionStorage()
    return g.storage_mgr
