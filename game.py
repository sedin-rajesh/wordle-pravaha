from collections import Counter

WORD_LENGTH = 5
MAX_GUESSES = 6
CORRECT = "correct"
PRESENT = "present"
ABSENT = "absent"

class GuessResult:
    def __init__(self, guess: str, result: list[str]) -> None:
        self.guess = guess
        self.result = result

    def __str__(self) -> str:
        letters = "  ".join(self.guess.upper())
        symbols = {
            CORRECT: "✓",
            PRESENT: "~",
            ABSENT: "✗",
        }
        results = "  ".join(
            symbols[item] for item in self.result
        )
        return f"{letters}\n{results}"

def evaluate_guess(secret: str, guess: str) -> GuessResult:
    secret = secret.lower()
    guess = guess.lower()
    if len(secret) != WORD_LENGTH:
        raise ValueError(
            f"Secret must be {WORD_LENGTH} letters long"
        )
    if len(guess) != WORD_LENGTH:
        raise ValueError(
            f"Guess must be {WORD_LENGTH} letters long"
        )
    results = [ABSENT] * WORD_LENGTH
    remaining_letters = Counter(secret)
    for index in range(WORD_LENGTH):
        if guess[index] == secret[index]:
            results[index] = CORRECT
            remaining_letters[guess[index]] -= 1
    for index in range(WORD_LENGTH):
        if results[index] == CORRECT:
            continue
        letter = guess[index]
        if remaining_letters[letter] > 0:
            results[index] = PRESENT
            remaining_letters[letter] -= 1
    return GuessResult(guess, results)

class Game:
    def __init__(
        self,
        secret: str,
        word_list: list[str],
    ) -> None:
        self.secret = secret.lower()
        self.word_list = [
            word.lower()
            for word in word_list
        ]
        self.guesses: list[GuessResult] = []
        if len(self.secret) != WORD_LENGTH:
            raise ValueError(
                f"Secret must be {WORD_LENGTH} letters long"
            )
        if self.secret not in self.word_list:
            raise ValueError(
                "Secret word must be in the word list"
            )

    def make_guess(self, guess: str) -> GuessResult:
        if self.is_over:
            raise ValueError("Game is over")
        word = guess.strip().lower()
        if len(word) != WORD_LENGTH:
            raise ValueError(
                f"Guess must be {WORD_LENGTH} letters long"
            )
        if word not in self.word_list:
            raise ValueError(
                "Guess must be a valid word"
            )
        result = evaluate_guess(self.secret, word)
        self.guesses.append(result)
        return result

    @property
    def is_won(self) -> bool:
        return any(
            result.guess == self.secret
            for result in self.guesses
        )

    @property
    def is_over(self) -> bool:
        return self.is_won or len(self.guesses) >= MAX_GUESSES

    def __str__(self) -> str:
        lines = [
            "",
            "WORDLE",
            "======",
        ]
        for result in self.guesses:
            lines.append(str(result))
            lines.append("")
        remaining = MAX_GUESSES - len(self.guesses)
        lines.append(
            f"Guesses remaining: {remaining}/{MAX_GUESSES}"
        )
        return "\n".join(lines)