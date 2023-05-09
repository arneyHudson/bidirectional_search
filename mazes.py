import numpy as np
from shapes import *


def basic_maze():
    """
    basic maze used as an initial test for the search algorithms
    :return: initial and goal states as a tupple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.array([[2, 1, 0], [0, 1, 0], [0, 1, 1]])
    goal_state = np.array([[1, 1, 0], [0, 1, 0], [0, 1, 2]])
    return [initial_state, goal_state]


def goaless_maze():
    """
    maze with an unreachable state
    :return: initial and goal states as a tupple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.array([[1, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 1, 2, 1, 0], [1, 0, 1, 0, 1], [1, 1, 1, 0, 1]])
    goal_state = np.array([[1, 1, 1, 1, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 1, 0, 2]])
    return [initial_state, goal_state]


def cross_maze(size, start_loc, end_loc):
    """
    Maze that is a cross.
    :return: initial and goal states as a tuple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.zeros((size, size))

    # create a cross of ones
    initial_state[int(size / 2), :] = 1
    initial_state[:, int(size / 2)] = 1

    goal_state = np.copy(initial_state)

    initial_state[start_loc[0]][start_loc[1]] = 2
    goal_state[end_loc[0]][end_loc[1]] = 2

    return [initial_state, goal_state]


def border_maze(size, start_loc, end_loc):
    """
    Maze that is just a ring around the border of the maze.
    :return: initial and goal states as a tuple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.zeros((size, size))

    # create a border of ones
    initial_state[0, :] = 1
    initial_state[size - 1, :] = 1
    initial_state[:, 0] = 1
    initial_state[:, size - 1] = 1

    goal_state = np.copy(initial_state)

    initial_state[start_loc[0]][start_loc[1]] = 2
    goal_state[end_loc[0]][end_loc[1]] = 2

    return [initial_state, goal_state]


def informed_maze():
    """
    Maze to test Greedy and A* in week 3. Contains a deceptive goal location that will cause
    Greedy to return the non-optimal solution
    :return: initial and goal states as a tuple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.ones((5, 5))
    initial_state[1,1:] = 0
    initial_state[3,1:4] = 0
    goal_state = np.copy(initial_state)

    initial_state[4,2] = 2
    goal_state[0,4] = 2
    return [initial_state, goal_state]


def open_maze(size, start_loc, end_loc):
    """
    Maze that is just a bunch of open space.
    :return: initial and goal states as a tuple. 0s are impassable,
    1s are walkable, and 2s represent location of the agent
    """
    initial_state = np.ones((size, size))
    goal_state = np.copy(initial_state)

    initial_state[start_loc[0]][start_loc[1]] = 2
    goal_state[end_loc[0]][end_loc[1]] = 2

    return [initial_state, goal_state]


def draw_maze(initial_state: np.ndarray, goal_state: np.ndarray):
    w = 640
    h = 640
    paper = Paper(w, h)
    grid_size = min(int(h / initial_state.shape[0]), int(w / initial_state.shape[1]))
    start = np.where(initial_state == 2)
    goal = np.where(goal_state == 2)
    for i in range(initial_state.shape[0]):
        for j in range(initial_state.shape[1]):
            r = Rectangle()
            r.set_width(grid_size)
            r.set_height(grid_size)
            r.set_x(j * grid_size)
            r.set_y(i * grid_size)
            if i == start[0] and j == start[1]:
                r.set_color("green")
            elif i == goal[0] and j == goal[1]:
                r.set_color("red")
            elif initial_state[i][j] == 0: # impassable
                r.set_color("black")
            elif initial_state[i][j] == -1: # higher path cost
                r.set_color("gray")
            else:
                r.set_color("white")
            r.draw()
    paper.display()


if __name__ == '__main__':
    maze_type = 11

    if maze_type == 1:
        initial_state, goal_state = basic_maze()
    elif maze_type == 2:
        initial_state, goal_state = goaless_maze()
    elif maze_type == 3:
        # start in the center and goal is north at end of spoke
        initial_state, goal_state = cross_maze(101, [50, 50], [0, 50])
    elif maze_type == 4:
        # start in the center and goal is west at end of spoke
        initial_state, goal_state = cross_maze(101, [50, 50], [50, 0])
    elif maze_type == 5:
        # start in the center and goal is north midway down the spoke
        initial_state, goal_state = cross_maze(101, [50, 50], [25, 50])
    elif maze_type == 6:
        # start in the center and goal is west midway down the spoke
        initial_state, goal_state = cross_maze(101, [50, 50], [50, 25])
        # initial_state, goal_state = test_maze6()
    elif maze_type == 7:
        # start left center and goal is top center
        initial_state, goal_state = border_maze(101, [50, 0], [0, 50])
    elif maze_type == 8:
        # start left center and goal is bottom center
        initial_state, goal_state = border_maze(101, [50, 0], [100, 50])
    elif maze_type == 9:
        # start left center and goal is upper left
        initial_state, goal_state = border_maze(101, [50, 0], [0, 0])
    elif maze_type == 10:
        # start left center and goal is lower left
        initial_state, goal_state = border_maze(101, [50, 0], [100, 0])
    elif maze_type == 11:
        # Informed search test maze
        initial_state, goal_state = informed_maze()
    else:
        initial_state = np.array([])
        goal_state = np.array([])

    if len(initial_state) != 0 and len(goal_state) != 0:
        draw_maze(initial_state, goal_state)
