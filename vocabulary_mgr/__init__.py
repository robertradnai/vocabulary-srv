from vocabulary.stateless import Vocabulary
from vocabulary.dataaccess import load_wordlist_book

class VocabularyMgr():
    def __init__(self, storage_path):
        self._storage_path = storage_path

    def get_shared_list_names(self):
        pass

    def authenticate_guest(self):
        pass

    def clone_shared(self):
        pass

    def pick_question(self, collection_name, list_name, pick_strategy):
        pass