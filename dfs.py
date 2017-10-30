from maze import Maze
from sys import argv
from time import sleep

def generate(w, h, step=False):
    maze = Maze(w, h)
    start = maze.rand_point()
    stack = [start]
    visited = set([start])
    
    while len(stack) > 0:
        n = stack[-1]

        for d in maze.neighbors(n):
            m = n.adj(d)
            if m not in visited: 
                maze.carve(n, d)
                stack.append(m)
                visited.add(m)
                if step:
                    print(maze)
                    sleep(0.30)
                break
        else:
            stack.pop()
    return maze

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: dfs.py <WIDTH> <HEIGHT>")
    else:
        print(generate(int(argv[1]), int(argv[2]), True))
