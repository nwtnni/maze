from maze import *
from sys import argv

def hunt(maze, visited):
    for y in range(maze.h):
        for x in range(maze.w):
            n = Point(x, y)
            adj = [d for d in maze.neighbors(n) if n.adj(d) in visited]
            if n not in visited and len(adj) > 0:
                maze.carve(n, adj[0])
                visited.add(n)
                return n
    return False

def kill(maze, n, visited):
    while True:
        dirs = maze.neighbors(n)
        free = [d for d in dirs if n.adj(d) not in visited]
        next = n.adj(dirs[0]) 
        if len(free) == 0: return            
        elif next not in visited:
            visited.add(next)
            maze.carve(n, dirs[0])
        n = next

def generate(w, h):
    maze = Maze(w, h)
    n = maze.rand_point()
    visited = set([n])

    while True:
        kill(maze, n, visited)
        h = hunt(maze, visited)

        if h == False:
            break
        else:
            n = h

    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python hunt.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2])))
