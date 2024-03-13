from astar import AStar, AStarBlocked
from grid_renderer import GridRenderer

def main():
    rows, cols = 4, 4
    start, goal = (2, 2), (0, 0)
    astar = AStarBlocked(start, goal, rows, cols)
    traversal = astar.run()
    grid_renderer = GridRenderer()
    grid_renderer.run(traversal) 

if __name__ == "__main__":
    main()