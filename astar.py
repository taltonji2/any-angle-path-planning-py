import heapq
import math
import time
import random
from typing import Callable, Tuple

    #    start     Vertex     goal
    #     |----------|---------|
    #         g(n)      h(n)
    #     |--------------------|
    #       f(n) = g(n) + h(n)

class Vertex:
    def __init__(self, x, y, astar):
        self.x = x
        self.y = y
        self.astar = astar
    
    def __lt__(self, other):
        self_g = self.astar.g_score[self]
        other_g = self.astar.g_score[other]
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

    def calculate_d(self, current, neighbor) -> None:
        dx = abs(neighbor.x - current.x)
        dy = abs(neighbor.y - current.y)
        
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
            neighbor = Vertex(vertex.x, y, self)
            self.neighbors[vertex].append(neighbor)

        x = vertex.x + 1
        if(x < len(self.grid[0])):
            neighbor = Vertex(x, vertex.y, self)
            self.neighbors[vertex].append(neighbor)

        y = vertex.y + 1
        if(y < len(self.grid)):
            neighbor = Vertex(vertex.x, y, self)
            self.neighbors[vertex].append(neighbor)
    
        x = vertex.x - 1
        if(x >= 0):
            neighbor = Vertex(x, vertex.y, self)
            self.neighbors[vertex].append(neighbor)
        
        x = vertex.x + 1
        y = vertex.y - 1
        if(y >= 0 and x < len(self.grid[0])):
            neighbor = Vertex(x, y, self)
            self.neighbors[vertex].append(neighbor)
        
        x = vertex.x - 1
        y = vertex.y - 1
        if(y >= 0 and x >= 0):
            neighbor = Vertex(x, y, self)
            self.neighbors[vertex].append(neighbor)

        x = vertex.x + 1
        y = vertex.y + 1
        if(y < len(self.grid) and x < len(self.grid[0])):
            neighbor = Vertex(x, y, self)
            self.neighbors[vertex].append(neighbor)

        x = vertex.x - 1
        y = vertex.y + 1
        if(y < len(self.grid) and x >= 0):
            neighbor = Vertex(x, y, self)
            self.neighbors[vertex].append(neighbor)

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
                path_coordinate_pairs = self.reconstruct(current)
                print(path_coordinate_pairs)
                return path_coordinate_pairs
            
            self.open_set.remove(current)
            
            self.get_neighbors(current)
            
            print(f"has {len(self.neighbors[current])}, neighbors")
            if self.g_score[current] > 500 : 
                print("No path")
                return

            for neighbor in self.neighbors[current]:
                tenative_g = self.g_score[current] + self.calculate_d(current, neighbor)
                neighbor_g  = self.g_score[neighbor] if neighbor in self.g_score else math.inf
        
                if tenative_g < neighbor_g:
                    self.calculate_h(neighbor)
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tenative_g
                    self.f_score[neighbor] = tenative_g + self.h_score[neighbor]
        
                    print(f"{neighbor.x} {neighbor.y} g_score {tenative_g} h_score {self.h_score[neighbor]}")
        
                    if neighbor not in self.open_set.heap:
                        self.open_set.push(self.f_score[neighbor], neighbor)
    
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
        print("blocked ", blocked)
        return blocked
      
    
    def init_grid(self, rows, cols):
        return [[0 for col in range(cols)] for row in range(rows)]
    
    def get_neighbors(self, vertex: Vertex) -> None:
        def is_blocked(x, y) -> bool:
            return (x, y) in self.blocked
        
        self.neighbors[vertex] = []

        x = vertex.x - 1
        y = vertex.y - 1
        north_west_neighbor = Vertex(x,y,self)

        x = vertex.x
        y = vertex.y - 1
        north_neighbor = Vertex(x,y,self)

        x = vertex.x + 1
        y = vertex.y
        east_neighbor = Vertex(x,y,self)

        x = vertex.x - 1
        y = vertex.y
        west_neighbor = Vertex(x,y,self)

        x = vertex.x
        y = vertex.y + 1
        south_neighbor = Vertex(x,y,self)

        x = vertex.x + 1
        y = vertex.y - 1
        north_east_neighbor = Vertex(x,y,self)

        x = vertex.x + 1
        y = vertex.y + 1
        south_east_neighbor = Vertex(x,y,self)

        x = vertex.x - 1
        y = vertex.y + 1
        south_west_neighbor = Vertex(x,y,self)
        
        if north_neighbor is not None:
            if vertex.x > 1:
                if not is_blocked(north_neighbor.x, north_neighbor.y) or not is_blocked(vertex.x, vertex.y):
                    if is_blocked(north_west_neighbor.x, north_west_neighbor.y):
                        self.neighbors[vertex].append(north_neighbor)
                    elif is_blocked(north_west_neighbor.x, north_west_neighbor.y) and not is_blocked(north_neighbor.x, north_neighbor.y):
                        self.neighbors[vertex].append(north_neighbor)
                elif north_neighbor.x == 0:
                    self.neighbors[vertex].append(north_neighbor)
                elif not is_blocked(north_west_neighbor.x, north_west_neighbor.y) and not is_blocked(west_neighbor.x, west_neighbor.y):
                    self.neighbors[vertex].append(north_neighbor)
            elif not is_blocked(north_neighbor.x, north_neighbor.y) and north_neighbor.y >= 0 and not is_blocked(vertex.x, vertex.y):
                self.neighbors[vertex].append(north_neighbor)

        if south_neighbor.y < len(self.grid):
            if vertex.x == 0 and not is_blocked(vertex.x, vertex.y):
                self.neighbors[vertex].append(south_neighbor)
            elif vertex.x != 0 and (not is_blocked(west_neighbor.x, west_neighbor.y) or not is_blocked(vertex.x, vertex.y)):
                self.neighbors[vertex].append(south_neighbor)
            
        if east_neighbor.x < len(self.grid):
            if east_neighbor.y != 0:
                if not is_blocked(north_neighbor.x, north_neighbor.y) or not is_blocked(vertex.x, vertex.y):
                    self.neighbors[vertex].append(east_neighbor)
            elif not is_blocked(vertex.x, vertex.y):
                self.neighbors[vertex].append(east_neighbor)

        if west_neighbor.x >= 0:
            if north_west_neighbor.x >= 0 and north_west_neighbor.y >= 0:
                if not is_blocked(west_neighbor.x, west_neighbor.y) or not is_blocked(north_west_neighbor.x, north_west_neighbor.y):
                    self.neighbors[vertex].append(west_neighbor)
            elif not is_blocked(west_neighbor.x, west_neighbor.y):
                self.neighbors[vertex].append(west_neighbor)

        if north_east_neighbor.x < len(self.grid[0]) and north_east_neighbor.y >= 0:
            if not is_blocked(north_neighbor.x, north_neighbor.y):
                self.neighbors[vertex].append(north_east_neighbor)

        if north_west_neighbor.x >= 0 and north_west_neighbor.y >= 0 and not is_blocked(north_west_neighbor.x, north_west_neighbor.y):
            self.neighbors[vertex].append(north_west_neighbor)

        if south_east_neighbor.x < len(self.grid[0]) and south_east_neighbor.y < len(self.grid) and not is_blocked(vertex.x, vertex.y):
            self.neighbors[vertex].append(south_east_neighbor)

        if south_west_neighbor.x >= 0 and south_west_neighbor.y < len(self.grid) and not is_blocked(west_neighbor.x, west_neighbor.y):
            self.neighbors[vertex].append(south_west_neighbor)
        
    def run(self):
        coordinate_pairs = super().run()
        return (coordinate_pairs, self.blocked)