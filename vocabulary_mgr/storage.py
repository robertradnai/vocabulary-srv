from shelve import DbfilenameShelf, open
from time import sleep
from traceback import format_exception


class StorageManager:
    def __init__(self, storage_path):
        self._storage_path = storage_path

    def get_item(self, element_id: str):
        attempts = 1
        while attempts <= 5:
            try:
                with open(self._storage_path) as storage:
                    return storage[element_id]
            except Exception as e:
                print(f"WARNING - Exception occurred during accessing the shelf object, attempt {attempts}. {format_exception(e)}")
                sleep(1)
        raise Exception("Shelve object couldn't be accessed after several attempts in get_item!")


    def put_item(self, element_id: str, item_to_store: object):
        with open(self._storage_path) as storage:
            storage[element_id] = item_to_store

    def delete_item(self, element_id: str):
        with open(self._storage_path) as storage:
            del storage[element_id]


