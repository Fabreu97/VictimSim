# Class that mimics stack operations.
# Author: Fernando Abreu
# Date: 12/18/2024

from collections import deque

class Stack:
    def __init__(self):
        self.__stack = deque()
    
    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        if not self.empty():
            return self.__stack.pop()
        raise IndexError("pop opetaion in Empty Stack!")

    def empty(self) -> bool:
        return len(self.__stack) == 0
    
    def size(self):
        return len(self.__stack)