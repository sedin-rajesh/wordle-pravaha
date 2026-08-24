import random 
from pathlib import Path
from game import Game,MAX_GUESSES,WORD_LENGTH
from history import GameHistory

WORDS_FILE=Path(__file__).parent/"words.txt"

def load_words(filename: Path)->list[str]:
    words=[]
    with filename.open("r") as file:
        for line_number,line in enumerate(file,start=1):
            word=line.strip().lower()
            if not word:
                continue
            if len(word)!=WORD_LENGTH:
                raise ValueError(f"Invalid word length at line {line_number}: '{word}'")
            if not word.isalpha():
                raise ValueError(f"Invalid word at line {line_number}: '{word}'")
            words.append(word)
    if not words:
        raise ValueError("No valid words found in the file")
    return words

def print_stats(history: GameHistory)->None:
    print()
    print("Game Statistics:")
    print("----------------")
    print(f"Total games played: {history.total_games}")
    print(f"Total wins: {history.total_wins}")
    print(f"Win percentage: {history.win_percentage:.2f}%")
    print(f"Current streak: {history.current_streak}")
    print(f"Best streak: {history.best_streak}")

def main()->None:
    words=load_words(WORDS_FILE)
    secret=random.choice(words)
    history=GameHistory()
    game=Game(secret,words)

    print("Welcome to Wordle!")
    print(f"You have {MAX_GUESSES} attempts to guess the {WORD_LENGTH}-letter word.")

    while not game.is_over:
        print(game)
        guess=input("Enter your guess: ").strip().lower()
        try:
            game.make_guess(guess)
        except ValueError as error:
            print(f"Error: {error}")
            continue
    print(game)
    attempts=len(game.guesses)
    print()
    if game.is_won:
        print(f"Congratulations! You guessed the word '{secret}' in {attempts} attempts.")
        history.record_game(won=True,attempts=attempts,word=secret)
    else:
        print(f"Game over! The word was '{secret}'.")
        history.record_game(won=False,attempts=attempts,word=secret)

    print_stats(history)

if __name__=="__main__":
    main()