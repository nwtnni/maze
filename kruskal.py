from maze import Point, Maze
from random import shuffle


def generate(w, h):
    maze = Maze(w, h)
    yield maze
    ids = {Point(x, y): str(x) + " " + str(y) for x in range(w) for y in range(h)}
    visit = [(Point(x, y), d) for x in range(w) for y in range(h) for d in maze.neighbors(Point(x, y))]
    shuffle(visit)

    for n, d in visit:
        f = ids[n.adj(d)]
        t = ids[n]

        if f == t:
            continue

        for k, v in ids.items():
            if v == f:
                ids[k] = t

        maze.carve(n, d)
        yield maze
