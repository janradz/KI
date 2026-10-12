import unittest

from State.problem import GameState, Node, Problem, actions as available_actions, result
from Algorithms.uniform_search import uniform_cost_search


class TestSearch(unittest.TestCase):

    def _all_edges(self) -> frozenset[tuple[int, int]]:
        return frozenset({
            (0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4),
            (4, 5), (3, 6), (4, 7), (5, 8), (6, 7), (7, 8)
        })

        #prüfen ob wir überhaupt valide edges bekommen
    def test_actions_returns_all_available_edges(self):
        edges = self._all_edges()
        state = GameState(
            drawn_edges=frozenset(),
            not_drawn_edges=edges,
            current_player="red",
            scores=(0, 0),
            all_edges=edges
        )
        problem = Problem(initial_gamestate=state)
        node = Node(state)

        actions = available_actions(node)

        self.assertEqual(set(actions), set(edges))
        self.assertEqual(len(actions), len(edges))


    #standardfall test, passsiert am öftesten
    def test_result_without_box_switches_player_and_keeps_score(self):
        edges = self._all_edges()
        state = GameState(
            drawn_edges=frozenset(),
            not_drawn_edges=edges,
            current_player="red",
            scores=(0, 0),
            all_edges=edges
        )
        problem = Problem(initial_gamestate=state)
        node = Node(state)

        next_state = result(node, (0, 1))  # kein Box-Abschluss

        self.assertEqual(next_state.current_player, "green")
        self.assertEqual(next_state.scores, (0, 0))
        self.assertIn((0, 1), next_state.drawn_edges)
        self.assertNotIn((0, 1), next_state.not_drawn_edges)

    #punktscore test
    def test_result_with_box_gives_point_and_keeps_player(self):
        edges = self._all_edges()
        drawn = frozenset({(0, 1), (1, 4), (3, 4)})  # 3 seiten einer Box
        state = GameState(
            drawn_edges=drawn,
            not_drawn_edges=edges - drawn,
            current_player="red",
            scores=(0, 0),
            all_edges=edges
        )
        problem = Problem(initial_gamestate=state)
        node = Node(state)

        next_state = result(node, (0, 3))  # schließt box

        self.assertEqual(next_state.current_player, "red")
        self.assertEqual(next_state.scores, (1, 0))
        self.assertIn((0, 3), next_state.drawn_edges)
        self.assertNotIn((0, 3), next_state.not_drawn_edges)


    #was wenn unentschieden erreicht
    def test_uniform_cost_search_returns_plan_reaching_goal(self):
        edges = self._all_edges()
        initial = GameState(
            drawn_edges=frozenset(),
            not_drawn_edges=edges,
            current_player="red",
            scores=(0, 0),
            all_edges=edges
        )
        problem = Problem(initial_gamestate=initial)

        plan = uniform_cost_search(problem)

        self.assertIsNotNone(plan)
        self.assertGreater(len(plan), 0)

        # validation
        node = Node(initial)
        for action in plan:
            next_state = result(node, action)
            node = Node(next_state, parent=node, action=action)

        self.assertTrue(problem.goal_test(node.state))