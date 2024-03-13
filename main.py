from astar import AStar, AStarBlocked
from grid_renderer import GridRenderer

def main():
    rows, cols = 4, 4
    start, goal = (2, 2), (0, 0)
    astar = AStarBlocked(start, goal, rows, cols)
    (traversal, blocked) = astar.run()
    grid_renderer = GridRenderer()
    print(traversal, blocked)
    grid_renderer.run(traversal, blocked) 

if __name__ == "__main__":
    main()