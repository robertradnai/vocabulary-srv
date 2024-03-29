from abc import ABC, abstractmethod


class IWordCollectionsDao(ABC):
    @abstractmethod
    def get_item(self, element_id: int):
        pass

    @abstractmethod
    def create_item(self, element_id: int, item_to_store: object, available_word_list_id: int) -> int:
        pass

    @abstractmethod
    def update_item(self, element_id: int, item_to_store: object) -> str:
        pass

