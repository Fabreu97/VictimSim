# Class to build the map of environment
# Author: Fernando Abreu
# Date: 12/18/2024

class Map:
    def __init__(self):
        self.__map = {} # [Content, Result]
    
    def addPosition(self, position, content) -> None:
        self.__map[position] = content

    def knowPosition(self, position: tuple) -> bool:
        if position in self.__map:
            return True
        return False

    def getContent(self, position: tuple) -> int:
        return self.__map[position]
    
    def update(self, map: dict):
        self.__map.update(map)
    
# end of the class Map
    
    
