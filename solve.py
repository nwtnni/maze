from maze import *
from queue import PriorityQueue, Queue
from collections import defaultdict
import dfs

def search(maze, s):
    distance = defaultdict(lambda: float("inf"))
    distance[s] = 0
    retrace = {s : False}
    frontier = [(0, s)]
    visited = set([])

    while len(frontier) > 0:
        frontier = sorted(frontier, key=lambda v: -v[0])
        d, p = frontier.pop()

        if p in visited: continue
        else: visited.add(p)

        for d in maze.reachable(p):
            n = p.adj(d)
            if n in visited: continue
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
    while r[n] != False:
        path.append(r[n])
        n = r[n]
    path.reverse()
    return(path)
