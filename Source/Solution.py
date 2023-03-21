import random
import heapq
import sys
import copy
import time
import psutil
import os

class AbstractProblem: #here "queens" is also the size (number of rows and columns) of the chess board
    position = []
    queens: int
    
    def __init__(self, queens):
        try:
            self.queens = queens
            self.position = random.sample(range(0,self.queens), queens)
        except ValueError:
            print("Value of Queens must be at least 2")
            sys.exit(0)

    def getPosition(self):
        return self.position
    
    def updatePosition(self, newState: list):
        self.position = newState

    def genQueenMoves(self):
        results = []
        col = 0
        while col < self.queens:
            count = random.randint(0, self.queens-1)
            newMove = (col, count)
            results.append(newMove)
            col += 1
        return results

    def printBoard(self):
        positions = self.getPosition()
        for rows in range (0,self.queens):
            for queens in positions:
                if queens == rows:
                    print(" Q ", end="")
                else: print(" * ",end="")

            print('\n')

    def result(self, queenMove: tuple): #queenMove is a tuple that contains the place of the queen after moving (e.g: ("0","1") means the queen got moved to (0,1)
        new = list(self.position)
        new[queenMove[0]] = queenMove[1]
        return new
    def goalTest(self):
        if not self.position:
            return False
        
        if self.h() != 0:
            return False
        
        return True

    def g(self, cost: int, _parentState, _childState): #a step has the cost of 1
        return cost + 1
            
    def h(self):  #calculate heuristics value
        invalids = 0
        for rows in range (0, self.queens): #checking diagonals and lines
            for cols in range (rows + 1, self.queens):
                if abs(self.position[rows] - self.position[cols]) == abs(rows - cols) or self.position[rows] == self.position[cols]:
                    invalids += 1
        return invalids

    def fitnessFunction(self): #fitness function that reaches the max value of 1 when there are no attacking queens
        return 1 / (1 + self.h())

    def __gt__(self, other):
        return self.fitnessFunction() > other.fitnessFunction()

    def __lt__(self, other):
        return self.fitnessFunction() < other.fitnessFunction()

class StateNode:
    state: AbstractProblem
    heuristics: int
    parent: AbstractProblem
    path_cost: int
    queenMove: tuple
    
    def __init__(self, _state: AbstractProblem, _parent=None, _cost=0, _move=None, _heuristics=0):
        self.state = _state
        self.parent = _parent
        self.path_cost = _cost
        self.queenMove = _move
        self.heuristics = _heuristics

    def genSuccessors(self, problem: AbstractProblem):
        return [self.genChildNode(problem, move) for move in problem.genQueenMoves()]

    def genChildNode(self, problem: AbstractProblem, queenMove: tuple):
        pass
    
    def __lt__(self, otherNode): #overwriting the "<" operator
        pass
    
            
class UCSNode(StateNode):
    def __init__(self, _state: AbstractProblem, _parent=None, _cost=0, _move = None):
        super().__init__(_state, _parent, _cost, _move)

    def genChildNode(self, problem: AbstractProblem, queenMove: tuple):
        childState = copy.copy(self.state)
        childState.updatePosition(problem.result(queenMove))
        childNode = UCSNode(childState, self, problem.g(self.path_cost, self.state, childState), queenMove)
        return childNode
    
    def __lt__(self, otherNode):
        return self.path_cost < otherNode.path_cost
    
class AStarNode(StateNode):            
    def __init__(self, _state: AbstractProblem, _parent=None, _cost=0, _move=None, _heuristics=0):
        super().__init__(_state, _parent, _cost, _move, _heuristics)

    def genChildNode(self, problem: AbstractProblem, queenMove: tuple):
        childState = copy.copy(self.state)
        childState.updatePosition(problem.result(queenMove))
        childNode = AStarNode(childState, self, problem.g(self.path_cost, self.state, childState), queenMove, childState.h())
        return childNode

    def __lt__(self, otherNode):
        return (self.path_cost + self.heuristics) < (otherNode.path_cost + otherNode.heuristics)


def Search(node: StateNode):
    frontier = [node]
    heapq.heapify(frontier)
    expanded_list = set()
    expanded_list.add(node.state)
    while frontier:
        currentNode = heapq.heappop(frontier)
        if currentNode.state.goalTest():
            return currentNode
        if currentNode in expanded_list:
            continue
        children = currentNode.genSuccessors(currentNode.state)  #generate child nodes
        expanded_list.add(currentNode.state)
        for child in children:
            if child.state not in expanded_list:
                heapq.heappush(frontier, child)

    return None  # no solution


