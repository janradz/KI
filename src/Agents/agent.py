from abc import ABC, abstractmethod
from State.problem import GameState

#basisklasse für spätere Agenten
class Agent(ABC):
    def __init__(self):
        pass


    #wir brauchen move für alle agenten
    @abstractmethod
    def get_move(self, game_state: GameState) -> tuple:
        pass



    