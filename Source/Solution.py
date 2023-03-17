from queue import PriorityQueue
import random

class ChessBoard: #here "queens" is also the size (number of rows and columns) of the chess board
    position = []
    queens: int
    
    def __init__(self, queens):
        self.queens = queens
        for cols in range(queens):
            queenIndex = random.randrange(0,queens-1,1)
            self.position.append(queenIndex)
            
    def getPosition(self):
        return self.position
    
    def updatePosition(self, newState):
        self.position = newState
        
    def conflict(self, row1, col1, row2, col2) -> bool:
        return row1 == row2  or abs(row1 - row2) == abs(col1 - col2)
    
    def printBoard(self):
        positions = self.getPosition()
        for rows in range (0,self.queens):
            for queens in positions: 
                if (queens == rows):
                    print(" Q ", end="")
                else: print(" * ",end="")
                
            print('\n')  
           

class StateNode:
    state: ChessBoard
    heuristics: int
    parent: ChessBoard
    
    def __init__(self, _state: ChessBoard, _heuristics: int, _parent: ChessBoard):
        self.state = _state
        self.heuristics = _heuristics
        self.parent = _parent
        
        
    def genSuccessors(self):
        for cols in range(self.board.queens):
            index = 0
            if (position[index] == self.board.queens):
                position[index] = 1
            else : position[index] += 1
            index += 1
            
    def h(self, state):
        pass

class Graph:
    def __init__(self) -> None:
        pass    
    
            
    
    
print("Please enter the number of queens: ")
N = input()    
testBoard = ChessBoard(int(N))
position = testBoard.getPosition()
print(position)    
testBoard.printBoard()
    