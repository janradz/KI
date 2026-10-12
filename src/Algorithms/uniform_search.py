import heapq

from State.problem import Node, GameState, actions, result


def uniform_cost_search(problem, heuristic=None):
    """Uniform Cost Search"""
    _node: Node = problem.initial_state
    _frontier = []
    heapq.heappush(_frontier, _node)  # add initial node to frontier
    _explored = set()
    while _frontier:
        _node = heapq.heappop(_frontier)  # chooses the lowest-cost node in frontier
        if problem.goal_test(_node.state):
            return solution(_node, problem)

        _explored.add(_node.state)
        for action in actions(_node):
            child_state: GameState = result(_node, action)
            _child = Node(child_state, _node, action)
            if _child.state not in _explored and _child not in _frontier:
                heapq.heappush(_frontier, _child)
            elif _child in _frontier:
                # If child is already in frontier with higher path cost, replace it

                index = _frontier.index(_child)
                if _frontier[index].path_cost > _child.path_cost:
                    _frontier[index] = _child
                    heapq.heapify(_frontier)  # Reorder the heap after replacement



def solution(node, problem_in_solution):
    actionsequence = []
    while node.state != problem_in_solution.initial_gamestate:
        actionsequence.append(node.action)
        node = node.parent
    actionsequence.reverse()
    return actionsequence

"""
function UNIFORM-COST-SEARCH ( _problem ) returns a solution, or failure
_node → a node with STATE = _problem.INITIAL-STATE.PATH-COST = 0
_frontier → a priority queue ordered by PATH-COST, with _node as the only element
_explored → an empty set
loop do
if EMPTY?( _frontier ) then
return failure
 _node → POP ( _frontier ) /* chooses the lowest-cost node in frontier */
 if _problem.GOAL-TEST ( _node.STATE ) then
 return SOLUTION ( _node )
 add _node.STATE to _explored

 for each _action in _problem.ACTIONS ( _node.STATE ) do
 _child → CHILD-NODE ( _problem, _node, _action )
 if _child.STATE is not in _explored or _frontier then
 _frontier → INSERT ( _child, _frontier )
 else if _child.STATE is in _frontier with higher PATH-COST then
 replace that frontier node with _child
"""