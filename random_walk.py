from maze import Maze


def generate(w, h):
    maze = Maze(w, h)
    yield maze
    n = maze.rand_point()
    visited = set([n])

    while len(visited) < w * h:
        dirs = maze.neighbors(n)
        next = n.adj(dirs[0])
        if next not in visited:
            visited.add(next)
            maze.carve(n, dirs[0])
            yield maze
        n = next
