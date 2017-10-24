from enum import IntEnum
from random import randint, shuffle

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

    def inside(self, arr): return arr[self.y][self.x]

    def adj(self, d):
        if   d == D.N: return Point(self.x, self.y - 1)
        elif d == D.E: return Point(self.x + 1, self.y)
        elif d == D.S: return Point(self.x, self.y + 1)
        elif d == D.W: return Point(self.x - 1, self.y)

    def __repr__(self): return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if type(other) is type(self):
            return other.x == self.x and other.y == self.y
        return False
    
    def __ne__(self, other):
        return not __eq__(self, other)

    def __hash__(self):
        return self.x * self.y

class Tile:
    def __init__(self):
        self.config = "1111"
    
    def is_wall(self, d): 
        return self.config[d] == "1"

    def set_wall(self, d, up): 
        flag = "1" if up else "0"
        self.config = self.config[:d] + flag + self.config[d+1:]
        return self
        
class Maze: 
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.maze = [[Tile() for x in range(w)] for y in range(h)]

    def get_adj(self, p, d):
        a = p.inside(self.maze)
        b = p.adj(d).inside(self.maze)
        return (a, b)

    def set_wall(self, p, d, wall):
        if self.valid(p) and self.valid(p.adj(d)):
            a, b = self.get_adj(p, d)
            a.set_wall(d, wall)       
            b.set_wall(opp(d), wall)
        return self

    def is_wall(self, p, d):
        a, b = self.get_adj(p, d)
        return a.is_wall(d) and b.is_wall(opp(d))

    def create(self, p, d):
        self.set_wall(p, d, True)
        return self

    def carve(self, p, d):
        self.set_wall(p, d, False)
        return self

    def valid(self, p):
        return (p.x >= 0 and p.x < self.w and p.y >= 0 and p.y < self.h)

    def neighbors(self, p):
        l = [d for d in list(D) if self.valid(p.adj(d))]
        shuffle(l)
        return l

    def rand_point(self):
        while True:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
            p = Point(x, y)
            if self.valid(p): break
        return p

    def __repr__(self):
        line = "-----".join(["+" for tile in range(self.w + 1)]) + "\n"
        rep = line
        for row in self.maze: 
            v = "     ".join(["|" if tile.is_wall(D.W) else " " for tile in row]) + "     |\n"
            h = "+" + "+".join(["-----" if tile.is_wall(D.S) else "     " for tile in row]) + "+\n"
            rep = rep + v*2 + h
        return rep
