import copy
import bisect
import timeit

# Global Variables:
solvedPuzzle = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '*'],
]


def readFromFile(file_name):
    array = []
    textFile = open(file_name)
    string = textFile.read()
    lines = string.split("\n")
    for line in lines:
        array.append(line.split("\t"))
    return array


def findStar(puzzle, starLocation):
    for row in range(0, 3):
        for column in range(0, 3):
            if puzzle[row][column] == '*':
                starLocation["row"] = row
                starLocation["col"] = column


# return location of a digit in puzzle
def findLocation(puzzle, number, location):
    for row in range(0, 3):
        for column in range(0, 3):
            if puzzle[row][column] == number:
                location["row"] = row
                location["col"] = column


def printPuzzle(puzzle):
    if puzzle == None:
        return print("None")
    for line in puzzle:
        print("%s\t%s\t%s" % (line[0], line[1], line[2]))
        print("\n")
    print("---------------------------")


def moveUp(puzzle):
    starLocation = {"row": 0, "col": 0}
    findStar(puzzle, starLocation)
    if(starLocation["row"] > 0):
        retPuzzle = copy.deepcopy(puzzle)
        temp = puzzle[starLocation["row"] - 1][starLocation["col"]]
        starLocation["row"] = starLocation["row"] - 1
        retPuzzle[starLocation["row"]][starLocation["col"]] = '*'
        retPuzzle[starLocation["row"] + 1][starLocation["col"]] = temp
        return retPuzzle
    else:
        return None


def moveDown(puzzle):
    starLocation = {"row": 0, "col": 0}
    findStar(puzzle, starLocation)
    if(starLocation["row"] < 2):
        retPuzzle = copy.deepcopy(puzzle)
        temp = puzzle[starLocation["row"] + 1][starLocation["col"]]
        starLocation["row"] = starLocation["row"] + 1
        retPuzzle[starLocation["row"]][starLocation["col"]] = '*'
        retPuzzle[starLocation["row"] - 1][starLocation["col"]] = temp
        return retPuzzle
    else:
        return None


def moveRight(puzzle):
    starLocation = {"row": 0, "col": 0}
    findStar(puzzle, starLocation)
    if(starLocation["col"] < 2):
        retPuzzle = copy.deepcopy(puzzle)
        temp = puzzle[starLocation["row"]][starLocation["col"] + 1]
        starLocation["col"] = starLocation["col"] + 1
        retPuzzle[starLocation["row"]][starLocation["col"]] = '*'
        retPuzzle[starLocation["row"]][starLocation["col"] - 1] = temp
        return retPuzzle
    else:
        return None


def moveLeft(puzzle):
    starLocation = {"row": 0, "col": 0}
    findStar(puzzle, starLocation)
    if(starLocation["col"] > 0):
        retPuzzle = copy.deepcopy(puzzle)
        temp = puzzle[starLocation["row"]][starLocation["col"] - 1]
        starLocation["col"] = starLocation["col"] - 1
        retPuzzle[starLocation["row"]][starLocation["col"]] = '*'
        retPuzzle[starLocation["row"]][starLocation["col"] + 1] = temp
        return retPuzzle
    else:
        return None


def IsSolved(puzzle):
    if(puzzle == solvedPuzzle):
        return True
    else:
        return False


class Node:
    def __init__(self, nodeDepth, nodeData, nodeParent):
        self.depth = nodeDepth
        self.data = nodeData
        self.parent = nodeParent
        self.f = 0

    def compute_f(self):
        if self.data != None:
            self.f = self.depth + h(self.data)


def expandNode(node):
    expandedNodes = []
    retList = []
    expandedNodes.append(Node(node.depth + 1, moveRight(node.data), node))
    expandedNodes.append(Node(node.depth + 1, moveLeft(node.data), node))
    expandedNodes.append(Node(node.depth + 1, moveUp(node.data), node))
    expandedNodes.append(Node(node.depth + 1, moveDown(node.data), node))
    for node in expandedNodes:
        if node.data != None:
            retList.append(node)
    return retList


def bfs(puzzle):
    nodesQueue = []

    # root of tree
    nodesQueue.append(Node(0, puzzle, None))
    while True:
        # no solution
        if len(nodesQueue) == 0:
            return None

        # take the node from front of queue
        node = nodesQueue.pop(0)

        # if node is goal,return moves
        if node.data == solvedPuzzle:
            moves = []
            while node.parent != None:
                moves.append(node)
                node = node.parent
            return moves

        # if node is not goal,expand node
        else:
            nodesQueue.extend(expandNode(node))


def dfs(puzzle, depth=100):

    nodesQueue = []

    # maximum depth to search
    depth_limit = depth

    # append first node to queue
    nodesQueue.append(Node(0, puzzle, None))

    while True:
        # never this state accure
        if(len(nodesQueue) == 0):
            return None

        # pop first node in queue
        node = nodesQueue.pop(0)

        if node.data == solvedPuzzle:

            # an array for store moves
            moves = []

            while node.parent != None:
                moves.append(node)
                node = node.parent
            return moves

        if node.depth < depth_limit:
            # extend node to queue
            """expanded_nodes = expandNode(node)
            expanded_nodes.extend(nodesQueue)
            nodesQueue = expanded_nodes"""
            nodesQueue.extend(expandNode(node))


def ids(puzzle, depth=30):
    for i in range(depth):
        result = dfs(puzzle, i)
        if result != None:
            return result


def a_star(puzzle):
    nodesQueue = []
    nodesQueue.append(Node(0, puzzle, None))
    while True:
        if len(nodesQueue) == 0:
            return None

        # nodesQueue.sort(cmp)

        nodesQueue.sort(key=lambda x: x.f)

        node = nodesQueue.pop(0)

        if node.data == solvedPuzzle:
            moves = []

            while node.parent != None:
                moves.append(node)
                node = node.parent
            return moves
        else:
            nodesQueue.extend(expandNode(node))


def h(puzzle):
    score = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i][j] != solvedPuzzle[i][j]:
                score += 1
    return score


"""def cmp(x, y):
    return (x.depth + h(x.data)) - (y.depth + h(y.data))"""


if __name__ == '__main__':
    start = timeit.default_timer()
    currentPuzzle = readFromFile("input.txt")
    moves = a_star(currentPuzzle)
    #moves = dfs(currentPuzzle, 30)
    #moves = ids(currentPuzzle, 30)
    printPuzzle(currentPuzzle)
    for state in reversed(moves):
        printPuzzle(state.data)
    stop = timeit.default_timer()
    print(stop - start)
