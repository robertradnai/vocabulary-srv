import os
import tempfile

import pytest
from vocabulary_srv import create_app

# with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
#    _data_sql = f.read().decode('utf8')

TEST_CONFIG: dict = {
    'TESTING': True,
    'SHARED_WORKBOOKS_PATH': "../tests/testdata/shared_collections"
    # 'DATABASE': db_path,
}

@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app()

    with app.app_context():
        pass
        # init_db()
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
