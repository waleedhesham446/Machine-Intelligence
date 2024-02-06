from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use
def is_deadlocked(state: SokobanState, problem: SokobanProblem):
    # count of border crates for this state
    border_crates = {
        't': 0,
        'b': 0,
        'r': 0,
        'l': 0,
    }

    for crate in state.crates:
        # in case a crate is at a goal position, it can't cause a deadlock
        if crate in state.layout.goals:
            continue
        # combine the results of the three possible deadlock situations (double box, corner, border)
        blocked = double_box_deadlock(problem, state, crate) or corner_deadlock(state, crate) or border_deadlock(state, crate, problem.cache(), border_crates)
        if blocked == True:
            return True

    return False

# Detect if a crate in a corner
def corner_deadlock(state: SokobanState, box: Point):

    up_block = (Point(box.x, box.y - 1) not in state.layout.walkable) 
    down_block = (Point(box.x, box.y + 1)  not in state.layout.walkable)   

    left_block = (Point(box.x - 1, box.y) not in state.layout.walkable)
    right_block = (Point(box.x + 1, box.y) not in state.layout.walkable)    

    return (up_block or down_block) and (left_block or right_block)

# Detect if a crate at a border while there is no more goals for this crate at this border
def border_deadlock(state: SokobanState, box: Point, cache, border_crates):
    if box.y == 1:
        border_crates['t'] += 1
        if cache.get('t_goal') - border_crates['t'] < 0:
            return True
    if box.y == state.layout.height - 2:
        border_crates['b'] += 1
        if cache.get('b_goal') - border_crates['b'] < 0:
            return True
    if box.x == 1:
        border_crates['l'] += 1
        if cache.get('l_goal') - border_crates['l'] < 0:
            return True
    if box.x == state.layout.width - 2:
        border_crates['r'] += 1
        if cache.get('r_goal') - border_crates['r'] < 0:
            return True
    return False

# Detect if there are 2 boxes preventing each other from moving
def double_box_deadlock(problem: SokobanProblem, state: SokobanState, box: Point):
    walkable = state.layout.walkable
    for box_2 in state.crates:
        if box_2 == box:
            continue
        # check if they are on the same vertical axis
        if box.x == box_2.x:
            # check if they are on top of each other
            if abs(box.y - box_2.y) == 1:
                l = box.__add__(Point(-1, 0))
                r = box.__add__(Point(1, 0))
                l2 = box_2.__add__(Point(-1, 0))
                r2 = box_2.__add__(Point(1, 0))
                if ((l not in walkable) and (l2 not in walkable)) or ((r not in walkable) and (r2 not in walkable)):
                    return True
            if box.x == 1 and problem.cache().get('l_goal') < 2:
                return True
            if box.x == state.layout.width - 2 and problem.cache().get('r_goal') < 2:
                return True
        
        # check if they are on the same horizontal axis
        if box.y == box_2.y:
            # check if they are beside each other
            if abs(box.x - box_2.x) == 1:
                t = box.__add__(Point(0, -1))
                b = box.__add__(Point(0, 1))
                t2 = box_2.__add__(Point(0, -1))
                b2 = box_2.__add__(Point(0, 1))
                if ((t not in walkable) and (t2 not in walkable)) or ((b not in walkable) and (b2 not in walkable)):
                    return True
            if box.y == 1 and problem.cache().get('t_goal') < 2:
                return True
            if box.y == state.layout.height - 2 and problem.cache().get('b_goal') < 2:
                return True
    return False

def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # NotImplemented()

    t_goal, b_goal, r_goal, l_goal = 0, 0, 0, 0
    for goal in state.layout.goals:
        if goal.y == 1:
            t_goal += 1
        elif goal.y == state.layout.height - 2:
            b_goal += 1
        if goal.x == 1:
            l_goal += 1
        elif goal.x == state.layout.width - 2:
            r_goal += 1
    
    # cache the count of goal at each border to use it in the `border_deadlock` detection
    cache = problem.cache()
    cache['t_goal'] = t_goal
    cache['b_goal'] = b_goal
    cache['r_goal'] = r_goal
    cache['l_goal'] = l_goal

    # heuristic of the goal state is zero
    if problem.is_goal(state):
        return 0
    if is_deadlocked(state, problem):
        return float('inf')
    
    total_distance = 0
    
    for crate in state.crates:
        min_distance = float('inf')
        for goal in problem.layout.goals:
            distance = manhattan_distance(crate, goal)
            min_distance = min(min_distance, distance)
        total_distance += min_distance

    return total_distance