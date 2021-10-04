import pytest



@pytest.mark.parametrize("answers,option,correct_answer", [("[A,B,C]", "1","A"),("[E,F,G]", "2","F"),("[C,D,F]", "3","A")])
def test_user_answer(answers, option,correct_answer):
    user_selection=answers[int(option)]
    assert user_selection == correct_answer