import functools
import os

from flask import Blueprint, jsonify, request, current_app, Response
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, BooleanField, validators

from vocabulary.dataaccess import load_wordlist_book
from vocabulary.stateless import Vocabulary
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

    word_list_elements = show_shared_collections(os.path.join(current_app.instance_path,
                                                              current_app.config["SHARED_WORKBOOKS_METADATA"]))

    res = [
        {"wordCollectionDisplayName": word_list_element.word_collection_display_name,
         "wordListDisplayName": word_list_element.word_list_display_name,
         "wordCollection": word_list_element.word_collection_name,
         "wordList": word_list_element.word_list_name}
        for word_list_element in word_list_elements]

    return jsonify(res)


@bp.route("/clone-word-list", methods=('POST',))
@inject_guest_user_id
def clone_shared(guest_user_id: str):

    """
        Validate the path of the word collection, then load it into the DB.
    """

    collection_name = secure_filename(request.args['wordCollection'])
    workbook_path = os.path.join(current_app.instance_path,
                                 current_app.config["SHARED_WORKBOOKS_PATH"],
                                 collection_name)
    if not os.path.exists(workbook_path):
        return Response(status=400)

    voc = Vocabulary()
    voc.load(workbook_path, load_wordlist_book)

    for word_list in voc.get_word_sheet_list():
        voc.reset_progress(word_list)

    get_word_collection_storage().create_item(guest_user_id, voc)

    return jsonify({"success": True})


@bp.route('/pick-question', methods=('POST', 'GET'))
@inject_guest_user_id
def pick_question(guest_user_id):

    collection_name = secure_filename(request.args["wordCollection"])
    list_name = request.args["wordList"]
    pick_strategy = request.args["wordPickStrategy"]

    # Getting the stored collection
    storage_id = get_storage_element_id(guest_user_id, collection_name, list_name)
    voc: Vocabulary = get_word_collection_storage().get_item(storage_id)

    # Fetching a question and the learning progress

    quiz_list = voc.choice_quiz(list_name, pick_strategy)
    res_dict_list = []

    for quiz in quiz_list:
        extended_directives: dict = {}
        extended_directives.update(quiz.directives)
        extended_directives.update({"lang1_name": voc.word_collection.word_lists[list_name].lang1,
                                    "lang2_name": voc.word_collection.word_lists[list_name].lang2})

        res = {
            "question": {
                "options": quiz.question.options if quiz.question is not None else None,
                "rowKey": quiz.question.row_key if quiz.question is not None else None,
                "text": quiz.question.text if quiz.question is not None else None
            },
            "directives": extended_directives,
            "flashcard": {
                "lang1": quiz.flashcard.lang1,
                "lang2": quiz.flashcard.lang2,
                "remarks": quiz.flashcard.remarks
            },
        }
        res_dict_list.append(res)

    return jsonify({"quizList": res_dict_list})


@bp.route('/answer-question', methods=('POST',))
@inject_guest_user_id
def answer_question(guest_user_id):
    collection_name = secure_filename(request.args["wordCollection"])
    list_name = request.args["wordList"]
    answers = request.json["answers"]


    stored_collection_id = get_storage_element_id(guest_user_id, collection_name, list_name)
    voc: Vocabulary = get_word_collection_storage().get_item(stored_collection_id)
    for row_key, is_correct in answers.items():
        voc.update_progress(list_name, int(row_key), is_correct)

    # Return learning progress for the word list
    learning_progress = voc.get_progress(list_name)

    get_word_collection_storage().update_item(stored_collection_id, voc)

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
    raise Exception("This is an intentionally raised test exception.")


@bp.errorhandler(Exception)
def handle_exception(e: Exception):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    current_app.logger.exception(f"Error while handling request {request.url}")
    # Handle non-HTTP errors
    return Response(status=500)
