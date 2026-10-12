from abc import ABC

from Algorithms.minimax import  Minimax
from State.problem import GameState, Problem
from Agents.agent import Agent


class AgentMinimax(Agent):

    def __init__(self):
        super().__init__()
        self.algo = Minimax()



    def get_move(self, game_state: GameState) -> tuple[int, int]:
        action: tuple[int,int] = self.algo.minimax_decision(game_state)
        print("Minimax Aufrufe: " + str(self.algo.counter))
        self.algo.counter = 0
        return action

