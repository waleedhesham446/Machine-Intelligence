from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # print('BFS', problem)
    if problem.is_goal(initial_state):
        return []
    explored = { initial_state: True }
    child_parent = {}
    queue = [initial_state]
    while len(queue) > 0:
        state = queue.pop(0)
        # print('STATE:', state)
        
        for action in problem.get_actions(state):
            # print('ACTION:', action)
            successor = problem.get_successor(state, action)
            if successor in explored:
                continue
            child_parent[successor] = (state, action)
            if problem.is_goal(successor) == True:
                # print('FOUND GOAL, PATH DICT:', child_parent)
                solution_list = []
                node = successor
                while node in child_parent and node != initial_state:
                    node, _action = child_parent[node]
                    solution_list.insert(0, _action)
                # print('SOLUTION:', solution_list)
                return solution_list
            explored[successor] = True
            queue.append(successor)
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # print('DFS', problem)
    explored = {}
    child_parent = {}
    stack = [initial_state]
    while len(stack) > 0:
        state = stack.pop()
        # print('STATE:', state)
        if state in explored:
            continue
        explored[state] = True
        if problem.is_goal(state) == True:
            # print('FOUND GOAL, PATH DICT:', child_parent)
            solution_list = []
            node = state
            while node in child_parent and node != initial_state:
                node, _action = child_parent[node]
                solution_list.insert(0, _action)
            # print(solution_list)
            return solution_list

        for action in problem.get_actions(state):
            # print('ACTION:', action)
            successor = problem.get_successor(state, action)
            if successor in explored:
                continue
            child_parent[successor] = (state, action)
            stack.append(successor)
    return None

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # print('UCS', problem)
    explored = {}
    child_parent = {}
    priority_queue = []
    order = 0
    # the order is used as a priority fallback in case 2 nodes have the same cost
    heapq.heappush(priority_queue, (0, order, initial_state))
    while priority_queue:
        p, o, state = heapq.heappop(priority_queue)
        # print('STATE:', state)
        if state in explored:
            continue
        explored[state] = True
        if problem.is_goal(state) == True:
            # print('FOUND GOAL, PATH DICT:', child_parent)
            solution_list = []
            node = state
            while node in child_parent and node != initial_state:
                node, c, a = child_parent[node]
                solution_list.insert(0, a)
            # print(solution_list)
            return solution_list

        for action in problem.get_actions(state):
            # print('ACTION:', action)
            successor = problem.get_successor(state, action)
            if successor in explored:
                continue
            cost = problem.get_cost(state, action) + p
            if successor in child_parent:
                _state, _cost, _action = child_parent[successor]
                if _cost > cost:
                    child_parent[successor] = (state, cost, action)
            else:
                child_parent[successor] = (state, cost, action)

            order += 1
            heapq.heappush(priority_queue, (cost, order, successor))
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # print('A* SEARCH', problem)
    explored = {}
    child_parent = {}
    priority_queue = []
    order = 0
    h = heuristic(problem, initial_state)
    heapq.heappush(priority_queue, (h, order, 0, initial_state))
    while priority_queue:
        state_f, o, _c, state = heapq.heappop(priority_queue)
        # print('STATE:', state)
        if state in explored:
            continue
        explored[state] = True
        if problem.is_goal(state) == True:
            # print('FOUND GOAL, PATH DICT:', child_parent)
            solution_list = []
            node = state
            while node in child_parent and node != initial_state:
                node, c, _a = child_parent[node]
                solution_list.insert(0, _a)
            # print(solution_list)
            return solution_list
        for action in problem.get_actions(state):
            # print('ACTION:', action)
            successor = problem.get_successor(state, action)
            if successor in explored:
                continue
            h = heuristic(problem, successor)
            cost = problem.get_cost(state, action) + _c
            f = h + cost
            if successor in child_parent:
                parent, _f, _action = child_parent[successor]
                if _f > f:
                    child_parent[successor] = (state, f, action)
            else:
                child_parent[successor] = (state, f, action)

            order += 1
            heapq.heappush(priority_queue, (f, order, cost, successor))
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    # print('GREEDY BEST FIRST SEARCH', problem)
    explored = {}
    child_parent = {}
    priority_queue = []
    order = 0
    h = heuristic(problem, initial_state)
    heapq.heappush(priority_queue, (h, order, initial_state))
    while priority_queue:
        p, o, state = heapq.heappop(priority_queue)
        # print('STATE:', state)
        if state in explored:
            continue
        explored[state] = True
        if problem.is_goal(state) == True:
            # print('FOUND GOAL, PATH DICT:', child_parent)
            solution_list = []
            node = state
            while node in child_parent and node != initial_state:
                node, _heuristic, _action = child_parent[node]
                solution_list.insert(0, _action)
            # print(solution_list)
            return solution_list
        for action in problem.get_actions(state):
            # print('ACTION:', action)
            successor = problem.get_successor(state, action)
            if successor in explored:
                continue
            h = heuristic(problem, successor)
            if successor in child_parent:
                _state, _h, _a = child_parent[successor]
                if _h > h:
                    child_parent[successor] = (state, h, action)
            else:
                child_parent[successor] = (state, h, action)

            order += 1
            heapq.heappush(priority_queue, (h, order, successor))
    return None