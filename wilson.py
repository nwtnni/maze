from maze import Maze, Point
from random import choice
from sys import argv
from time import sleep


def prune(path, dirpath):
    last = path[-1]
    if path.count(last) > 1:
        a = path.index(last)
        path = path[:a + 1]
        dirpath = dirpath[:a]
    return (path, dirpath)


def generate(w, h, step=False):
    maze = Maze(w, h)
    n = maze.rand_point()
    unknown = set([Point(x, y) for x in range(w) for y in range(h)])
    unknown.remove(n)

    while len(unknown) > 0:
        path = [choice(list(unknown))]
        dirpath = []

        while path[-1] in unknown:
            last = path[-1]
            dirs = maze.neighbors(last)
            path.append(last.adj(dirs[0]))
            dirpath.append(dirs[0])
            path, dirpath = prune(path, dirpath)

        for i in range(len(path) - 1):
            maze.carve(path[i], dirpath[i])
            if step:
                print(maze)
                sleep(0.3)
            unknown.remove(path[i])

    return maze


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python wilson.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2]), True))
