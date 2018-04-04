from maze import Maze


def generate(w, h):
    maze = Maze(w, h)
    start = maze.rand_point()
    stack = [start]
    visited = set([start])
    yield maze

    while len(stack) > 0:
        n = stack[-1]

        for d in maze.neighbors(n):
            m = n.adj(d)
            if m not in visited:
                maze.carve(n, d)
                stack.append(m)
                visited.add(m)
                yield maze
                break
        else:
            stack.pop()
