from sys import argv
from time import sleep
from random import choice
from maze import *

def generate(w, h, step=False):
    maze = Maze(w, h)
    
    # Directional bias
    hd = choice([D.E, D.W])
    vd = choice([D.S, D.N])
    d = [hd, vd]

    rows = range(h) if vd == D.S else range(h - 1, -1, -1)
    cols = range(w) if hd == D.E else range(w - 1, -1, -1)

    for row in rows[:-1]:
        run = []
        for col in cols:
            run.append(col) 
            if col == cols[-1] or choice(d) == vd:
                maze.carve(Point(choice(run), row), vd)
                run.clear()
            else:
                maze.carve(Point(col, row), hd)
            if step:
                print(maze)
                sleep(0.3)
    for col in cols:
        maze.carve(Point(col, rows[-1]), hd)
        if step:
            print(maze)
            sleep(0.3)

    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python sidewinder.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2]), True))
