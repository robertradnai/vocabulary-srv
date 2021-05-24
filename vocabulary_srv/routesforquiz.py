import functools
import os
from typing import List, Optional

from flask import Blueprint, jsonify, request, current_app, Response
from werkzeug.exceptions import HTTPException
from wtforms import Form, StringField, BooleanField, validators

from vocabulary.dataaccess import load_wordlist_book
from vocabulary.stateless import Vocabulary

from vocabulary_srv.models import WordListMeta, UserWordListMeta
from vocabulary_srv.wordcollections import get_storage_element_id, show_shared_collections
from vocabulary_srv import get_word_collection_storage
from vocabulary_srv.user import GuestUserFactory
from vocabulary_srv.database import FeedbackStorage

bp = Blueprint('vocabulary', __name__, url_prefix='/')


def inject_guest_user_id(view):
    """When the user uses the demo, a (guest) JWT identifies the user so that their progress
    can be saved on the server. This wrapper provides the guest user ID to the routes"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        guest_jwt = request.headers["Guest-Authentication-Token"]
        current_app.logger.debug(f"Validating received guest-JWT: {guest_jwt}")

        guest_user = GuestUserFactory.from_jwt(guest_jwt, current_app.config["SECRET_KEY"])
        current_app.logger.debug(f"Request received from ID {guest_user.id}")

        kwargs["guest_user_id"] = guest_user.id
        return view(**kwargs)

    return wrapped_view


@bp.route('/register-guest', methods=('POST',))
def register_guest():

    guest_user = GuestUserFactory.generate()
    res = {
        "guestJwt": guest_user.get_jwt(current_app.config["SECRET_KEY"]),
        "guestJwtBody": guest_user.get_jwt_body()
    }
    current_app.logger.debug(f"JWT token created: {res['guestJwt']}")

    return jsonify(res)


@bp.route('/shared-lists', methods=('GET',))
def get_shared_lists():

    word_list_elements: List[WordListMeta] = show_shared_collections(os.path.join(
        current_app.instance_path, current_app.config["SHARED_WORKBOOKS_METADATA"]))

    return jsonify([word_list_element.to_dict() for word_list_element
                    in word_list_elements])


def get_word_list_meta_from_id(word_list_id: int) -> WordListMeta:
    word_list_elements = show_shared_collections(os.path.join(current_app.instance_path,
                                                              current_app.config["SHARED_WORKBOOKS_METADATA"]))
    word_collection_index = [i for i, v in enumerate(word_list_elements)
                             if v.available_word_list_id == word_list_id][0]
    return word_list_elements[word_collection_index]


@bp.route("/clone-word-list", methods=('POST',))
@inject_guest_user_id
def clone_shared(guest_user_id: str):

    """
        This endpoint takes the chosen available word list ID. If the chosen list hasn't been
        added to the user's own word list, this will be performed and some basic
        reference and information about it will be returned to the client. If the chosen list has
        been added earlier, then the information of this list will be returned,
        without adding the list to the user's word lists again.
    """

    available_word_list_id = int(request.args['availableWordListId'])
    word_list_meta = get_word_list_meta_from_id(available_word_list_id)
    user_word_list_id: Optional[int] = get_word_collection_storage() \
        .get_already_existing_user_word_list_id(guest_user_id, available_word_list_id)

    if user_word_list_id is None:

        workbook_path = os.path.join(current_app.instance_path,
                                     current_app.config["SHARED_WORKBOOKS_PATH"],
                                     word_list_meta.word_collection_name)
        if not os.path.exists(workbook_path):
            return Response(status=400)

        voc = Vocabulary()
        voc.load(workbook_path, load_wordlist_book)

        for word_list in voc.get_word_sheet_list():
            voc.reset_progress(word_list)
        voc.selected_word_list_name = word_list_meta.word_list_name
        user_word_list_id: int = get_word_collection_storage() \
            .create_item(guest_user_id, voc, available_word_list_id)

    word_list_meta.user_word_list_id = user_word_list_id
    return jsonify(word_list_meta.to_dict())


@bp.route('/pick-question', methods=('POST', 'GET'))
@inject_guest_user_id
def pick_question(guest_user_id):

    user_word_list_id = int(request.args["userWordListId"])
    pick_strategy = request.args["wordPickStrategy"]

    (voc, stored_user_id) = get_word_collection_storage().get_item(user_word_list_id)
    if not stored_user_id == guest_user_id:
        raise PermissionError("User has no right to access this word list")

    """
    word_list_id = int(request.args['wordListId'])
    word_list_meta = get_word_list_meta_from_id(word_list_id)
    

    # Getting the stored collection
    storage_id = get_storage_element_id(guest_user_id, word_list_meta.word_collection_name,
                                        word_list_meta.word_list_name)
    voc: Vocabulary = get_word_collection_storage().get_item(storage_id)
    """

    from .models import QuizEntry, Flashcard, MultipleChoiceQuiz
    from vocabulary_srv.models import PickQuestionsResponse

    # Fetching a question and the learning progress
    quiz_list = voc.choice_quiz(voc.selected_word_list_name, pick_strategy)

    quiz_entries = []

    for quiz_entry_old in quiz_list:

        if quiz_entry_old.question is not None:
            choice_quiz = MultipleChoiceQuiz(
                row_key=quiz_entry_old.question.row_key,
                instruction_header=voc.word_collection.word_lists[voc.selected_word_list_name].lang2,
                instruction_content=quiz_entry_old.flashcard.lang2,
                options_header="{} - how would you translate?".format(
                    voc.word_collection.word_lists[voc.selected_word_list_name].lang1),
                options=quiz_entry_old.question.options,
                correct_answer_indices=[2])
            # TODO assign real value to correct_answer_indices
        else:
            choice_quiz = None

        quiz_entry = QuizEntry(
            question=choice_quiz,
            flashcard=Flashcard(lang1=quiz_entry_old.flashcard.lang1,
                                lang2=quiz_entry_old.flashcard.lang2,
                                remarks=quiz_entry_old.flashcard.remarks,
                                lang1_header=voc.word_collection.word_lists[voc.selected_word_list_name].lang1,
                                lang2_header=voc.word_collection.word_lists[voc.selected_word_list_name].lang2,
                                remarks_header="Remarks"))

        quiz_entries.append(quiz_entry.__dict__)

    learning_progress = voc.get_progress(voc.selected_word_list_name)
    return jsonify(PickQuestionsResponse(quiz_list=quiz_entries,
                                         learning_progress=learning_progress).to_dict())


@bp.route('/answer-question', methods=('POST',))
@inject_guest_user_id
def answer_question(guest_user_id):

    user_word_list_id = int(request.args["userWordListId"])
    answers = request.json["answers"]

    """
    word_list_id = int(request.args['wordListId'])
    word_list_meta = get_word_list_meta_from_id(word_list_id)
    

    stored_collection_id = get_storage_element_id(guest_user_id,
                                                  word_list_meta.word_collection_name,
                                                  word_list_meta.word_list_name)
    """

    (voc, stored_user_id) = get_word_collection_storage().get_item(user_word_list_id)
    if not stored_user_id == guest_user_id:
        raise PermissionError("User has no right to access this word list")

    for row_key, is_correct in answers.items():
        voc.update_progress(voc.selected_word_list_name, int(row_key), is_correct)

    # Return learning progress for the word list
    learning_progress = voc.get_progress(voc.selected_word_list_name)

    get_word_collection_storage().update_item(user_word_list_id, voc)

    res = {"learningProgress": learning_progress}

    return jsonify(res)


@bp.route("/feedback-or-subscribe", methods=('POST',))
def feedback_subscribe():
    form = FeedbackForm(request.form)
    if not form.validate():
        return Response(status=400)
    else:
        FeedbackStorage.insert(name=form.name.data,
                               email=form.email.data,
                               is_subscribe=form.is_subscribe.data,
                               subject=form.subject.data,
                               message=form.message.data)
        return Response(status=200)


class FeedbackForm(Form):
    name = StringField('name', [validators.Length(min=1, max=120)])
    email = StringField('email', [validators.email()])
    is_subscribe = BooleanField('is_subscribe')
    subject = StringField('subject', [validators.Length(min=0, max=1200)])
    message = StringField('message', [validators.Length(min=0, max=1200)])


@bp.route('/test/raise', methods=('GET',))
def throw_error():
    raise RuntimeError("This is an intentionally raised test exception.")


@bp.errorhandler(Exception)
def handle_exception(e: Exception):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    current_app.logger.exception(f"Error while handling request {request.url}")
    # Handle non-HTTP errors
    return Response(status=500)
