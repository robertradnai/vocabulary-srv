from abc import ABC, abstractmethod


class IWordCollectionsDao(ABC):
    @abstractmethod
    def get_item(self, element_id: str):
        pass

    @abstractmethod
    def create_item(self, element_id: str, item_to_store: object) -> str:
        pass

    @abstractmethod
    def update_item(self, element_id: str, item_to_store: object) -> str:
        pass

