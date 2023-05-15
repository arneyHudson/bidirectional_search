from __future__ import annotations  # needed in order to reference a Class within itself

from typing import List, Any, Generic, TypeVar
from abc import ABC, abstractmethod
import numpy as np

# https://realpython.com/python-type-checking/
T = TypeVar('T')


class Node(Generic[T]):
    count = 0

    def __init__(self, state: T, parent: Node = None, action: str = None, path_cost: float = 0, depth: int = 0):
        """ This constructor stores the references when the Node is
        initialized. """
        self._state = state
        self._parent = parent
        self._action = action
        self._path_cost = path_cost
        self._id = Node.count
        self._depth = depth
        Node.count += 1

    @property
    def state(self) -> T:
        """state this node represents"""
        return self._state

    @property
    def parent(self) -> Node:
        """returns the parent of this node"""
        return self._parent

    @property
    def action(self) -> str:
        """returns action it took to get to this node"""
        return self._action

    @property
    def path_cost(self) -> float:
        """returns the cost to get to this node"""
        return self._path_cost

    @property
    def depth(self) -> int:
        """returns the depth of this node"""
        return self._depth

    def __str__(self) -> str:
        """String representation of the node"""
        ret = "ID: " + str(self._id) + "\n"
        ret += "State: \n" + str(self.state) + "\n"
        ret += "ParentID: " + ("None" if self.parent is None else str(self.parent._id)) + "\n"
        ret += "Action: " + str(self._action) + "\n"
        ret += "Cost: " + str(self._path_cost) + "\n"
        ret += "Depth: " + str(self._depth) + "\n"
        return ret

    # You shouldn't need either of these
    # def __eq__(self, other):
    #    """returns true is two nodes have the same state"""
    #    return self.state == other.state

    # def __repr__(self) -> str:
    #    """String representation when in a list"""
    #    return self.__str__()


class Problem(ABC, Generic[T]):
    def __init__(self, initial_state: T, goal_state: T):
        """
        Create a generic problem that can be solved with an Uninformed Search algorithm
        :param initial_state: initial state which can be any type T
        :param goal_state: goal state which can be any type T
        """
        self._initial: T = initial_state
        self._goal: T = goal_state

    @property
    def goal(self) -> T:
        return self._goal

    @property
    def initial(self) -> T:
        return self._initial

    @abstractmethod
    def is_goal(self, state: T) -> bool:
        """
        Returns true if the pass in state equals goal
        :param state: state to test
        :return: true or false if state equals goal
        """
        pass

    @abstractmethod
    def expand(self, node: Node) -> List[Node]:
        """
        Creates a new list of Node objects for all the
        neighboring states of the state in node.
        :param node: Node object that represents a state
        :return: List of Node objects
        """
        pass

    @abstractmethod
    def _actions(self, state: Any) -> List[str]:
        """
        Returns a list of actions available for the
        given state.
        :param state: current state
        :return: List of actions encoded as Strings
        """
        pass

    @abstractmethod
    def hashable_state(self, state: T) -> Any:
        """
        Returns a value that represents the state and is hashable. Needed
        in order to use a state in conjunction with a dictionary like
        the reached set.
        :param state: State object that needs to be hashed
        :return: object that can be hashed
        """
        pass

    @abstractmethod
    def _result(self, current_state: T, action: str) -> T:
        """
        Returns the state generated given the passed in
        current_state and action
        :param current_state: state object
        :param action: String that represents an action
        :return: state that is the result of applying an action to the current state
        """
        pass

    @abstractmethod
    def _action_cost(self, current: T, action: str, next: T) -> float:
        """
        Cost of going from the current state to the next state
        given the provided action
        :param current: state object that represents current state
        :param action: String that represents an action
        :param next: state object that we will transition to
        :return:
        """
        pass

    @abstractmethod
    def estimated_cost(self, current: T):
        """
        Returns an estimate of the cost from the current state to the goal
        :param current: current state
        :return: cost from current state to the goal
        """
        pass


