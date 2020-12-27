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


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Generate a nice key using secrets.token_urlsafe()
        SECRET_KEY=os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw'),
        # store the database in the instance folder,
        DEBUG=True,
        # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
        # Generate a good salt using: secrets.SystemRandom().getrandbits(128)

        SHARED_WORKBOOKS_PATH="shared_collections",
        SHARED_WORKBOOKS_METADATA="shared_collections_metadata.yml"

    )

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Loading configuration
    config_path=os.path.join(app.instance_path, "config.py")
    if test_config is not None:
        app.config.from_mapping(test_config)
        print("Loaded test configuration.")
    elif os.path.isfile(config_path):
        app.config.from_pyfile(config_path)
        print(f"Loaded configuration from {config_path}.")
    else:
        print(f"Configuration file at {config_path} isn't found, default configuration values are used.")

    # Check if connection string is defined
    if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
        raise Exception("SQLALCHEMY_DATABASE_URI is not set, terminating app...")

    # The db engine needs to know about the models
    from . import models
    db.init_app(app)

    # Routes for the application
    from .routes import quiz
    app.register_blueprint(quiz.bp)

    # Version information for testing the deployment system
    @app.route("/api/hello")
    def hello():
        return jsonify({"build": "2020-12-25 test"})

    init_app(app) # Register database command for flask

    return app


def get_storage_manager() -> IWordCollectionsDao:
    if "storage_mgr" not in g:
        g.storage_mgr = DbWordCollectionStorage()
    return g.storage_mgr
