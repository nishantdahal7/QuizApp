import pytest


@pytest.fixture
def insert_question():
    question = "What is the Correct Answer?"
    answer = "None"
    options = ["a", "b", "c"]
    return [question, answer, options]


def test_insert_question(insert_question):
    question = "What is the Correct Answer?"
    assert insert_question[0] == question


def test_insert_question_options(insert_question):
    options = insert_question[2]
    new_options = ["a", "b", "c"]
    for index in range(0, len(insert_question)):
        if options[index] != new_options[index]:
            assert False
    assert True

def test_insert_question_answer(insert_question):
    answer=insert_question[1]
    new_answer="None"
    assert answer==new_answer
