from simpleai.search import SearchProblem
from simpleai.search import astar, depth_first, greedy,  breadth_first
import pickle

class Rover(SearchProblem):
    def __init__(self, origin, destination, map) -> None:
        super().__init__(initial_state=origin)
        self.map = map
        self.destination = destination
        self.map_limit = (self.map.shape[0], self.map.shape[1])

    def actions(self, state) -> list:
        moves = []
        if state[0] > 0:
            objective_nav = self.map[state[0]-1,state[1]]
            print(f'{state[1]}-{state[0]}->{objective_nav}')
            if objective_nav in [3, 4]:
                moves.append((state[0]-1,state[1]))
        if state[0] < self.map_limit[0]:
            objective_nav = self.map[state[0]+1,state[1]]
            print(f'{state[1]}-{state[0]}->{objective_nav}')
            if objective_nav in [3, 4]:
                moves.append((state[0]+1,state[1]))
        if state[1] > 0:
            objective_nav = self.map[state[0],state[1]-1]
            print(f'{state[1]}-{state[0]}->{objective_nav}')
            if objective_nav in [3, 4]:
                moves.append((state[0],state[1]-1))
        if state[1] < self.map_limit[1]:
            objective_nav = self.map[state[0],state[1]+1]
            print(f'{state[1]}-{state[0]}->{objective_nav}')
            if objective_nav in [3, 4]:
                moves.append((state[0],state[1]+1))
        return moves

    def cost(self, state, action, state2):
        return 1

    def result(self, state, action) -> tuple:
        state = action
        return state

    def is_goal(self, state) -> tuple:
        return state == self.destination

    def heuristic(self, state) -> int:
        return abs(state[0]-self.destination[0]) + abs(state[1]-self.destination[1])

class PredictPath:

    def __init__(self, origin, destination) -> None:
        print(origin)
        self.origin = (origin[1]//200, origin[0]//200)
        print(self.origin)
        self.destination = (destination[1]//200, destination[0]//200)
        print(self.destination)
        inputFile = open('./Data/map.obj', 'rb')
        self.map = pickle.load(inputFile)
        rover = Rover(origin=self.origin, destination=self.destination, map=self.map)
        self.result = astar(rover, graph_search=True)
        print(self.result)


