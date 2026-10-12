from typing import Any

from State.problem import Node, GameState, actions, result
import numpy as np

class AlphaBeta:
    def __init__(self, game_state: GameState=None):
        self.game_state = game_state
        self.counter: int = 0


    def utility(self, game_state: GameState, max_player: str) -> float:
        p1_points, p2_points = game_state.scores

        # 1. zuordnung von punkten laut agent
        if max_player == "red":
            my_points = p1_points
            enemy_points = p2_points

        else:  # my_color == "green"
            my_points = p2_points
            enemy_points = p1_points

        # 2. auswertung des zustandes (gewonnen: +1, verloren: -1, unentschieden: 0)

        if my_points > enemy_points:
            return 1
        elif my_points < enemy_points:
            return -1
        else:
            return 0


    def alphabeta_decision(self, game_state: GameState):
        node = Node(game_state)
        best_child_node: Node = node  #evt fehlerquelle
        value_best_child_node = -np.inf
        max_player = game_state.current_player

        for action in actions(node):
            child_state = result(node, action)
            child_node = Node(child_state, parent=node, action=action)
            value_child_node = self.min_value(child_node, max_player, -np.inf, np.inf)
            if value_child_node > value_best_child_node:
                best_child_node = child_node
                value_best_child_node = value_child_node

        return best_child_node.action


    def max_value(self, node: Node, max_player: str, alpha: float, beta: float) -> float:
        #check 1: ist unser gamestate terminal?
        self.counter += 1

        if node.is_terminal():
            return self.utility(node.state, max_player)
        value = -np.inf

        for action in actions(node):
            child_state = result(node, action)
            child_node = Node(child_state, parent=node, action=action)
            if (child_state.current_player == node.state.current_player):
                value_child_node = self.max_value(child_node, max_player, alpha, beta)
            else: value_child_node =  self.min_value(child_node, max_player, alpha, beta)
            
            if value_child_node > value:
                value = value_child_node
                alpha = max(alpha, value)
            if beta <= value:
                break
        return value


    def min_value(self, node: Node, max_player: str, alpha: float, beta: float) -> float:
        self.counter += 1
        if node.is_terminal():
            return self.utility(node.state, max_player)
        value = np.inf

        for action in actions(node):
            child_state = result(node, action)
            child_node = Node(child_state, parent=node, action=action)
            if (child_state.current_player == node.state.current_player):
                value_child_node = self.min_value(child_node, max_player, alpha, beta)
            else: value_child_node = self.max_value(child_node, max_player, alpha, beta)
            if value_child_node < value:
                value = value_child_node
                beta = min(beta, value)
            if alpha >= value:
                break
        return value



