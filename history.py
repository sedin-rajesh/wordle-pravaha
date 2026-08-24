import json
from pathlib import Path

class GameHistory:
    def __init__(self,filename: str="history.json")->None:
        self.filename=Path(filename)
        self.games: list[dict[str,object]]=[]
        self._load()

    def _load(self)->None:
        if not self.filename.exists():
            self._save()
            return 
        try:
            with self.filename.open("r") as file:
                data=json.load(file)
            if not isinstance(data,list):
                raise ValueError("Invalid history file format")
            self.games=data
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError(f"Failed to load history file: {error}") from error

    def _save(self)->None:
        with self.filename.open("w") as file:
            json.dump(self.games,file,indent=4)
    def record_game(self,won:bool,attempts:int,word:str)->None:
        game={
            "won":won,
            "attempts":attempts,
            "word":word
        }
        self.games.append(game)
        self._save()

    @property
    def total_games(self)->int:
        return len(self.games)

    @property
    def total_wins(self)->int:
        return sum(1 for game in self.games if game["won"])

    @property
    def win_percentage(self)->float:
        if self.total_games==0:
            return 0.0
        return (self.total_wins/self.total_games)*100

    @property
    def current_streak(self)->int:
        streak=0
        for game in reversed(self.games):
            if game["won"]:
                streak+=1
            else:
                break
        return streak

    @property
    def best_streak(self)->int:
        best_streak=0
        current_streak=0
        for game in self.games:
            if game["won"]:
                current_streak+=1
                best_streak=max(best_streak,current_streak)
            else:
                current_streak=0
        return best_streak

