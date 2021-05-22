from vocabulary_srv import create_app
from vocabulary_srv.database import FeedbackStorage
from flask.wrappers import Response

TEST_LIST_ID = 1
TEST_LIST_DISPLAY_NAME = "Short list for testing"
TEST_LIST_LANG1 = "Finnish"
TEST_LIST_LANG2 = "English"


def test_config():
    assert create_app({'TESTING': True, "SQLALCHEMY_DATABASE_URI": "dummy_string"}).testing


def test_demo_quiz(client):
    r_list: Response = client.get('/shared-lists')

    assert TEST_LIST_DISPLAY_NAME == r_list.json[0]["wordListDisplayName"]
    assert TEST_LIST_ID == r_list.json[0]["wordListId"]
    assert TEST_LIST_LANG1 == r_list.json[0]["lang1"]
    assert TEST_LIST_LANG2 == r_list.json[0]["lang2"]

    r_register: Response = client.post('/register-guest')
    assert 'guestJwt' in r_register.json

    guest_jwt = r_register.json['guestJwt']

    # https://werkzeug.palletsprojects.com/en/1.0.x/test/#werkzeug.test.EnvironBuilder
    headers = {'Guest-Authentication-Token': guest_jwt}

    r_clone_word_list = client.post(f'/clone-word-list?wordListId={TEST_LIST_ID}', headers=headers)
    assert r_clone_word_list.json['success']

    r_quiz = client.post(f'/pick-question?wordListId={TEST_LIST_ID}'
                         f'&wordPickStrategy=dummy', headers=headers)

    assert "quizList" in r_quiz.json
    quiz_list = r_quiz.json['quizList']
    for quiz in quiz_list:
        assert 'question' in quiz
        assert 'flashcard' in quiz
        assert "lang1Header" in quiz["flashcard"]
        assert "lang2Header" in quiz["flashcard"]

    answers = {2: True, 3: True, 4: True}

    # Submit batch answer
    r_submit_answer = client.post(f'/answer-question?wordListId={TEST_LIST_ID}'
                                  f'&wordPickStrategy=dummy',
                                  headers=headers, json={"answers": answers})

    # Verify if a few correct answers had an effect on the learning progress
    learning_progress = r_submit_answer.json['learningProgress']
    assert learning_progress > 0


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
