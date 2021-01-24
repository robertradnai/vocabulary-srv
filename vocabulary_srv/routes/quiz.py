import functools
import os
from pdb import set_trace

import jwt

from random import randint
from flask import Blueprint, jsonify, request, current_app, Response
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, BooleanField, validators

from vocabulary.dataaccess import load_wordlist_book
from vocabulary.stateless import Vocabulary
from vocabulary_mgr.wordcollectionscontroller import get_storage_element_id, show_shared_collections
from vocabulary_srv import get_storage_manager
from vocabulary_srv.database import FeedbackStorage

bp = Blueprint('vocabulary', __name__, url_prefix='/')


def guest_auth_required(view):
    """When the user uses the demo, a (guest) JWT identifies the user so that their progress
    can be saved on the server. This is the authentication based on this guest JWT"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        guest_jwt = request.headers["Guest-Authentication-Token"]
        current_app.logger.debug(f"Validating received guest-JWT: {guest_jwt}")
        decoded_body = jwt.decode(guest_jwt, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        user_id = decoded_body["guestUserId"]
        kwargs["temp_user"] = user_id

        current_app.logger.debug(f"Request received from ID {user_id}")

        return view(**kwargs)

    return wrapped_view


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


@bp.route('/register-guest', methods=('POST',))
def register_guest():

    jwt_body = {
        "guestUserId": str(randint(0, 100000)),
        "expires": "2020-10-15 12:34:00"
    }

    encoded_jwt = jwt.encode(jwt_body, current_app.config["SECRET_KEY"], algorithm='HS256')
    current_app.logger.debug(f"JWT token created: {encoded_jwt}")
    res = {
        "guestJwt": encoded_jwt,
        "guestJwtBody": jwt_body
    }
    return jsonify(res)


@bp.route("/clone-word-list", methods=('POST',))
@guest_auth_required
def clone_shared(temp_user):

    collection_name = secure_filename(request.args['wordCollection'])

    # Find the shared collection among the file
    voc = Vocabulary()
    voc.load(os.path.join(current_app.instance_path,
                          current_app.config["SHARED_WORKBOOKS_PATH"],
                          collection_name),
             load_wordlist_book)

    for word_list in voc.get_word_sheet_list():
        voc.reset_progress(word_list)

    get_storage_manager().create_item(temp_user, voc)

    # Header: jwt
    # collection (, list)
    # output: authentication result, cloning result
    return jsonify({"success": True})


@bp.route('/pick-question', methods=('POST', 'GET'))
@guest_auth_required
def pick_question(temp_user):

    collection_name = secure_filename(request.args["wordCollection"])
    list_name = request.args["wordList"]
    pick_strategy = request.args["wordPickStrategy"]

    # Getting the stored collection
    storage_id = get_storage_element_id(temp_user, collection_name, list_name)
    voc: Vocabulary = get_storage_manager().get_item(storage_id)

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
@guest_auth_required
def answer_question(temp_user):
    collection_name = secure_filename(request.args["wordCollection"])
    list_name = request.args["wordList"]
    answers = request.json["answers"]


    storage_id = get_storage_element_id(temp_user, collection_name, list_name)
    voc: Vocabulary = get_storage_manager().get_item(storage_id)
    for row_key, is_correct in answers.items():
        voc.update_progress(list_name, int(row_key), is_correct)

    # Return learning progress for the word list
    learning_progress = voc.get_progress(list_name)

    get_storage_manager().update_item(storage_id, voc)

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
