from dataclasses import dataclass
from typing import Optional
import heapq
cell_cost = {
    '.': 1,
    'S': 1,
    'E': 1,
    'H': 4,
    'D': 10
    # Wände sind nicht begehbar und erhalten daher keinen Eintrag.
}
@dataclass
class SearchNode:
    position: tuple[int, int] # (x,y)
    g_cost:  int
    f_cost: int
    parent: Optional['SearchNode'] = None

    #spezifisches handling
    def __lt__(self, other):
        return self.f_cost < other.f_cost

#h(n) funktion, nutzt manhattan distance
def heuristic(start_position, end_position) -> int:
    manhattan_distance = abs(start_position[0] - end_position[0]) + abs(start_position[1] - end_position[1])

    return manhattan_distance

#parsing aus der txt
def parse(file_path: str):
    maze : dict[tuple[int, int], int] = {}
    start_position = None
    end_position = None
    with open(file_path, 'r') as file:
        for y, line in enumerate(file):
            if line.strip() == "" or line.startswith("Legend:"):
                break
            clean = line.split()
            for x, char in enumerate(clean):

                if char in cell_cost:
                    maze[(x, y)] = cell_cost[char]
                if char == 'S':
                    start_position = (x, y)
                elif char == 'E':
                    end_position = (x, y)

    return maze, start_position, end_position

#hol dir alle möglichen nachbarn der node
def get_neighbors(current_position, maze)-> list[tuple[int, int]]:
    neighbors = []
    x,y = current_position
    # rechts, links, unten, oben
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx,dy in directions:
        new_position = (x + dx, y + dy)
        if new_position in maze:
            neighbors.append(new_position)
    return neighbors


def reconstruct_path(goal_node):
    path =  []
    while goal_node is not None:
        path.append(goal_node.position)
        goal_node = goal_node.parent

    path.reverse()
    return path

'''
Evaluierungsfunkton: f(n) = g(n) + h(n)
g(n): Pfadkosten von Ausgangszustand zum Knoten n
h(n): geschätzte Kosten von n zu einem Ziel
'''


def a_star(maze, start_position, end_position):
    start_node = SearchNode(position= start_position, g_cost = 0, f_cost= heuristic(start_position, end_position), parent=None)


    #init priority queue
    #frontier ist für nodes die noch untersucht werden sollen
    #mit heapq machen wir dass der kleinste f_cost oben liegt
    '''_frontier <- a priority queue ordered by PATH-COST'''
    #idee analog gerippt aus uniform cost search, anstatt PATH-COST hier f-cost
    frontier = []
    heapq.heappush(frontier, start_node) #besagte priority queue

    #unser visited memory
    g_scores = {start_position: 0}
    explored_nodes = {}

    while frontier:
        current_node = heapq.heappop(frontier)

        #veraltete Heap-Einträge überspringen
        if current_node.g_cost > g_scores.get(current_node.position, float("inf")):
            continue

        explored_nodes[current_node.position] = current_node
        # check ob wir am ziel sind, quasi goaltest function
        '''_node <- POP(_frontier) /* chooses the lowest-cost node in frontier * /
            if _problem.GOAL-TEST(_node.STATE) then
            return SOLUTION(_node)
        '''
        if current_node.position == end_position:
            path = reconstruct_path(current_node)
            return path, g_scores, explored_nodes

        for neighbor_position in get_neighbors(current_position= current_node.position, maze= maze):
            new_g_score = current_node.g_cost + maze[neighbor_position] #g(n)

            '''else if _child.STATE is in
                _frontier with higher PAST-COST
                then
                replace that frontier node with _child'''
            #"falls knoten durch pfad mit günstigeren kosten erreicht wird: ersetze alten teureren durch günstigeren pfad"
            #A* soll pruning verwenden -> g_scores dict
            if neighbor_position not in g_scores or new_g_score < g_scores[neighbor_position]:
                g_scores[neighbor_position] = new_g_score

                new_f = new_g_score + heuristic(neighbor_position, end_position) #f(n) = g(n) + h(n)
                better_node = SearchNode(position= neighbor_position, g_cost= new_g_score, f_cost= new_f, parent= current_node)

                heapq.heappush(frontier, better_node)

    return

def main():
    maze, start_position, end_position = parse("maze_with_legend.txt")

    if start_position is None or end_position is None:
        print("Start oder Ziel nicht gefunden!")
        return

    result = a_star(maze, start_position, end_position)

    if result is None:
        print("Kein Pfad gefunden.")
        return

    path, _, _ = result

    print("Gefundener Pfad:")
    for step in path:
        print(step)

if __name__ == "__main__":
    main()
