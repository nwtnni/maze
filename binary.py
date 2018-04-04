from random import choice
from maze import Maze, D, Point


def generate(w, h):
    maze = Maze(w, h)
    yield maze

    # Carving directions
    hd = choice([D.W, D.E])
    vd = choice([D.N, D.S])
    d = [hd, vd]

    # Fill in opposite wall
    x = 0 if hd == D.W else w - 1
    y = 0 if vd == D.N else h - 1

    for row in range(h):
        for col in range(w):
            p = Point(col, row)
            if col == x:
                maze.carve(p, vd)
            elif row == y:
                maze.carve(p, hd)
            else:
                maze.carve(p, choice(d))
            yield maze
