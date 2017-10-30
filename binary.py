from sys import argv
from time import sleep
from random import choice
from maze import *

def generate(w, h, step=True):
    maze = Maze(w, h)
    
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
            
            if col == x: maze.carve(p, vd)
            elif row == y: maze.carve(p, hd)
            else: maze.carve(p, choice(d))
            if step: 
                print(maze)
                sleep(0.30)
    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python binary.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2])))
