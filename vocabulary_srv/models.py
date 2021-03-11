from dataclasses import dataclass

from typing import List


@dataclass
class Flashcard:
    lang1: str
    lang2: str
    remarks: str
    lang1_header: str
    lang2_header: str
    remarks_header: str


@dataclass
class MultipleChoiceQuiz:
    row_key: int
    instruction_header: str
    instruction_content: str
    options_header: str
    options: List[str]
    correct_answer_indices: List[int]


@dataclass
class QuizEntry:
    question: MultipleChoiceQuiz
    flashcard: Flashcard


@dataclass
class PickQuestionsResponse:
    quiz_list: List[QuizEntry]
