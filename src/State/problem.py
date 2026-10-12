

from dataclasses import dataclass
@dataclass(frozen=True)
class GameState:
    drawn_edges: frozenset[tuple[int, int]]
    not_drawn_edges: frozenset[tuple[int, int]] #entkoppelt von eigentlichen gamestate, quasi ein snapshot fürs vorrechnen
    current_player: str
    scores: tuple[int, int] #punkte p1,p2
    all_edges: frozenset[tuple[int, int]]



class Node:
    def __init__(self, gameState, parent=None, action=None, path_cost=0):
        self.state = gameState
        self.parent = parent
        self.path_cost = 0 if parent is None else parent.path_cost + 1
        self.action = action




    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f"Node(state={self.state}, path_cost={self.path_cost}, points={self.state.scores})"

    def is_terminal(self) -> bool:
        # gamestate ist terminal wenn alle boxes geschlossen sind
        return len(self.state.not_drawn_edges) == 0


BOXES = [
    {(0,1),(1,4),(3,4),(0,3)},
    {(1,2),(2,5),(4,5),(1,4)},
    {(3,4),(4,7),(6,7),(3,6)},
    {(4,5),(5,8),(7,8),(4,7)}
]

def completed_boxes(drawn_edges):
    count = 0
    for box in BOXES:
        if box.issubset(drawn_edges):
            count += 1
    return count

class Problem:
    def __init__(self, initial_gamestate=None):

        edges = frozenset([(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(3,6),(4,7),(5,8),(6,7),(7,8)])
        if initial_gamestate is None:
            self.initial_gamestate = GameState(frozenset(),edges,"red", (0,0),edges)
        else: self.initial_gamestate = initial_gamestate
        self.goal_gamestate = GameState(frozenset(edges),frozenset(),"red", (2,2),edges)
        self.goal_gamestate2 = GameState(frozenset(edges),frozenset(), "green", (2, 2), edges)
        self.initial_state: Node = Node(self.initial_gamestate)


    def goal_test(self, state):
        if state == self.goal_gamestate or state == self.goal_gamestate2:
            return True
        return False

def actions(node: Node):
    actions = []

    for edge in node.state.not_drawn_edges:
        actions.append(edge)

    return actions



def result(node: Node, action: tuple[int, int]) -> GameState:
    new_drawn_edges = set(node.state.drawn_edges)
    new_drawn_edges.add(action)
    new_not_drawn_edges = set(node.state.not_drawn_edges)
    new_not_drawn_edges.remove(action)

    # check for new Boxes
    old_boxes = completed_boxes(node.state.drawn_edges)
    new_boxes = completed_boxes(new_drawn_edges)
    p1_points, p2_points = node.state.scores
    gained_points = new_boxes -old_boxes
    if gained_points > 0:
        if node.state.current_player == "red":
            p1_points += gained_points
            next_player = "red"
        else:
            p2_points += gained_points
            next_player = "green"
    else:
        next_player = "green" if node.state.current_player == "red" else "red"

    return GameState(frozenset(new_drawn_edges), frozenset(new_not_drawn_edges), next_player, (p1_points, p2_points), node.state.all_edges)





