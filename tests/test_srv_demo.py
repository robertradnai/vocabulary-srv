from vocabulary_srv import create_app
from vocabulary_srv.database import FeedbackStorage
from flask.wrappers import Response
import jwt




def test_config():
    assert create_app({'TESTING': True, "SQLALCHEMY_DATABASE_URI": "dummy_string"}).testing


def run_test_cycle(client, chosen_available_word_list_id):

    r_list: Response = client.get('/shared-lists')

    r_register: Response = client.post('/register-guest')
    guest_jwt = r_register.json["guestJwt"]

    r_clone_word_list = client.post(
        f'/clone-word-list?availableWordListId={chosen_available_word_list_id}',
        headers={'Guest-Authentication-Token': guest_jwt})
    user_word_list_id = r_clone_word_list.json["userWordListId"]
    assert type(user_word_list_id) is int

    r_quiz = client.post(f'/pick-question?userWordListId={user_word_list_id}'
                         f'&wordPickStrategy=dummy',
                         headers={'Guest-Authentication-Token': guest_jwt})

    quiz_list = r_quiz.json['quizList']
    for quiz in quiz_list:
        assert 'question' in quiz
        assert 'flashcard' in quiz
        if quiz["flashcard"] is not None:
            assert "lang1Header" in quiz["flashcard"]
            assert "lang2Header" in quiz["flashcard"]

    answers = {2: True, 3: True, 4: True}

    # Submit batch answer
    r_submit_answer = client.post(f'/answer-question?userWordListId={user_word_list_id}'
                                  f'&wordPickStrategy=dummy',
                                  headers={'Guest-Authentication-Token': guest_jwt},
                                  json={"answers": answers})

    # Verify if a few correct answers had an effect on the learning progress
    learning_progress = r_submit_answer.json['learningProgress']
    assert learning_progress > 0

    test_data = {
        "r_shared_lists": r_list,
        "r_register": r_register,
        "r_clone_word_list": r_clone_word_list,
        "r_quiz": r_quiz,
        "r_submit_answer": r_submit_answer
    }
    return test_data


def test_demo_quiz(client):

    chosen_available_word_list_id = 1
    test_data = run_test_cycle(client, chosen_available_word_list_id)

    test_available_list_id = 1
    test_list_display_name = "Short list for testing"
    test_list_lang1 = "Finnish"
    test_list_lang2 = "English"

    assert test_list_display_name == test_data["r_shared_lists"].json[0]["wordListDisplayName"]
    assert test_available_list_id == test_data["r_shared_lists"].json[0]["availableWordListId"]
    assert test_list_lang1 == test_data["r_shared_lists"].json[0]["lang1"]
    assert test_list_lang2 == test_data["r_shared_lists"].json[0]["lang2"]

    # Verify that the sessions and resources
    # of two users aren't mixed up in the app
    test_data_2 = run_test_cycle(client, 1)

    assert not test_data["r_clone_word_list"].json["userWordListId"] \
        == test_data_2["r_clone_word_list"].json["userWordListId"]

    def get_user_id(test_data):
        return jwt.decode(test_data["r_register"].json["guestJwt"],
                          options={"verify_signature": False})
    assert not get_user_id(test_data) == get_user_id(test_data_2)


def test_raise_error(client):
    client.get('/test/raise')
    # TODO add assertion


def test_feedback_subscribe(app):
    # See https://werkzeug.palletsprojects.com/en/1.0.x/test/#werkzeug.test.EnvironBuilder
    # for parameters

    with app.app_context():
        assert FeedbackStorage.get_count() == 0  # No entries in the table

    form_data = {"name": "Aladar", "email": "aladar@example.com", "is_subscribe": True,
                 "subject": "some subject", "message": "some message"}
    r_feedback: Response = app.test_client().post("/feedback-or-subscribe", data=form_data)

    form_data_bad_email = {"name": "Aladar", "email": "invalid email", "is_subscribe": True,
                           "subject": "some subject", "message": "some message"}

    r_bad_email: Response = app.test_client().post("/feedback-or-subscribe", data=form_data_bad_email)

    assert r_feedback.status_code == 200
    assert r_bad_email.status_code == 400

    with app.app_context():
        assert FeedbackStorage.get_count() == 1  # Exactly one entry in the table
