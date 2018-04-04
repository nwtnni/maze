from maze import Point, D
from collections import defaultdict
from matplotlib import collections as mc
from dfs import generate
import matplotlib.pyplot as plt
import matplotlib.patches as p


def search(maze, s):
    distance = defaultdict(lambda: float("inf"))
    distance[s] = 0
    retrace = {s: None}
    frontier = [(0, s)]
    visited = set([])

    while len(frontier) > 0:
        frontier = sorted(frontier, key=lambda v: -v[0])
        d, p = frontier.pop()

        if p in visited:
            continue
        else:
            visited.add(p)

        for dir in maze.reachable(p):
            n = p.adj(dir)

            if n in visited:
                continue

            if d + 1 < distance[n]:
                distance[n] = d + 1
                retrace[n] = p
            frontier.append((distance[n], n))
    return (distance, retrace)


def solve(maze, s, f):
    if not maze.valid(s) or not maze.valid(f):
        return False

    d, r = search(maze, s)
    n = f
    path = [n]
    while r[n] is not None:
        path.append(r[n])
        n = r[n]
    path.reverse()
    return(path)


def plot(lines, save=False, path="maze"):
    f, ax = plt.subplots(figsize=(10, 10))
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    for lc in lines:
        ax.add_collection(lc)
    ax.autoscale()

    if save:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()


def outline(maze):
    lines = [[(0, 0), (maze.w, 0)]]
    for y in range(maze.h):
        v = [[(x, y), (x, y + 1)] for x in range(maze.w) if maze.is_wall(Point(x, y), D.W)]
        v.append([(maze.w, y), (maze.w, y + 1)])
        h = [[(x, y + 1), (x + 1, y + 1)] for x in range(maze.w) if maze.is_wall(Point(x, y), D.S)]
        lines.extend(v)
        lines.extend(h)
    return mc.LineCollection(lines, colors="blue")


def solution(maze, s, f):
    path = solve(maze, s, f)
    lines = []
    for i in range(len(path) - 1):
        x1 = path[i].x + 0.5
        y1 = path[i].y + 0.5
        x2 = path[i+1].x + 0.5
        y2 = path[i+1].y + 0.5
        lines.append([(x1, y1), (x2, y2)])
    return mc.LineCollection(lines, colors="orange")


def heat(maze, s):
    patches = []
    colors = []
    d, r = search(maze, s)
    scale = max(d.values()) * 1.5

    for y in range(maze.h):
        for x in range(maze.w):
            patches.append(p.Rectangle((x, y), 1, 1))
            colors.append((0, 0, 1, d[Point(x, y)]/scale))
    return mc.PatchCollection(patches, facecolors=colors)


def draw(maze):
    plot([outline(maze)])


def draw_sol(maze, s, f):
    plot([outline(maze), solution(maze, s, f)])


def draw_heat(maze, s):
    plot([outline(maze), heat(maze, s)])


def save_outline(maze, path):
    plot([outline(maze)], True, path)


def save_sol(maze, s, f, path):
    plot([outline(maze), solution(maze, s, f)], True, path)


def save_heat(maze, s, path):
    plot([outline(maze), heat(maze, s)], True, path)


if __name__ == "__main__":
    m = generate(100, 100)
    draw_heat(m, Point(50, 50))
