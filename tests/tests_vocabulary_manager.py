import pytest

from vocabulary_mgr.shelvestorage import StorageManager
from tests.utils import reset_test_env


def test_object_store():
    reset_test_env()

    storage_path = "testdata_temp/test_storage"
    sm = StorageManager(storage_path)

    stored_obj = {"a": "AA", "b": "BB"}

    id = "first"
    sm.put_item(id, stored_obj)

    assert sm.get_item(id) == stored_obj

    sm.delete_item(id)

    with pytest.raises(KeyError):
        sm.get_item(id)
