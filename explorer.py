## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.
# IMPORTS
import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
from map import Map, THERE_VICTIM, UNTRIED_ACTIONS, UNBACKTRACKED
from stack import Stack
# MACROS
DELTA = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
VISIT = 1

# Functions

def updatePosition(position: list, delta: tuple) -> list:
    return [position[0] + delta[0], position[1] + delta[1]]

def reverse(delta: list | tuple) -> list:
    return [delta[0]*-1, delta[1]*-1]

class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)
        
        # Specific initialization for the rescuer
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore     
        self.map = Map()           # Map of environment
        self.map_vision = Map()    # Map of Vision Não confirma as vítimas
        self.backtracked = Map()   # Stack com delta daquela posição, só é executado quando untried retorna None
        self.position = [0,0]      # [x,y]
        self.action = [0,0]        # ultima ação tomada
    
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""
        dx = 0
        dy = 0
        # No more actions, time almost ended
        if self.rtime < 10.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims([],[])
            return False
        
        if not self.map.knowPosition(tuple(self.position)):
            actions_results = self.createActionsResults(self.position) # list
            content: list = [PhysAgent.CLEAR] + actions_results
            self.map.addPosition(tuple(self.position), content)
            untried_actions: Stack = content[1]
            unbacktracked = None
            if self.backtracked.knowPosition(tuple(self.position)):                             
                unbacktracked: Stack = self.backtracked.getContent(tuple(self.position))
            if not untried_actions.empty():
                self.action = list(untried_actions.pop())
                dx = self.action[0]
                dy = self.action[1]
            elif(unbacktracked is not None):
                if not unbacktracked.empty():
                    self.action = list(unbacktracked.pop())
                    dx = self.action[0]
                    dy = self.action[1]
                else:
                    dx = 0
                    dy = 0
            else:
                dx = 0
                dy = 0
            self.position = updatePosition(self.position, self.action)
            if self.backtracked.knowPosition(tuple(self.position)):
                self.backtracked.getContent(tuple(self.position)).push(reverse(self.action))
            else:
                backaction = Stack()
                backaction.push(reverse(self.action))
                self.backtracked.addPosition(tuple(self.position), backaction)
        else:
            content: list = self.map.getContent(tuple(self.position)) # [obstacle, untried_actions(Pilha), Result(dict)]
            actions: Stack = content[1]
            if(not actions.empty()):
                self.action = actions.pop()
                dx = self.action[0]
                dy = self.action[1]
                self.position = updatePosition(self.position, self.action)
                if self.backtracked.knowPosition(tuple(self.position)):
                    self.backtracked.getContent(tuple(self.position)).push(reverse(self.action))
                else:
                    backaction = Stack()
                    backaction.push(reverse(self.action))
                    self.backtracked.addPosition(tuple(self.position), backaction)
            else:
                unbacktracked: Stack = None
                if self.backtracked.knowPosition(tuple(self.position)):
                    unbacktracked: Stack = self.backtracked.getContent(tuple(self.position))
                if(unbacktracked is not None):
                    if(not unbacktracked.empty()):
                        print("Unbacktracked")
                        self.action = unbacktracked.pop()
                        dx = self.action[0]
                        dy = self.action[1]
                        self.position = updatePosition(self.position, self.action)
                    else:
                        dx = 0 # Aleatorio
                        dy = 0
                else:
                    dx = 0
                    dy = 0
        '''
        if(dx == 0 and dy == 0):
            print("Aleatório")
            dx = random.choice([-1, 0, 1])
            if dx == 0:
                dy = random.choice([-1, 1])
            else:
                dy = random.choice([-1, 0, 1])
        '''
        # Check the neighborhood obstacles
        # obstacles = self.body.check_obstacles()
        

        # Moves the body to another position
        result = self.body.walk(dx, dy)


        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            seq = self.body.check_for_victim()
            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                # print("exp: read vital signals of " + str(seq))
                # print(vs)
                
        return True


    '''
        Métodos do algoritmo DFS-on-line
    '''

    # Result[delta] = [result of the delta, VISIT] 

    def getResult(self, position: tuple) -> dict:
        result = {}
        obstacle = self.body.check_obstacles()
        for i,d in enumerate(DELTA):
            if obstacle[i] == PhysAgent.CLEAR:
                result[d] = (position[0] + d[0], position[1] + d[1])
            else:
                result[d] = position
        return result
    
    def createActionsResults(self, position: list) -> list:
        ans = []
        result = {}
        highest_priority_action = Stack()
        lower_priority_action = Stack()
        obstacle = self.body.check_obstacles()
        for i,d in enumerate(DELTA):
            if obstacle[i] == PhysAgent.CLEAR:
                result[d] = tuple([position[0] + d[0], position[1] + d[1]])
                if self.map.knowPosition(result[d]):
                    lower_priority_action.push(d)
                else:
                    highest_priority_action.push(d)
            else:
                result[d] = tuple(position)
                if not self.map.knowPosition(tuple([position[0] + d[0], position[1] + d[1]])):
                    self.map.addPosition(position = tuple([position[0] + d[0], position[1] + d[1]]), content=obstacle[i])
        while(not highest_priority_action.empty()):
            lower_priority_action.push(highest_priority_action.pop()) # embaixo da pilha esta de baixa prioridade e em cima da pilha está de alta prioridade
        ans.append(lower_priority_action)
        ans.append(result)
        return ans
    
    from typing import Optional

    def Untried(self, position: list) -> Optional[tuple]:
        if self.map.knowPosition(tuple(position)):
            stack_actions: Stack = self.map.getContent()[UNTRIED_ACTIONS]
            if not stack_actions.empty():
                return stack_actions.pop()
        return None