from queue import PriorityQueue
import random

class ChessBoard: #here "queens" is also the size (number of rows and columns) of the chess board
    position = []
    queens: int
    
    def __init__(self, queens):
        self.queens = queens
        for cols in range(queens):
            queenIndex = random.randrange(1,queens,1)
            self.position.append(queenIndex)
            
    def getPosition(self):
        return self.position
    
    def updatePosition(self, newState):
        self.position = newState
        
    def conflict(self) -> bool:
        pass
        

class StateNode:
    board: ChessBoard
    heuristics: int
    parent: ChessBoard
    
    def __init__(self, _board: ChessBoard, _heuristics: int, _parent: ChessBoard):
        self.board = _board
        self.heuristics = _heuristics
        self.parent = _parent
        
        
    def genSuccessors(self):
        for cols in range(self.board.queens):
            index = 0
            if (position[index] == self.board.queens):
                position[index] = 1
            else : position[index] += 1
            index += 1
            
    def h(self):
        pass

class Graph:
    def __init__(self) -> None:
        pass    
            
    
    
print("Please enter the number of queens: ")
N = input()    
testBoard = ChessBoard(int(N))
position = testBoard.getPosition()
print(position)    
    