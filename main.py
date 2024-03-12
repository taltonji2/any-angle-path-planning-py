from astar import AStar, AStarBlocked
def main():
    rows, cols = 4, 4
    start, goal = (2, 2), (0, 0)
    astar = AStarBlocked(start, goal, rows, cols)
    astar.run()

if __name__ == "__main__":
    main()