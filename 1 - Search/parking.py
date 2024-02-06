from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # print('GET_INITIAL_STATE', self.passages, self.cars, self.slots)
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # print('IS_GOAL', state)
        for idx, car in enumerate(state):
            if car in self.slots and self.slots[car] == idx:
                continue
            return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # print('GET_ACTIONS', state)
        actions = []
        for idx, car in enumerate(state):
            t = car.__add__(Point(0, -1))
            r = car.__add__(Point(1, 0))
            b = car.__add__(Point(0, 1))
            l = car.__add__(Point(-1, 0))
            if t in self.passages and t not in state:
                actions.append((idx, Direction(1)))
            if r in self.passages and r not in state:
                actions.append((idx, Direction(0)))
            if b in self.passages and b not in state:
                actions.append((idx, Direction(3)))
            if l in self.passages and l not in state:
                actions.append((idx, Direction(2)))
        # print(actions)
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # print('GET_SUCCESSOR', action, state)
        car_index = action[0]
        car = state[car_index]
        d = action[1].to_vector()
        updated_coords = car + d
        if updated_coords in self.passages and updated_coords not in state:
            _cars = list(state)
            # print(_cars)
            _cars[car_index] = updated_coords
            state = tuple(_cars)
        # print(state)
        return state

    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # print('GET_COST', action)
        car_index = action[0]
        car = state[car_index]
        updated_coords = car + action[1].to_vector()
        if updated_coords in self.passages and updated_coords not in state:
            cost  = 26 - car_index
            if updated_coords in self.slots and self.slots[updated_coords] != car_index:
                cost += 100
            # print(cost)
            return cost
        return -1
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
