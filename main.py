from astar import AStar


def main():
    rows, cols = 10, 10
    start, goal = (0, 0), (6, 3)
    astar = AStar(start, goal,rows, cols)
    astar.run()

if __name__ == "__main__":
    main()
