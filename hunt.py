from maze import Point, Maze
from sys import argv
from time import sleep


def hunt(maze, visited, step):
    for y in range(maze.h):
        for x in range(maze.w):
            n = Point(x, y)
            adj = [d for d in maze.neighbors(n) if n.adj(d) in visited]
            if n not in visited and len(adj) > 0:
                maze.carve(n, adj[0])
                visited.add(n)
                if step:
                    print(maze)
                    sleep(0.30)
                return n
    return None


def kill(maze, n, visited, step):
    while True:
        dirs = maze.neighbors(n)
        free = [d for d in dirs if n.adj(d) not in visited]
        next = n.adj(dirs[0])

        if len(free) == 0:
            return

        elif next not in visited:
            visited.add(next)
            maze.carve(n, dirs[0])
            if step:
                print(maze)
                sleep(0.30)
        n = next


def generate(w, h, step=False):
    maze = Maze(w, h)
    n = maze.rand_point()
    visited = set([n])

    while True:
        kill(maze, n, visited, step)
        h = hunt(maze, visited, step)
        if h is None:
            break
        else:
            n = h
    return maze


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python hunt.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2]), True))
