# Class that mimics queue operations.
# Author: Fernando Abreu
# Date: 12/18/2024

from collections import deque

class Queue:
    def __init__(self):
        self.__queue = deque()
    
    def enqueue(self, item) -> None:
        self.__queue.append(item)
    
    def dequeue(self):
        if not self.empty():
            return self.__queue.popleft()
        raise IndexError("dequeue in empty queue")

    def empty(self) -> bool:
        return len(self.__queue) == 0
    
    def size(self) -> int:
        return len(self.__queue)