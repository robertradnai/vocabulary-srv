import os

from vocabulary.dataaccess import load_wordlist_book
from vocabulary.stateless import Vocabulary
from abc import ABC, abstractmethod
from typing import List
from flask import current_app


class IStorageManager(ABC):
    @abstractmethod
    def get_item(self, element_id: str):
        pass

    @abstractmethod
    def put_item(self, element_id: str, item_to_store: object):
        pass

    @abstractmethod
    def delete_item(self, element_id: str):
        pass



class WordListsElement:
    def __init__(self, word_collection_name: str, word_list_name: str,
                 word_collection_display_name: str, word_list_display_name: str):
        self.word_collection_name = word_collection_name
        self.word_list_name = word_list_name
        self.word_collection_display_name = word_collection_display_name
        self.word_list_display_name = word_list_display_name


def show_shared_collections(shared_collections_folder: str, shared_collections_metadata_folder: str):
    voc = Vocabulary()
    voc.load(os.path.join(shared_collections_folder, "testdict.xlsx"), load_wordlist_book)
    for word_list in voc.get_word_sheet_list():
        voc.reset_progress(word_list)

    word_lists = [WordListsElement("testdict.xlsx",
                                   element,
                                   "Test collection",
                                   element) for element in voc.get_word_sheet_list()]

    return word_lists


def get_storage_element_id(user_id, collection_name, list_name) -> str:
    return user_id


def get_shared_collection_names() -> List[str]:
    pass

# TODO using slugs or real names?????