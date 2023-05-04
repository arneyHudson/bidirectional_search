import queue
from Problem import *


def get_path(node: Node) -> List[str]:
    """
    Takes in a Node object and returns
    a reversed list of actions from that node to its root.
    """
    root = node
    p = []
    while root is not None:
        p.append(root.action)
        root = root.parent
    p.reverse()
    return p


def breadth_first_search(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
    well as search operators (methods). Performs a Breadth First Search
    and returns the path found using the get_path method. For example,
    return get_path(node), where node is the node with a state that
    matches the goal. Returns and empty list if no path is found.
    """
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return get_path(node)

    frontier = queue.Queue()  # Frontier is a queue that we use as a FIFO queue
    frontier.put(node)
    reached = {problem.hashable_state(node.state): node}

    while not frontier.empty():
        node = frontier.get()

        for child in problem.expand(node):
            state = child.state
            if problem.is_goal(state):
                # construct the path by traversing parent links
                return get_path(child)

            state_key = problem.hashable_state(state)
            if state_key not in reached:
                reached[state_key] = child
                frontier.put(child)

    return []  # no path found



def depth_first_search(problem: Problem) -> Any:
    """
    Takes in a Problem object that has an initial and goal state as
     well as search operators (methods). Performs a Depth First Search
     and returns the path found using the get_path method. For example,
     return get_path(node), where node is the node with a state that
      matches the goal. Returns and empty list if no path is found.
     """
    initial_node = Node(problem.initial)
    if problem.is_goal(initial_node.state):
        return get_path(initial_node)

    frontier = [initial_node]
    reached = {problem.hashable_state(initial_node.state): initial_node}

    while frontier:
        node = frontier.pop()

        for child in problem.expand(node):
            state = child.state
            if problem.is_goal(state):
                # construct the path by traversing parent links
                return get_path(child)

            state_key = problem.hashable_state(state)
            if state_key not in reached:
                reached[state_key] = child
                frontier.append(child)

    return []  # no path found


