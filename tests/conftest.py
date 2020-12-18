import pytest

from vocabulary_srv import create_app, init_db

TEST_CONFIG: dict = {
    'TESTING': True,
    'SHARED_WORKBOOKS_PATH': "../tests/testdata/shared_collections",
    "SHARED_WORKBOOKS_METADATA": "../tests/testdata/shared_collections_metadata.yml",
    "COLLECTION_STORAGE_PATH": "../tests/testdata/user_collections",
    "SQLALCHEMY_DATABASE_URI": "postgres://vocabulary_test:vocabulary_test@localhost/vocabulary_test"
}


@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app(TEST_CONFIG)

    with app.app_context():
        init_db()
        # get_db().executescript(_data_sql)
    pass

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
