from queue import PriorityQueue
import networkx as nx
import random

class ChessBoard: #here "queens" is also the size of the chess board
    position = ""
    
    def __init__(self, queens):
        self.queens = queens
        for cols in queens:
            queenIndex = random.randrange(1,queens,1)
            self.position += queenIndex
            
    
    
    