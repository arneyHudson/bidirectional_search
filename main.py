import csv
import tracemalloc
import time

from InformedSearch import *
from UninformedSearch import *
from mazes import *




def run_test(maze_type:int, search_type: str, print_stats: bool = True, print_maze: bool = False):
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

    if print_maze:
        # draw_maze(initial_state, goal_state, None)
        print(f"Initial state: ")
        print(initial_state)
        print(f"Goal state: ")
        print(goal_state)

    p1 = MazeNavigation(initial_state, goal_state)

    # memory, time, path length
    stats = [0 for i in range(3)]
    path = []
    n = None

    start = time.time()
    tracemalloc.start()

    if search_type == "b":
        path = breadth_first_search(p1)
    elif search_type == "d":
        path = depth_first_search(p1)
    elif search_type == "a":
        path = a_star(p1)
    elif search_type == "g":
        path = greedy(p1)
    elif search_type == "s":
        path = bidirectional_search(p1)

    memory_usage = tracemalloc.get_traced_memory()
    stats[0] = memory_usage[1]
    tracemalloc.stop()
    end = time.time()

    stats[1] = (end - start)
    stats[2] = len(path)

    if print_stats:
        print(f"Memory usage: {stats[0]:.2e}")
        print(f"Elasped time {stats[1]:.4f}")
        print(f"Path length: {stats[2]}")
        print(f"Path: {path}")

    return stats, path


if __name__ == '__main__':
    print_maze = False
    print_stats = True
    filename = "searchResultsExample.csv"

    algorithm = input(f"Which algorithm do you want to run: "
                      f"\n(b)Breadth First Search "
                      f"\n(d)Depth First Search "
                      f"\n(a)A* Search "
                      f"\n(g)Greedy Search "
                      f"\n(s)Bidirectional Search"
                      f"\n(c)All\n")
    num_mazes = 11
    maze_num = input(f"Enter a number from 1 to {num_mazes} to indicate which maze you want to run or -1 for all: ")

    if maze_num == "-1":
        mazes = [i + 1 for i in range(num_mazes)]
    elif 1 <= int(maze_num) <= num_mazes:
        mazes = [int(maze_num)]
    else:
        print("Invalid maze number")
        mazes = []

    stats = []
    rows = []
    for m in mazes:
        print(f"\nMaze num: {m}")
        if algorithm == "c" or algorithm == "d":
            if print_stats:
                print(f"DFS_{m}")
                s, p = run_test(m, "d", print_stats, print_maze)
            stats.append([f"DFS_{m}"] + s + p)
        if algorithm == "c" or algorithm == "b":
            if print_stats:
                print(f"BFS_{m}")
                s, p = run_test(m, "b", print_stats, print_maze)
            stats.append([f"BFS_{m}"] + s + p)
        if algorithm == "c" or algorithm == "a":
            if print_stats:
                print(f"A*_{m}")
                s, p = run_test(m, "a", print_stats, print_maze)
            stats.append([f"A*_{m}"] + s + p)
        if algorithm == "c" or algorithm == "g":
            if print_stats:
                print(f"Greedy_{m}")
                s, p = run_test(m, "g", print_stats, print_maze)
            stats.append([f"Greedy_{m}"] + s + p)
        if algorithm == "c" or algorithm == "s":
            if print_stats:
                print(f"Bidirectional_{m}")
                s, p = run_test(m, "s", print_stats, print_maze)
            stats.append([f"Bidirectional_{m}"] + s + p)


    header = ["Run", "Memory", "Time", "Path Length", "Path"]

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(stats)

