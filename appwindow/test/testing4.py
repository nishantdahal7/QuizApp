import pytest


@pytest.fixture
def current_high():
    return 100

def get_score(score,time):
    return score*time/100+10

def testing_highscore(current_high):
    current_score = 27
    assert (get_score(current_score,5) < current_high) is True == True