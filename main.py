import copy
import bisect
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
        #self.manhattan = 0


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
    nodesQueue=[]

    #root of tree
    nodesQueue.append(Node(0,puzzle,None))
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


if __name__ == '__main__':
    currentPuzzle = readFromFile("input.txt")
    moves = bfs(currentPuzzle)
    for state in reversed(moves):
        printPuzzle(state.data)
