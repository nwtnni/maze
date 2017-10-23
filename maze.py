from enum import IntEnum
from random import choice, randint

class D(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

def opp(d): return (d + 2) % 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self, arr): return arr[y][x]

    def adj(self, d):
        if   d == D.N: return Point(self.x, self.y + 1)
        elif d == D.E: return Point(self.x + 1, self.y)
        elif d == D.S: return Point(self.x, self.y - 1)
        elif d == D.W: return Point(self.x - 1, self.y)
    def __repr__(self): return "(" + str(self.x) + ", " + str(self.y) + ")"

class Tile:
    def __init__(self):
        self.config = "1111"
    
    def get(self, d): 
        return self.config[d] == "1"

    def set(self, d, up): 
        flag = "1" if up else "0"
        self.config = self.config[:d] + flag + self.config[d+1:]
        return self
        
class Maze: 
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.maze = [[Tile() for x in range(w)] for y in range(h)]

    def get(self, p, d):
        a = p.get(self.maze)
        b = p.adj(d).get(self.maze)
        return (a, b)

    def set(self, p, d, wall):
        a, b = get(self, p, d)
        a.set(d, wall)       
        b.set(opp(d), wall)
        return self

    def is_wall(self, p, d):
        a, b = get(self, p, d)
        return a.get(d) and b.get(opp(d))

    def create(self, p, d):
        set(self, p, d, True)

    def carve(self, p, d):
        set(self, p, d, False)

    def in_bounds(self, p):
        return (p.x >= 0 and p.x < self.w and p.y >= 0 and p.y < self.w)

    def rand_neighbor(self, p):
        while True: 
            a = p.adj(choice(list(D)))
            if self.in_bounds(a): break
        return a

    def rand_point(self):
        while True:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
            p = Point(x, y)
            if self.in_bounds(p): break
        return p

if __name__ == "__main__":
    m = Maze(10, 10) 

    for i in range(20):
        p = m.rand_point()
        print(p)
        print("\t" + str(m.rand_neighbor(p)))
