from models import Pessoa, Ponto
from typing import List


class Quadtree:

    def __init__(self, width: float, height: float, coords: Ponto, capacity: int):
        self.root = Node(width, height, coords, capacity)
        self.width = width
        self.height = height
        self.coords = coords
        self.capacity = capacity

    def insert(self, element: Pessoa):
        self.root.insert(element)
    def findBetween(self, init: Ponto, end: Ponto):
        return self.root.findBetween(init, end)
    def clear(self):
        self.root = Node(self.width, self.height, self.coords, self.capacity)

class Node:
    e: list[Pessoa]
    children: list['Node']
    def __init__(self, width: float, height: float, coords: Ponto, capacity: int):
        self.e = []
        self.width = width
        self.height = height
        self.capacity = capacity
        self.coords = coords
        self.children = []

    def insert(self, element: Pessoa):
        MIN_SIZE = 1e-5
        if self.width <= MIN_SIZE or self.height <= MIN_SIZE:
            self.e.append(element)
            return
        if len(self.e) < self.capacity and not self.children:
            self.e.append(element)
            return
        if not self.children:
            self.subdivide()
            moved = []
            for el in self.e:
                for child in self.children:
                    if child.contains(el.pos):
                        child.insert(el)
                        moved.append(el)
                        break
            self.e = [el for el in self.e if el not in moved]
        for child in self.children:
            if child.contains(element.pos):
                child.insert(element)
                return
        self.e.append(element)
        
    def contains(self, point: Ponto):
        return (
            point.x >= self.coords.x - self.width / 2 and point.x <= self.coords.x + self.width / 2 and
            point.y >= self.coords.y - self.height / 2 and point.y <= self.coords.y + self.height / 2
        )

    def subdivide(self):
        halfMeasures = [self.width/2, self.height/2]
        offsets = [Ponto(self.coords.x, self.coords.y), Ponto(self.coords.x+halfMeasures[0], self.coords.y), Ponto(self.coords.x+halfMeasures[0], self.coords.y+halfMeasures[1]), Ponto(self.coords.x, self.coords.y+halfMeasures[1])]

        for ponto in offsets:
            self.children.append(Node(halfMeasures[0], halfMeasures[1], ponto, self.capacity))

    def findBetween(self, init: Ponto, end: Ponto):
        found = [];
        if not self.intersects(init, end):
            return found
        if self.children:
            for child in self.children:
                found.extend(child.findBetween(init, end))
        if self.e:
            for element in self.e:
                found.append(element)
        return found
    def intersects(self, init: Ponto, end: Ponto):
        return not ((end.y < self.coords.y) or 
                    (init.y > self.coords.y + self.height) or 
                    (end.x < self.coords.x) or
                    (init.x > self.coords.x + self.width))
        

