from vocabulary_srv import create_app
from pdb import set_trace
from flask.wrappers import Response

TEST_COLLECTION_NAME = "en_fin_demo.xlsx"
TEST_LIST_NAME = "basics1"


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_demo_quiz(client):
    r_list: Response = client.get('/api/vocabulary/shared-lists')
    set_trace()


    r_register: Response = client.post('/api/vocabulary/register-guest')
    assert 'guestJwt' in r_register.json

    guest_jwt = r_register.json['guestJwt']

    # https://werkzeug.palletsprojects.com/en/1.0.x/test/#werkzeug.test.EnvironBuilder
    headers = {'Guest-Authentication-Token': guest_jwt}

    r_clone_word_list = client.post('/api/vocabulary/clone-word-list?wordCollection=testdict.xlsx', headers=headers)
    assert r_clone_word_list.json['success']

    r_quiz = client.post('/api/vocabulary/pick-question?wordCollection=testdict'
                         '&wordList=shorttest&wordPickStrategy=dummy', headers=headers)

    assert "quizList" in r_quiz.json
    quiz_list = r_quiz.json['quizList']
    for quiz in quiz_list:
        assert 'directives' in quiz
        assert 'question' in quiz
        assert 'flashcard' in quiz

    answers = {2: True, 3: True, 4: True}

    # Submit batch answer
    r_submit_answer = client.post('/api/vocabulary/answer-question?wordCollection=testdict'
                                  '&wordList=shorttest&wordPickStrategy=dummy',
                                  headers=headers, json={"answers": answers})

    # Verify if a few correct answers had an effect on the learning progress
    learning_progress = r_submit_answer.json['learningProgress']
    assert learning_progress > 0
