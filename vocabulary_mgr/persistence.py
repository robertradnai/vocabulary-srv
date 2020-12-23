from abc import ABC, abstractmethod


class AbsStorageManager(ABC):
    @abstractmethod
    def get_item(self, element_id: str) -> object:
        pass

    @abstractmethod
    def put_item(self, element_id: str, item_to_store: object) -> str:
        pass