def UCSSearch(initState: AbstractProblem):
    initialState = UCSNode(initState)
    return Search(initialState)


def AStarSearch(initState: AbstractProblem):
    initialState = AStarNode(initState)
    return Search(initialState)

def genInitPopulation(initState: AbstractProblem, size):
    initPopulation = [initState]
    heapq.heapify(initPopulation)
    for i in range(size*size):
        chromo = AbstractProblem(size)
        if chromo in initPopulation:
            continue
        else: heapq.heappush(initPopulation, chromo)
    initPopulation = initPopulation[0:(size*size//2)]
    return initPopulation

def Mutate(chromo: AbstractProblem):
    MutatePoint = random.randint(0, chromo.queens - 1)
    MutateValue = random.randint(0, chromo.queens - 1)
    chromo.position[MutatePoint] = MutateValue
    return chromo

def crossOver(first_chromo: AbstractProblem, second_chromo: AbstractProblem):
    firstNewChild = first_chromo
    secondNewChild = second_chromo

    cuttingPoint = random.randint(0, len(first_chromo.position) - 1) #random cutting position
    firstNewChild.updatePosition(first_chromo.position[0:cuttingPoint] + second_chromo.position[cuttingPoint: second_chromo.queens])
    secondNewChild.updatePosition(second_chromo.position[0:cuttingPoint] + first_chromo.position[cuttingPoint: first_chromo.queens])

    mutate = random.random()
    if (mutate <= mutateProbability):
        firstNewChild = Mutate(firstNewChild)
        secondNewChild = Mutate(secondNewChild)

    return firstNewChild, secondNewChild

def geneticAlgorithm(initState, size):
    population = genInitPopulation(initState, size)
    heapq.heapify(population)
    while population[0].fitnessFunction() != maxFitness:
        bestChromo1 = heapq.heappop(population)
        bestChromo2 = heapq.heappop(population)
        newChromo1, newChromo2 = crossOver(bestChromo1, bestChromo2)
        heapq.heappush(population, newChromo1)
        heapq.heappush(population, newChromo2)
        population = population[0:size]
    return population[0]

if __name__ == "__main__":
    process = psutil.Process(os.getpid())
    start_time = time.time()
    print("Please enter the number of queens: ")

    N = input()
    N = int(N)
    print("Enter the algorithm: ")
    print("1. UCS Search")
    print("2. A* Search")
    print("3. Genetic Algorithm")

    choice = input()
    choice = int(choice)

    testBoard = AbstractProblem(N) #this can be treated as one chromosome

    print("Initial State: ")
    print(testBoard.getPosition())
    testBoard.printBoard()
    print("----------------------------")

    if N < 4:
        print("No solution")
        sys.exit(0)

    elif testBoard.goalTest():
        print("Result: ")
        testBoard.printBoard()
        print("Runtime: --- %s seconds ---" % (time.time() - start_time) + '\n')
        print("Memory: --- " + process.memory_info().rss / (1024 * 1024) + " MB ---")

    else:
        if choice == 1:
            try:
                result = UCSSearch(testBoard)
                print("Result: ")
                result.state.printBoard()
                print("Runtime: --- %s seconds ---" % (time.time() - start_time) + '\n')
                print("Memory: --- ", end="")
                print(process.memory_info().rss / (1024 * 1024), end="")
                print(" MB ---", end="")
            except AttributeError:
                print("Can't find the answer")
        elif choice == 2:
            try:
                result = AStarSearch(testBoard)
                print("Result: ")
                result.state.printBoard()
                print("Runtime: --- %s seconds ---" % (time.time() - start_time) + '\n')
                print("Memory: --- ", end="")
                print(process.memory_info().rss / (1024 * 1024), end="")
                print(" MB ---", end="")
            except AttributeError:
                print("Can't find the answer")

        else:
            maxFitness = 1
            mutateProbability = 0.3
            result = geneticAlgorithm(testBoard,N)
            print("Result: ")
            result.printBoard()
            print("Runtime: --- %s seconds ---" % (time.time() - start_time) + '\n')
            print("Memory: --- ", end="")
            print(process.memory_info().rss / (1024 * 1024), end="")
            print(" MB ---", end="")







