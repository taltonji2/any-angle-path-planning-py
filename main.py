from astar import AStar, AStarBlocked
from grid_renderer import GridRenderer

def main():
    rows, cols = 4, 4
    start, goal = (0, 0), (3, 3)
    astar = AStarBlocked(start, goal, rows, cols)
    (traversal, blocked) = astar.run()
    grid_renderer = GridRenderer(grid_size=rows)
    print(traversal)
    print(blocked)
    grid_renderer.run(traversal, blocked) 

if __name__ == "__main__":
    main()