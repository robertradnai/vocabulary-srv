from typing import List
import yaml

from .models import WordListMeta


class WordListsElement:
    def __init__(self, word_collection_name: str, word_list_name: str,
                 word_collection_display_name: str, word_list_display_name: str,
                 word_list_id: int):
        self.word_collection_name = word_collection_name
        self.word_list_name = word_list_name
        self.word_collection_display_name = word_collection_display_name
        self.word_list_display_name = word_list_display_name
        self.word_list_id = word_list_id


def show_shared_collections(shared_collections_metadata: str) -> List[WordListMeta]:

    with open(shared_collections_metadata) as f:
        metadata_file_content = f.read()

    metadata = yaml.load(metadata_file_content, Loader=yaml.Loader)

    word_lists = []
    for metadata_entry in metadata:
        word_lists.append(
            WordListMeta(
                available_word_list_id=metadata_entry["available_word_list_id"],
                word_list_display_name=metadata_entry["word_list_display_name"],
                description=metadata_entry["description"],
                lang1=metadata_entry["lang1"],
                lang2=metadata_entry["lang2"],
                is_added_to_user_word_lists=False,
                user_word_list_id=None,
                csv_filename=metadata_entry["csv_filename"]
            )
        )
    return word_lists


def get_storage_element_id(user_id, collection_name, list_name) -> str:
    return user_id

