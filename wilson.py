from maze import Maze, Point
from random import choice


def prune(path, dirpath):
    last = path[-1]
    if path.count(last) > 1:
        a = path.index(last)
        path = path[:a + 1]
        dirpath = dirpath[:a]
    return (path, dirpath)


def generate(w, h):
    maze = Maze(w, h)
    yield maze
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
            unknown.remove(path[i])
            yield maze
