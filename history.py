from pathlib import Path
import json
class GameHistory:
    def __init__(self,filename):
        self.filename=Path(filename)
        self.games:list[dict[str,object]]=[]
        self._load()

    def _save(self):
            with self.filename.open("w") as file:
                json.dump(self.games,file,indent=2)

    def _load(self):
        if not self.filename.exists():
            self._save()
            return
        try:
            with self.filename.open("r") as f:
                self.games=json.load(f)
        except (json.JSONDecodeError, OSError):
            self.games=[]

    def add_games(self,won:bool,attempts:int, word:str):
        game={"won":won,"attempts":attempts,"word":word}
        self.games.append(game)
        self._save()

    @property
    def total_games(self):
        return len(self.games)

    @property
    def total_wins(self):
        return sum(game["won"] for game in self.games)

    @property
    def win_percentage(self):
        if self.total_games==0:
            return 0
        return (self.total_wins/self.total_games)*100

    @property
    def current_streak(self):
        streak=0
        for game in reversed(self.games):
            if game["won"]:
                streak+=1
            else:
                break
        return streak

    @property
    def max_streak(self):
        max_streak=0
        current_streak=0
        for game in self.games:
            if game["won"]:
                current_streak+=1
                max_streak=max(max_streak,current_streak)
            else:
                current_streak=0
        return max_streak
    
    

