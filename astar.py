import heapq
import math
import time
import random
from typing import Callable, Tuple

    #    start     Vertex     goal
    #     |----------|---------|
    #         g(n)      h(n)
    #     |--------------------|
    #           g(n) + h(n)

class Vertex:
    def __init__(self, x, y, astar):
        self.x = x
        self.y = y
        self.astar = astar
    
    def __lt__(self, other):
        self_g = self.astar.g_score[self]
        other_g = self.astar.g_score[other]
        print("a", self_g, other_g)
        return self_g < other_g  

    def print_coordinates(self) -> None:
        print(f"coordinates ", self.x, self.y)

class PriorityQueue:
    def __init__(self) -> None:
        self.heap = []
    
    def push(self, priority: float, item: Vertex):
        entry = (priority, item)
        heapq.heappush(self.heap, entry)

    def pop(self) -> Vertex:
        while self.heap:
            priority, entry = heapq.heappop(self.heap)
            return entry
    
    def remove(self, vertex: Vertex):
        new_heap = [(priority, entry) for priority, entry in self.heap if vertex.x != entry.x or vertex.y != entry.y]
        heapq.heapify(new_heap)
        self.heap = new_heap

class AStar:
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], rows, cols) -> None:        
        self.start = Vertex(start[0], start[1], self)
        self.goal = Vertex(goal[0], goal[1], self)
        self.open_set = PriorityQueue()
        
        self.came_from = {}
        self.neighbors = {}
        self.g_score = {}
        self.h_score = {}
        self.f_score = {}

        self.grid = self.init_grid(rows, cols)

    def init_grid(self, rows, cols):
        return [[0 for col in range(cols)] for row in range(rows)]

    def reconstruct(self, current):
        total_path = [current]
        while current in self.came_from.keys():
            current = self.came_from[current]
            total_path = [current] + total_path 
        coordinate_pairs = [(vertex.x, vertex.y) for vertex in total_path]
        return coordinate_pairs

    def calculate_d(self, current, successor) -> None:
        dx = abs(successor.x - current.x)
        dy = abs(successor.y - current.y)
        
        if dx == 1 and dy == 0:
            return 1
        elif dx == 0 and dy == 1:
            return 1
        else:
            return math.sqrt(dx**2 + dy**2)

    def calculate_h(self, succesor) -> None: 
        self.h_score[succesor] = math.sqrt(2) * \
        min(abs(succesor.x - self.goal.x), abs(succesor.y - self.goal.y)) + \
        max(abs(succesor.x - self.goal.x), abs(succesor.y - self.goal.y)) - \
        min(abs(succesor.x - self.goal.x), abs(succesor.y - self.goal.y))
    
    def get_neighbors(self, vertex: Vertex) -> None:
        self.neighbors[vertex] = []
        y = vertex.y - 1
        if(y>=0):
            successor = Vertex(vertex.x, y, self)
            self.neighbors[vertex].append(successor)

        x = vertex.x + 1
        if(x < len(self.grid[0])):
            successor = Vertex(x, vertex.y, self)
            self.neighbors[vertex].append(successor)

        y = vertex.y + 1
        if(y < len(self.grid)):
            successor = Vertex(vertex.x, y, self)
            self.neighbors[vertex].append(successor)
    
        x = vertex.x - 1
        if(x >= 0):
            successor = Vertex(x, vertex.y, self)
            self.neighbors[vertex].append(successor)
        
        x = vertex.x + 1
        y = vertex.y - 1
        if(y >= 0 and x < len(self.grid[0])):
            successor = Vertex(x, y, self)
            self.neighbors[vertex].append(successor)
        
        x = vertex.x - 1
        y = vertex.y - 1
        if(y >= 0 and x >= 0):
            successor = Vertex(x, y, self)
            self.neighbors[vertex].append(successor)

        x = vertex.x + 1
        y = vertex.y + 1
        if(y < len(self.grid) and x < len(self.grid[0])):
            successor = Vertex(x, y, self)
            self.neighbors[vertex].append(successor)

        x = vertex.x - 1
        y = vertex.y + 1
        if(y < len(self.grid) and x >= 0):
            successor = Vertex(x, y, self)
            self.neighbors[vertex].append(successor)

    def run(self) -> None:
        self.open_set.push(0, self.start)
        self.g_score[self.start] = 0
        self.h_score[self.start] = 0
        self.f_score[self.start] = self.h_score[self.start]

        while len(self.open_set.heap):
            current = self.open_set.pop()
            print("\n visiting ", current.x, current.y, self.g_score[current])
            # time.sleep(1)
            if (current.x == self.goal.x and current.y == self.goal.y):
                print("Found it!")
                # for v in self.closed:
                #     print("\n visited", v)
                return self.reconstruct(current)
            
            self.open_set.remove(current)
            
            self.get_neighbors(current)
            
            print(len(self.neighbors[current]), "neighbors")
            
            for successor in self.neighbors[current]:
                tenative_g = self.g_score[current] + self.calculate_d(current, successor)
                successor_g  = self.g_score[successor] if successor in self.g_score else math.inf
                if tenative_g < successor_g:
                    self.calculate_h(successor)
                    self.came_from[successor] = current
                    self.g_score[successor] = tenative_g
                    self.f_score[successor] = tenative_g + self.h_score[successor]
                    if successor not in self.open_set.heap:
                        self.open_set.push(self.g_score[successor], successor)
    
