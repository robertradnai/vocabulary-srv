import functools
import os
from typing import List, Optional

from flask import Blueprint, jsonify, request, current_app, Response
from vocabulary import wordlistquiz
from vocabulary.wordlistquiz import create_quiz_round, submit_answers
from werkzeug.exceptions import HTTPException
from wtforms import Form, StringField, BooleanField, validators

from vocabulary_srv.models import WordListMeta, PickQuestionsResponse, WordListEntry
from vocabulary_srv.wordcollections import show_shared_collections
from vocabulary_srv import get_word_lists_dao
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


def get_available_list_meta_from_id(word_list_id: int) -> WordListMeta:
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

    user_lists_query: List[WordListEntry] = get_word_lists_dao() \
        .get_word_list_entries(user_id=guest_user_id,
                               available_word_list_id=available_word_list_id)
    word_list_already_added = bool(len(user_lists_query))

    if not word_list_already_added:
        available_list_meta = get_available_list_meta_from_id(available_word_list_id)
        word_list_csv_path = os.path.join(current_app.instance_path,
                                          current_app.config["SHARED_WORKBOOKS_PATH"],
                                          available_list_meta.csv_filename)
        if not os.path.exists(word_list_csv_path):
            return Response(status=400)

        with open(word_list_csv_path) as f:
            flashcards_csv_str = f.read()

        user_list_meta = get_word_lists_dao() \
            .create_item(available_list_meta, flashcards_csv_str, guest_user_id, False)
    else:
        user_list_meta = user_lists_query[0].meta

    return jsonify(user_list_meta.to_dict())


@bp.route('/user-lists', methods=('GET',))
@inject_guest_user_id
def get_user_lists(guest_user_id: str):
    word_list_entries = get_word_lists_dao().get_word_list_entries(user_id=guest_user_id)
    return jsonify([entry.meta.to_dict() for entry in word_list_entries])
    # TODO the output is not properly tested!


@bp.route('/pick-question', methods=('POST', 'GET'))
@inject_guest_user_id
def pick_question(guest_user_id):

    user_word_list_id = int(request.args["userWordListId"])
    pick_strategy = request.args["wordPickStrategy"]

    word_list = get_word_lists_dao().get_word_list_entries(
        user_word_list_id=user_word_list_id, user_id=guest_user_id)[0].word_list

    if word_list is None:
        raise LookupError("Word list doesn't exist with the given user id and word list id")

    def generate_alternatives(word_list):
        alternatives = []
        for _, flashcard in word_list.flashcards.items():
            alternatives.append(flashcard.lang1)
        return alternatives

    quiz_entries = create_quiz_round(word_list, pick_strategy, generate_alternatives(word_list))
    learning_progress = wordlistquiz.get_learning_progress(word_list)

    return jsonify(PickQuestionsResponse(quiz_list=quiz_entries,
                                         learning_progress=learning_progress).to_dict())


@bp.route('/answer-question', methods=('POST',))
@inject_guest_user_id
def answer_question(guest_user_id):

    user_word_list_id = int(request.args["userWordListId"])
    answers = {int(k): v for k, v in request.json["answers"].items()}

    word_list = get_word_lists_dao().get_word_list_entries(
        user_word_list_id=user_word_list_id, user_id=guest_user_id)[0].word_list

    word_list_updated = submit_answers(word_list, answers)
    learning_progress = wordlistquiz.get_learning_progress(word_list_updated)

    get_word_lists_dao().update_learning_progress(
        user_word_list_id, guest_user_id, word_list_updated)

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
