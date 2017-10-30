from maze import *
from sys import argv
from time import sleep
from random import shuffle

def generate(w, h, step=False):
    maze = Maze(w, h)
    ids = {Point(x, y) : str(x) + " " + str(y) for x in range(w) for y in range(h)}
    visit = [(Point(x, y), d) for x in range(w) for y in range(h) for d in maze.neighbors(Point(x, y))]
    shuffle(visit)

    for n, d in visit:
        f = ids[n.adj(d)] 
        t = ids[n]
        if f == t: continue
        for k, v in ids.items():
            if v == f: ids[k] = t
        maze.carve(n, d)
        if step:
            print(maze)
            sleep(0.3)
    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python kruskal.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2]), True))
