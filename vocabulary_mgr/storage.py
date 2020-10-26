from shelve import DbfilenameShelf, open


class StorageManager:
    def __init__(self, storage_path):
        self._storage_path = storage_path

    def get_item(self, element_id: str):
        with open(self._storage_path) as storage:
            return storage[element_id]

    def put_item(self, element_id: str, item_to_store: object):
        with open(self._storage_path) as storage:
            storage[element_id] = item_to_store

    def delete_item(self, element_id: str):
        with open(self._storage_path) as storage:
            del storage[element_id]