class MazeNavigation(Problem[np.ndarray]):
    """
    Maze Navigation Search problem. This class contains functions
    needed to do uninformed search. Specifically, the functions below
    are built to manipulate a numpy 2D array which is the state
    representation.
    """

    def __init__(self, initial_state: T, goal_state: T):
        """
        Initializes a MazeNavigation type search problem. The
        state objects are 2D numpy arrays
        :param initial_state: Initial state of the problem
        :param goal_state:  Goal state of the problem
        """
        super().__init__(initial_state, goal_state)
        # what each of the numbers in the maze means
        self._character = 2
        self._walkable = 1
        self._impassable = 0

    def is_goal(self, current: T) -> bool:
        """
        Returns true if the passed in state equals the goal state
        :param state: state to test
        :return: true or false if state equals goal
        """
        return np.array_equal(current, self.goal)

    def expand(self, node: Node) -> List[Node]:
        """
        Creates a new list of Node objects for all the
        neighboring states of the state in node.
        :param node: Node object that represents a state
        :return: List of Node objects
        """
        current_state = node.state
        ret = []
        for a in self._actions(current_state):
            next_state = self._result(current_state, a)
            cost = self._action_cost(current_state, a, next_state)
            ret.append(Node(next_state, node, a, node.path_cost + cost, node.depth + 1))
        return ret

    def _actions(self, state: T) -> List[str]:
        """
        Returns a list of actions available for the given state.
        :param state: current state
        :return: List of actions encoded as Strings
        """
        ret = []
        state: T

        # size of the maze
        height, width = state.shape

        # gets our current location within the maze
        row = np.where(state == self._character)[0][0]
        col = np.where(state == self._character)[1][0]

        # checks to see if there is a walkable space
        # in the four cardinal direction
        # North
        if row - 1 >= 0 and state[row - 1][col] != self._impassable:
            ret.append("north")
        # East
        if col + 1 < width and state[row][col + 1] != self._impassable:
            ret.append("east")
        # South
        if row + 1 < height and state[row + 1][col] != self._impassable:
            ret.append("south")
        # West
        if col - 1 >= 0 and state[row][col - 1] != self._impassable:
            ret.append("west")

        return ret

    def _result(self, state: T, action: str) -> T:
        """
        Returns the state generated given the passed in
        current_state and action
        :param current_state: state object
        :param action: String that represents an action
        :return: state that is the result of applying an action to the current state
        """

        ret = np.copy(state)
        # gets our current location within the maze
        row = np.where(state == self._character)[0][0]
        col = np.where(state == self._character)[1][0]

        # move from the current location
        ret[row][col] = self._walkable

        # move to the new location
        if action == "north":
            ret[row - 1][col] = self._character
        elif action == "east":
            ret[row][col + 1] = self._character
        elif action == "south":
            ret[row + 1][col] = self._character
        elif action == "west":
            ret[row][col - 1] = self._character
        return ret

    def _action_cost(self, curr_state: T, action: str, next_state: T) -> float:
        """
        Cost of going from the current state to the next state
        given the provided action
        :param current: state object that represents current state
        :param action: String that represents an action
        :param next: state object that we will transition to
        :return:
        """

        # where we are about to step to
        next_row = np.where(next_state == self._character)[0][0]
        next_col = np.where(next_state == self._character)[1][0]

        # right now the cost for all the walkable tiles is just 1
        # can be modified to add cost for different types of tiles
        # to simulate difficult terrain
        if curr_state[next_row][next_col] == -1:
            return 1
        elif curr_state[next_row][next_col] == self._walkable:
            return 1

    def hashable_state(self, state: T) -> Any:
        """
        Returns a value that represents the state and is hashable. Needed
        in order to use a state in conjunction with a dictionary like
        the reached set.
        :param state: State object that needs to be hashed
        :return: object that can be hashed
        """
        # For the maze navigation, state is a numpy array
        # numpy arrays do not have a hash method, but we can
        # use the value returns by tobytes as a unique representation
        # of the array
        return state.tobytes()

    def estimated_cost(self, current: T):
        """
        Returns an estimate of the cost from the current state to the goal
        :param current: current state
        :return: cost from current state to the goal
        """

        # row and col of current location
        curr_row = np.where(current == self._character)[0][0]
        curr_col = np.where(current == self._character)[1][0]

        # row and col of goal location
        goal_row = np.where(self.goal == self._character)[0][0]
        goal_col = np.where(self.goal == self._character)[1][0]

        # returns manhathan distance between current and goal
        return abs(curr_row - goal_row) + abs(curr_col - goal_col)


class SlidingPuzzle(Problem[np.array]):
    def __int__(self, initial_state: T, goal_state: T):
        super().__init__(initial_state, goal_state)

    def is_goal(self, current: T) -> bool:
        return np.array_equal(current, self.goal)

    def expand(self, node: Node) -> List[Node]:
        current_state = node.state
        ret = []
        for action in self._actions(current_state):
            next_state = self._result(current_state, action)
            cost = self._action_cost(current_state, action, next_state)
            ret.append(Node(next_state, node, action, node.path_cost + cost, node.depth + 1))
        return ret

    def _actions(self, state: T) -> List[str]:
        ret = []
        state: T
        height, width = state.shape
        row = np.where(state == 0)[0][0]
        col = np.where(state == 0)[1][0]

        if row - 1 >= 0:
            ret.append("north")
        if col + 1 < width:
            ret.append("east")
        if row + 1 < height:
            ret.append("south")
        if col - 1 >= 0:
            ret.append("west")

        return ret

    def _result(self, current_state: T, action: str) -> T:
        ret = np.copy(current_state)

        row = np.where(current_state == 0)[0][0]
        col = np.where(current_state == 0)[1][0]

        if action == "north":
            ret[row][col] = ret[row - 1][col]
            ret[row - 1][col] = 0

        elif action == "east":
            ret[row][col] = ret[row][col + 1]
            ret[row][col + 1] = 0

        elif action == "south":
            ret[row][col] = ret[row + 1][col]
            ret[row + 1][col] = 0

        elif action == "west":
            ret[row][col] = ret[row][col - 1]
            ret[row][col - 1] = 0

        return ret

    def _action_cost(self, current: T, action: str, next: T) -> float:
        # TODO I don't know
        return 1

    def hashable_state(self, state: T) -> Any:
        return state.tobytes()

    def estimated_cost(self, current: T):
        distance = 0
        height, width = current.shape()
        for y in range(height):
            for x in range(width):
                value = current[x][y]
                curr_row = np.where(current == value)[0][0]
                curr_col = np.where(current == value)[1][0]

                goal_row = np.where(self.goal == value)[0][0]
                goal_col = np.where(self.goal == value)[1][0]
                distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return distance
