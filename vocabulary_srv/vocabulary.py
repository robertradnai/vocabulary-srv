import functools
from random import randint

import jwt
from flask import Blueprint, jsonify, request, current_app, Response
from vocabulary.models import Question
from vocabulary.stateless import Vocabulary
from vocabulary.dataaccess import load_wordlist_book
from pdb import set_trace

from werkzeug.utils import secure_filename

from vocabulary_mgr.wordcollectionscontroller import get_storage_element_id, show_shared_collections
from . import get_vocabulary_manager, get_storage_manager
import os

bp = Blueprint('vocabulary', __name__, url_prefix='/api/vocabulary')


def guest_auth_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        guest_jwt = request.headers["Guest-Authentication-Token"]
        print(f"Validating received guest-JWT: {guest_jwt}")
        decoded_body = jwt.decode(guest_jwt, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        user_id = decoded_body["guestUserId"]
        kwargs["temp_user"] = user_id

        print(f"Request received from ID {user_id}")

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
    print(f"JWT token created: {encoded_jwt.decode()}")
    res = {
        "guestJwt": encoded_jwt.decode(),
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

        question_options = quiz.question.options if quiz.question is not None else None

        res = {
            "question": {
                "options": quiz.question.options if quiz.question is not None else None,
                "rowKey": quiz.question.row_key if quiz.question is not None else None,
                "text": quiz.question.text if quiz.question is not None else None
            },
            "directives": quiz.directives,
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
