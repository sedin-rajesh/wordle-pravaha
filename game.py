from collections import Counter
MAX_GUESSES=6
WORD_LENGTH=5
class GuessResult:
    def __init__(self,guess:str,result):
        self.guess=guess
        self.result=result

    def __str__(self):
        guess=" ".join(self.guess)
        result=" ".join(self.result)
        return f"{guess}\n{result}"

class Game:
    def __init__(self,secret:str,word_list:list[str] ):
        self.secret=secret
        self.word_list=word_list
        self.guesses=[]

    def make_guess(self,word:str):
        if len(word)!=WORD_LENGTH:
            raise ValueError("Guess must be 5 letters in length!")
        if word not in self.word_list:
            raise ValueError("Invalid word!")
        if self.is_over:
            raise ValueError("Game is over")
        result=evaluate_guess(self.secret,word)
        self.guesses.append(result)
        return result

    @property
    def is_won(self):
        for result in self.guesses:
            if result.guess==self.secret:
                return True
        return False
    @property
    def is_over(self):
        return self.is_won or len(self.guesses)>=MAX_GUESSES

    def __str__(self):
        output="\nWORDLE\n======\n"
        for result in self.guesses:
            output+=str(result)+"\n\n"
        return output

def evaluate_guess(secret,guess):
    secret_count=Counter(secret)
    result=["X"]*WORD_LENGTH
    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            result[i]="✓"
            secret_count[guess[i]]-=1
    for i in range(WORD_LENGTH):
        if result[i]=="✓":
            continue
        if secret_count[guess[i]]>0:
            result[i]="~"
            secret_count[guess[i]]-=1
    
    return GuessResult(guess,result)
