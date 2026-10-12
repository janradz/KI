from State.problem import GameState, Problem
from Agents.agent import Agent
from Algorithms.uniform_search import uniform_cost_search


class agentvV(Agent):

    def __init__(self):
        self.actionsequence = []
        self.state = None
        self.goal = None
        self.problem = None



    def update_state(self,  percept):
        return percept

    def simple_problem_solving(self, percept: GameState) -> tuple[int, int]:
        self.state: GameState = self.update_state(percept)
        if self.actionsequence == []:
            self.problem: Problem = Problem(initial_gamestate= self.state)
            self.actionsequence = uniform_cost_search(self.problem)
            if self.actionsequence is None:
                return None
        action: tuple[int, int] = self.actionsequence.pop(0)
        return action

    def get_move(self, game_state: GameState) -> tuple[int, int]:

        action: tuple[int,int] = self.simple_problem_solving(game_state)
        return action





"""
function SIMPLE-PROBLEM-SOLVING-AGENT ( _percept ) returns an action
2 persistent: _seq, an action sequence, initially empty
3 _state, some description of the current world state
4 _goal, a goal, initially null
5 _problem, a problem formulation
6
7 _state → UPDATE-STATE ( _state, _percept )
8
9 if _seq is empty then
10 _goal → FORMULATE-GOAL ( _state )
11 _problem → FORMULATE-PROBLEM ( _state, _goal )
12 _seq → SEARCH ( _problem )
13
14 if _seq = failure then
15 return a null action
16
17 _action → FIRST ( _seq )
18 _seq → REST ( _seq )
19
20 return _action
"""