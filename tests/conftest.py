import pytest

from vocabulary_srv import create_app, init_db

TEST_CONFIG: dict = {
    'TESTING': True,
    'SHARED_WORKBOOKS_PATH': "../tests/testdata/shared_collections",
    "SHARED_WORKBOOKS_METADATA": "../tests/testdata/shared_collections_metadata.yml",
    "SQLALCHEMY_DATABASE_URI": "sqlite://",
    "AWS_COGNITO_DOMAIN": 'https://vocabulary-test-local.auth.eu-central-1.amazoncognito.com'
}


@pytest.fixture
def app():
    app = create_app(TEST_CONFIG)
    with app.app_context():
        init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
