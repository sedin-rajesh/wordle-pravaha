import pytest

from game import (Game,ABSENT,CORRECT,PRESENT,evaluate_guess)

WORD_LIST=["apple","grape","peach","berry","mango"]

def test_evaluate_guess_fully_correct()->None:
    result=evaluate_guess("apple","apple")
    assert result.result==[CORRECT]*5

def test_evaluate_guess_mixed_results()->None:
    result=evaluate_guess("apple","grape")
    assert result.result==[ABSENT,ABSENT,PRESENT,PRESENT,CORRECT]

def test_evaluate_guess_duplicate_letters()->None:
    result=evaluate_guess("apple","peach")
    assert result.result==[PRESENT,PRESENT,PRESENT,ABSENT,ABSENT]

def test_make_rejects_word_not_in_word_list()->None:
    game=Game("apple",WORD_LIST)
    with pytest.raises(ValueError):
        game.make_guess("zzzzz")

def test_game_is_won_after_correct_guess()->None:
    game=Game("apple",WORD_LIST)
    game.make_guess("apple")
    assert game.is_won
    assert game.is_over

def test_game_is_over_after_max_attempts()->None:
    game=Game("apple",WORD_LIST)
    for _ in range(6):
        game.make_guess("grape")
    assert game.is_over
    assert not game.is_won