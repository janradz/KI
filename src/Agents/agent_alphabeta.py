from Agents.agent import Agent
from Algorithms.alphabeta import AlphaBeta
from State.problem import GameState


class AgentAlphaBeta(Agent):

    def __init__(self):
        super().__init__()
        self.algo = AlphaBeta()



    def get_move(self, game_state: GameState) -> tuple[int, int]:
        action: tuple[int,int] = self.algo.alphabeta_decision(game_state)
        print("AlphaBeta Aufrufe: " + str(self.algo.counter))
        self.algo.counter = 0
        return action
