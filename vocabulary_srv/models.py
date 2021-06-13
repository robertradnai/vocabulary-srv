from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from typing import List


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
