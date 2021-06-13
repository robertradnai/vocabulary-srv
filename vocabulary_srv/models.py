from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from datetime import datetime

from typing import List, Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Flashcard:
    lang1: str
    lang2: str
    remarks: str
    lang1_header: str
    lang2_header: str
    remarks_header: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MultipleChoiceQuiz:
    row_key: int
    instruction_header: str
    instruction_content: str
    options_header: str
    options: List[str]
    correct_answer_indices: List[int]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QuizEntry:
    question: MultipleChoiceQuiz
    flashcard: Flashcard


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PickQuestionsResponse:
    quiz_list: List[QuizEntry]
    learning_progress: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WordListMeta:
    available_word_list_id: int
    word_list_display_name: str
    description: str
    lang1: str
    lang2: str
    is_added_to_user_word_lists: bool
    user_word_list_id: Optional[int]
    word_collection_name: str
    word_list_name: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UserWordListMeta(WordListMeta):
    progress: float
    created_at: datetime
    last_opened_at: datetime
