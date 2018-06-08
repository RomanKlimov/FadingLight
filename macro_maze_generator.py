import random


class Box(object):
    def __init__(self):
        self.draw = [True, True, True, True]  # TBRL i.e. Top,Bottom,Left,Right
        self.visited = False


class MazeGenerator:
    def __init__(self):

        self.height = 10
        self.width = 10

        self.stack = []  # The stack of cells used for backtracking
        self.boxes = []
        self.done = False


    # grid = [[Box() for x in range(width)] for y in range(height)]  # A grid of boxes ie rectangular boxes
    # grid[0][0].visited = True
        self.currentX = 0
        self.currentY = 0


    def removeEdge(self, currentX, currentY, nextX, nextY):

        # global grid
        # Remove an edge between current and next box
        xDiff = int(self.currentX - self.nextX)
        if xDiff == 1:
            # Remove current's left and next's right
            self.grid[self.currentX][self.currentY].draw[3] = False
            self.grid[self.nextX][self.nextY].draw[2] = False
        elif xDiff == -1:
            # Remove current's right and next's left
            self.grid[self.currentX][self.currentY].draw[2] = False
            self.grid[self.nextX][self.nextY].draw[3] = False

        yDiff = int(self.currentY - self.nextY)
        if yDiff == 1:
            # Remove current's bottom and next's top
            self.grid[self.currentX][self.currentY].draw[0] = False
            self.grid[self.nextX][self.nextY].draw[1] = False
        elif yDiff == -1:
            # Remove current's top and next's bottom
            self.grid[self.currentX][self.currentY].draw[1] = False
            self.grid[self.nextX][self.nextY].draw[0] = False

        self.boxes.append(self.grid[self.currentX][self.currentY])

    def ret_maze(self, size):
        self.magic(size, size)
        # global currentX, currentY, height, width
        list_for_return = []
        for i in range(self.height):
            list_for_return.append([])
            for j in range(self.width):
                box = []
                box.append(self.grid[i][j].draw[0])
                box.append(self.grid[i][j].draw[2])
                box.append(self.grid[i][j].draw[1])
                box.append(self.grid[i][j].draw[3])
                list_for_return[i] += [box]
        # for row in range(len(list_for_return)):
        #     for col in range(len(list_for_return[row])):
        #         print(list_for_return[row][col], end='')
        #     print()
        return list_for_return


    def genMaze(self):
        # global currentX, currentY
        # Set current box as visited
        self.grid[self.currentX][self.currentY].visited = True
        # Choose a next neighbour that has not yet been visited and set it as the current box
        self.nextX, self.nextY = self.selectNeighbour(self.currentX, self.currentY)
        if self.nextX != -1:
            # Push current cell to stack
            self.stack.append([self.currentX, self.currentY])
            # Remove wall between current and next box and update currentX and currentY
            self.removeEdge(self.currentX, self.currentY, self.nextX, self.nextY)
            self.currentX = self.nextX
            self.currentY = self.nextY
        elif len(self.stack):
            # Remove a cell from stack and make it the current cell
            self.currentX, self.currentY = self.stack.pop()


    def selectNeighbour(self, x, y):
        # global height, width, grid
     # Select a random neighbour out of TBRL that has not been visited and return it
        self.neighbours = []
        # Top neighbour
        if y > 0 and not self.grid[x][y - 1].visited:
            self.neighbours.append([x, y - 1])
        # Bottom neighbour
        if y < self.height - 1 and not self.grid[x][y + 1].visited:
            self.neighbours.append([x, y + 1])
        # Left neighbour
        if x > 0 and not self.grid[x - 1][y].visited:
            self.neighbours.append([x - 1, y])
        # Right neighbour
        if x < self.width - 1 and not self.grid[x + 1][y].visited:
            self.neighbours.append([x + 1, y])

        if not len(self.neighbours):
            return ([-1, -1])
        n = self.neighbours[random.randint(0, len(self.neighbours) - 1)]
        return n


    def magic(self, visota, shirina):
        # global done
        # global height, width, grid

        self.height = visota
        self.width = shirina
        self.grid = [[Box() for x in range(self.width)] for y in range(self.height)]  # A grid of boxes ie rectangular boxes
        self.grid[0][0].visited = True

        while not self.done:
            if (len(self.boxes) == self.width * self.height - 1):
                self.done = True
            self.genMaze()

# a = MazeGenerator()
# b = a.ret_maze(4)
# for i in b:
#     print(i)


# maze = ret_maze(10)
# f = open('maze_txt', 'w')
# for i in maze:
#     f.write(str(i))




