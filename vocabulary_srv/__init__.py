import os
from logging.config import dictConfig

from flask import Flask, jsonify, g

from vocabulary_srv.dataaccess import IWordCollectionsDao
from .database import db
from .database import init_db, init_app, DbWordListStorage

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
            app.logger.debug(f"Loaded configuration from {config_path}.")
        else:
            raise FileNotFoundError(f"Configuration file at {config_path} is missing or access isn't granted, terminating...")
    else:
        app.logger.debug(f"No configuration file was provided.")

    if test_config is not None:
        app.config.from_mapping(test_config)
        app.logger.debug("Loaded test configuration.")

    # Check if connection string is defined
    if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
        exc_msg = "SQLALCHEMY_DATABASE_URI is not set, terminating app..."
        app.logger.debug(exc_msg) # Gunicorn doesn't print exception message, so I print it here additionally
        raise ValueError(exc_msg)

    if app.config.get("SECRET_KEY") is None and (app.testing):
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

    init_app(app) # Register database command for flask

    return app


def get_word_lists_dao():
    if "word_lists_dao" not in g:
        g.word_lists_dao = DbWordListStorage()
    return g.word_lists_dao
