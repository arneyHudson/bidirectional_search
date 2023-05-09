import collections

from Problem import *
from queue import PriorityQueue


def get_path(node: Node) -> List[str]:
    """
    Takes in a Node object and returns
    a reversed list of actions from that node to its root.
    """
    root = node
    p = []
    while root is not None and root.parent is not None:
        p.append(root.action)
        root = root.parent
    p.reverse()
    return p


def a_star(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
    well as search operators (methods). Performs A*
    and returns the path found. Returns and empty list is no path is found.
    """
    node = Node(problem.initial)
    entry = 0
    if problem.is_goal(node.state):
        return node
    frontier = PriorityQueue()
    frontier.put((node.path_cost + problem.estimated_cost(node.state), entry, node))
    entry += 1
    reached = {problem.hashable_state(problem.initial): node}
    while not frontier.empty():
        node = frontier.get()[2]
        if problem.is_goal(node.state):
            return get_path(node)
        for child_node in problem.expand(node):
            state = child_node.state

            s = problem.hashable_state(state)
            if s not in reached or child_node.path_cost < reached[s].path_cost:
                reached[s] = child_node
                frontier.put((node.path_cost + problem.estimated_cost(child_node.state), entry, child_node))
                entry += 1

    return [] # failure


def greedy(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
    well as search operators (methods). Performs a Greedy Search
    and returns the path found. Returns and empty list is no path is found.
    """
    node = Node(problem.initial)
    entry = 0
    if problem.is_goal(node.state):
        return node
    frontier = PriorityQueue()
    frontier.put((problem.estimated_cost(node.state), entry, node))
    entry += 1
    reached = {problem.hashable_state(problem.initial): node}
    while not frontier.empty():
        node = frontier.get()[2]
        if problem.is_goal(node.state):
            return get_path(node)
        for child_node in problem.expand(node):
            state = child_node.state

            s = problem.hashable_state(state)
            if s not in reached or child_node.path_cost < reached[s].path_cost:
                reached[s] = child_node
                frontier.put((problem.estimated_cost(child_node.state), entry, child_node))
                entry += 1

    return []  # failure