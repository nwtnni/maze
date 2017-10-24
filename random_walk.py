from maze import *
from sys import argv

def generate(w, h):
    maze = Maze(w, h)
    n = maze.rand_point()
    visited = set([n])

    while len(visited) < w * h:
        dirs = maze.neighbors(n)
        next = n.adj(dirs[0])
        if next not in visited:
            visited.add(next)
            maze.carve(n, dirs[0])
        n = next
    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python random_walk.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2])))
