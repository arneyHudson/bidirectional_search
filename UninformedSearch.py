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

def bidirectional_search(problem: Problem) -> Any:
    """
    TODO
    """
    initial_node = Node(problem.initial)
    goal_node = Node(problem.goal)

    if problem.is_goal(initial_node.state):
        return get_path(initial_node)
    if problem.is_goal(goal_node.state):
        return get_path(goal_node)

    # Initialize the frontiers and reached sets for the forward and backward searches
    forward_frontier = [initial_node]
    backward_frontier = [goal_node]
    forward_reached = {problem.hashable_state(initial_node.state): initial_node}
    backward_reached = {problem.hashable_state(goal_node.state): goal_node}

    while forward_frontier and backward_frontier:
        # Perform forward search expansion
        forward_node = forward_frontier.pop()
        for forward_child in problem.expand(forward_node):
            forward_state = forward_child.state
            forward_state_key = problem.hashable_state(forward_state)
            if forward_state_key in backward_reached:
                # Path found, combine paths from forward and backward searches
                backward_node = backward_reached[forward_state_key]
                forward_path = get_path(forward_child)
                backward_path = get_path(backward_node)[::-1]  # Reverse the backward path
                return forward_path + backward_path

            if forward_state_key not in forward_reached:
                forward_reached[forward_state_key] = forward_child
                forward_frontier.append(forward_child)

        # Perform backward search expansion
        backward_node = backward_frontier.pop()
        for backward_child in problem.expand(backward_node):
            backward_state = backward_child.state
            backward_state_key = problem.hashable_state(backward_state)
            if backward_state_key in forward_reached:
                # Path found, combine paths from forward and backward searches
                forward_node = forward_reached[backward_state_key]
                forward_path = get_path(forward_node)
                backward_path = get_path(backward_child)[::-1]  # Reverse the backward path
                return forward_path + backward_path

            if backward_state_key not in backward_reached:
                backward_reached[backward_state_key] = backward_child
                backward_frontier.append(backward_child)

    return []  # no path found

    return []  # no path found