class AStarBlocked(AStar):
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], rows, cols) -> None:
        super().__init__(start, goal, rows, cols)
        self.blocked = self.init_blocked(rows, cols)

    def init_blocked(self, rows, cols):
        blocked = []
        count = 0
        blocked_cell_count = 0
        if rows == cols:
            blocked_cell_count = (rows - 1) * (cols - 1) // 3
            print (blocked_cell_count)
        else:
            large = max(rows, cols)
            small = min(rows, cols)
            blocked_cell_count = (large - 1) * (small) // 3

        while count < blocked_cell_count:
            col = random.randint(0, cols - 2)
            row = random.randint(0, rows - 2)
            
            if (col, row) not in blocked:
                blocked.append((col, row))
                count += 1
        return blocked
      
    
    def init_grid(self, rows, cols):
        return [[0 for col in range(cols)] for row in range(rows)]
    
    def get_neighbors(self, vertex: Vertex) -> None:
        def is_blocked(x, y) -> bool:
            return (x, y) in self.blocked
        
        self.neighbors[vertex] = []
        self_blocked = is_blocked(vertex.x, vertex.y)
        
        x = vertex.x - 1
        y = vertex.y - 1
        north_west_successor = None
        north_west_blocked = is_blocked(x, y)
        if y >= 0 and x >= 0 and not north_west_blocked:
            north_west_successor = Vertex(x, y)
            north_west_successor.calculate_d(vertex, north_west_successor)
            north_west_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(north_west_successor)
        
        x = vertex.x
        y = vertex.y - 1
        north_successor = None
        north_blocked = is_blocked(x, y) if y > 0 else True
        if y >= 0 and not (north_west_blocked and north_blocked) and x < len(self.grid[0]) - 1:
            north_successor = Vertex(x, y)
            north_successor.calculate_d(vertex, north_successor)
            north_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(north_successor)

        x = vertex.x + 1
        y = vertex.y
        east_successor = None
        if x < len(self.grid[0]) and not (self_blocked and north_blocked) and not (north_blocked and y == len(self.grid) -1):
            east_successor = Vertex(x, y)
            east_successor.calculate_d(vertex, east_successor)
            east_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(east_successor)

        x = vertex.x - 1
        y = vertex.y
        west_successor = None
        west_blocked = is_blocked(x, y)
        if x >= 0 and (not north_west_blocked and y < len(self.grid) - 1) and not (west_blocked and north_west_blocked):
            west_successor = Vertex(x, y)
            west_successor.calculate_d(vertex, west_successor)
            west_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(west_successor)
        
        x = vertex.x
        y = vertex.y + 1
        south_successor = None
        if y < len(self.grid) and not (self_blocked and west_blocked):
            south_successor = Vertex(x, y)
            south_successor.calculate_d(vertex, south_successor)
            south_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(south_successor)
        
        x = vertex.x + 1
        y = vertex.y - 1
        north_east_successor = None
        if y >= 0 and x < len(self.grid[0]) and not north_blocked:
            north_east_successor = Vertex(x, y)
            north_east_successor.calculate_d(vertex, north_east_successor)
            north_east_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(north_east_successor)

        x = vertex.x + 1
        y = vertex.y + 1
        south_east_successor = None
        if y < len(self.grid) and x < len(self.grid[0]) and not self_blocked:
            south_east_successor = Vertex(x, y)
            south_east_successor.calculate_d(vertex, south_east_successor)
            south_east_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(south_east_successor)
        
        x = vertex.x - 1
        y = vertex.y + 1
        south_west_successor = None
        if y < len(self.grid) and x >= 0 and not west_blocked:
            south_west_successor = Vertex(x, y)
            south_west_successor.calculate_d(vertex, south_west_successor)
            south_west_successor.calculate_h(self.goal)
            self.neighbors[vertex].append(south_west_successor)

        print("blocked ", self.blocked)
        # print("is self blocked", self_blocked)
        
        for vertex in self.neighbors[vertex]:
            print(vertex.x, vertex.y, vertex.g)

    def run(self):
        coordinate_pairs = super().run()
        return (coordinate_pairs, self.blocked)