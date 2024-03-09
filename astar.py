import heapq
import math
import time
from typing import Callable, Tuple

    #    start     Vertex     goal
    #     |----------|---------|
    #         g(n)      h(n)
    #     |--------------------|
    #           g(n) + h(n)

class Vertex:
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = parent if parent is not None else self
        
    def calculate_g(self, current, successor) -> None:
        if (successor.x < current.x and successor.y == current.y): #Successor is to the left
            self.g = current.g + 1
        if (successor.x > current.x and successor.y == current.y): #Successor is to the right
            self.g = current.g + 1
        if (successor.x == current.x and successor.y < current.y): #Successor is above
            self.g = current.g + 1
        if (successor.x == current.x and successor.y > current.y): #Successor is under
            self.g = current.g + 1
        self.g = current.g + math.sqrt(2); #diagonal

    def calculate_h(self, vertex) -> None: 
        self.h = math.sqrt(2) * \
        min(abs(vertex.x - self.goal.x), abs(vertex.y - self.goal.y)) + \
        max(abs(vertex.x - self.goal.x), abs(vertex.y - self.goal.y)) - \
        min(abs(vertex.x - self.goal.x), abs(vertex.y - self.goal.y))
    
    def __lt__(self, other):
        return self.g  < other.g

    def print_coordinates(self) -> None:
        print(f"coordinates ", self.x, self.y)

class PriorityQueue:
    def __init__(self) -> None:
        self.heap = []
        self.removed_set = set()
    
    def push(self, priority: float, item: Vertex):
        entry = [priority, item]
        heapq.heappush(self.heap, entry)

    def pop(self) -> Vertex:
        while self.heap:
            priority, entry = heapq.heappop(self.heap)
            if entry not in self.removed_set:
                return entry
    
    def remove(self, vertex: Vertex):
        new_heap = [(priority, entry) for priority, entry in self.heap if vertex.x != entry[1].x or vertex.y != entry[1].y]
        heapq.heapify(new_heap)
        self.heap = new_heap

    def remove_if(self, condition: Callable[[Vertex], bool]):
        items_to_remove = [entry[1] for entry in self.heap if condition(entry[1])]
        self.removed_set.update(items_to_remove)
        self.heap = [entry for entry in self.heap if entry[1] not in self.removed_set]
        heapq.heapify(self.heap)

class AStar:
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], rows, cols) -> None:        
        self.start = Vertex(x=start[0], y=start[1], g=0, h=0)
        self.goal = Vertex(x=goal[0], y=goal[1], g=float('inf'), h=0)
        self.fringe = PriorityQueue()
        self.closed = []
        self.visited = {}
        self.neighbors = {}
        self.grid = self.init_grid(rows, cols)

    def init_grid(self, rows, cols):
        return [[0 for col in range(cols)] for row in range(rows)]

    def threshold_float_comparison(self, f_a, f_b) -> None:
        THRESHOLD = .0001
        if abs(f_a - f_b) < THRESHOLD:
            # equality
            return True
        else:
            return False

    def get_neighbors(self, vertex: Vertex) -> None:
        self.neighbors[vertex] = []
        y = vertex.y - 1
        if(y>=0):
            successor = Vertex(vertex.x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)     
            self.neighbors[vertex].append(successor)

        x = vertex.x + 1
        if(x < len(self.grid[0])):
            successor = Vertex(x, vertex.y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)

        y = vertex.y + 1
        if(y < len(self.grid)):
            successor = Vertex(vertex.x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)
    
        x = vertex.x - 1
        if(x >= 0):
            successor = Vertex(x, vertex.y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)
        
        x = vertex.x + 1
        y = vertex.y - 1
        if(y >= 0 and x < len(self.grid[0])):
            successor = Vertex(x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)
        
        x = vertex.x - 1
        y = vertex.y - 1
        if(y >= 0 and x >= 0):
            successor = Vertex(x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)

        x = vertex.x + 1
        y = vertex.y + 1
        if(y < len(self.grid) and x < len(self.grid[0])):
            successor = Vertex(x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)

        x = vertex.x - 1
        y = vertex.y + 1
        if(y < len(self.grid) and x >= 0):
            successor = Vertex(x, y)
            successor.calculate_g(vertex, successor)
            successor.calculate_h(vertex, successor)
            self.neighbors[vertex].append(successor)

    def tie_break(self, successor):
        if not self.threshold_float_comparison(successor.g, self.fringe.heap[0].g):
            self.fringe.heap.remove(successor)

    def run(self) -> None:
        self.start.h = 0
        self.fringe.push(0, self.start)
        while len(self.fringe.heap):
            current = self.fringe.pop()
            print("\n visiting ", current.x, current.y, current.g)
            time.sleep(1)
            if (current.x == self.goal.x and current.y == self.goal.y):
                self.closed.append(current)
                print("Found it!")
                # for v in self.closed:
                #     print("\n visited", v)
                break
            self.closed.append(current)
            self.fringe.remove_if(lambda n: self.visited[n] == True)
            self.get_neighbors(current)
            print(len(self.neighbors[current]))
            for successor in self.neighbors[current]:
                if successor not in self.closed:
                    verticies = [entry[1] for entry in self.fringe.heap]
                    coordinate_pairs = [(verticy.x, verticy.y) for verticy in verticies]
                    if (successor.x, successor.y) in coordinate_pairs:
                        self.fringe.heap.remove(successor)
                    self.visited[successor] = True
                    self.fringe.push(priority=successor.g + successor.h, item=successor)                 
                    if len(self.fringe.heap) and self.fringe.heap[0] == successor and self.threshold_float_comparison(successor.f, self.fringe.heap[0].f):
                        self.tie_break(successor)
                    # print(f"Added ( {successor.x}, {successor.y} ) to fringe")
        return self.closed