# Class to build the map of environment
# Author: Fernando Abreu
# Date: 12/18/2024

# MACROS
THERE_VICTIM = 0
UNTRIED_ACTIONS = 1
UNBACKTRACKED = 2

class Map:
    def __init__(self):
        self.__map = {} # [obstacle, untried_actions(Pilha), Result(dict)]
    
    def addPosition(self, position: tuple, content: any) -> None:
        self.__map[position] = content

    def knowPosition(self, position: tuple) -> bool:
        if position in self.__map:
            return True
        return False

    def getContent(self, position: tuple) -> int:
        return self.__map[position]
    
    def update(self, item):
        self.__map.update(item)
    
# end of the class Map
    
    
