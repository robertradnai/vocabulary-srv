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

        voc = Vocabulary()
        voc.load("tests/testdata/testdict.xlsx", load_wordlist_book)
        show_flashcard, question, flashcard = voc.choice_quiz(list_name, pick_strategy)
        return show_flashcard, question, flashcard