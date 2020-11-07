import os
from pdb import set_trace

from vocabulary.dataaccess import load_wordlist_book
from vocabulary.stateless import Vocabulary
from abc import ABC, abstractmethod
from typing import List
from yaml import load, Loader


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


def show_shared_collections(shared_collections_metadata: str):

    with open(shared_collections_metadata) as f:
        metadata_file_content = f.read()

    metadata = load(metadata_file_content, Loader=Loader)

    word_lists = []
    for collection in metadata['shared_collections_xlsx']:
        for word_list in collection["wordLists"]:
            word_lists.append(
                WordListsElement(word_collection_name=collection["wordCollection"],
                                 word_collection_display_name=collection["wordCollectionDisplayName"],
                                 word_list_name= word_list["wordList"],
                                 word_list_display_name=word_list["wordListDisplayName"])
            )

    return word_lists


def get_storage_element_id(user_id, collection_name, list_name) -> str:
    return user_id


def get_shared_collection_names() -> List[str]:
    pass

# TODO using slugs or real names?????