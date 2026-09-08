from pathlib import Path
import random
from game import  Game, MAX_GUESSES, WORD_LENGTH
from history import GameHistory

word_file=Path(__file__).parent/"words.txt"
game_history_file=Path(__file__).parent/"game_history.json"

def load_words(filename):
    words=[]
    with filename.open("r") as file:
        for line in file:
            word=line.strip()
            if len(word)==WORD_LENGTH:
                words.append(word)
    return words

secret=random.choice(load_words(word_file))

def main():
    game=Game(secret,load_words(word_file))
    game_history=GameHistory(game_history_file)
    print("Welcome to Wordle!")
    print("You have 6 attempts to guess the secret 5-letter word.")
    while not game.is_over:
        guess=input("Enter your guess: ").lower()
        try:
            result=game.make_guess(guess)
            print(result)
        except ValueError as e:
            print(e)
            continue
    print(game)
    attempts=len(game.guesses)

    if game.is_won:
        print(f"Congratulations! You guessed the word '{secret}' in {attempts} attempts.")
        game_history.add_games(won=True,attempts=attempts,word=secret)
    else:
        print(f"Sorry, you did not guess the word. The secret word was '{secret}'.")
        game_history.add_games(won=False,attempts=attempts,word=secret)

    print(f"Total games played: {game_history.total_games}")
    print(f"Total wins: {game_history.total_wins}")
    print(f"Win percentage: {game_history.win_percentage:.2f}%")
    print(f"Current winning streak: {game_history.current_streak}")
    print(f"Maximum winning streak: {game_history.max_streak}")

if __name__=="__main__":
    main()