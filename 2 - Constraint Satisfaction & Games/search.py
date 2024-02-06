from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    
    # the recursive minimax function
    def recursive_minimax(state: S, depth: int) -> Tuple[float, A]:

        agent = game.get_turn(state)
        
        # check if it's terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[agent], None

        # max node
        if agent == 0:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return heuristic(game, state, agent), None
            
            # get max value and its corresponding action
            max_value = float('-inf')
            best_action = None

            # for each action, get its value recursivly
            for action in game.get_actions(state):
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1)
                if value > max_value:
                    max_value = value
                    best_action = action
            return max_value, best_action
        
        # min node
        else:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return -1 * heuristic(game, state, agent), None

            # get min value and its corresponding action
            min_value = float('inf')
            best_action = None

            # for each action, get its value recursivly
            for action in game.get_actions(state):
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1)
                if value < min_value:
                    min_value = value
                    best_action = action
            return min_value, best_action

    # start recursion
    return recursive_minimax(state, 0)


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    
    # the recursive minimax function
    def recursive_minimax(state: S, depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        
        agent = game.get_turn(state)
        
        # check if it's terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        best_action = None

        # max node
        if agent == 0:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return heuristic(game, state, agent), None

            # get max value and its corresponding action
            max_value = float('-inf')
            actions = game.get_actions(state)

            # for each action, get its value recursivly
            for action in actions:
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1, alpha, beta)
                if value > max_value:
                    max_value = value
                    best_action = action

                # update the alpha
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break  # Beta cut-off

            return max_value, best_action

        # min node
        else:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return -1 * heuristic(game, state, agent), None

            # get min value and its corresponding action
            min_value = float('inf')
            actions = game.get_actions(state)

            # for each action, get its value recursivly
            for action in actions:
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1, alpha, beta)
                if value < min_value:
                    min_value = value
                    best_action = action
                
                # update the beta
                beta = min(beta, min_value)
                if beta <= alpha:
                    break  # Alpha cut-off

            return min_value, best_action

    # start recursion
    return recursive_minimax(state, 0, float('-inf'), float('inf'))

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    
    # the recursive minimax function
    def recursive_minimax(state: S, depth: int, alpha: float, beta: float) -> Tuple[float, A]:

        agent = game.get_turn(state)
        
        # check if it's terminal node
        terminal, values = game.is_terminal(state)
        if terminal:
            return values[0], None

        best_action = None

        # max node
        if agent == 0:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return heuristic(game, state, agent), None

            # get max value and its corresponding action
            max_value = float('-inf')
            actions = game.get_actions(state)

            # order actions based on heuristic values
            actions.sort(key=lambda a: heuristic(game, game.get_successor(state, a), agent), reverse=True)  # Order moves based on heuristic evaluation

            # for each action, get its value recursivly
            for action in actions:
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1, alpha, beta)
                if value > max_value:
                    max_value = value
                    best_action = action

                # update alpha
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break  # Beta cut-off

            return max_value, best_action

        # min node
        else:
            # check if reached max depth
            if max_depth != -1 and depth >= max_depth:
                return -1 * heuristic(game, state, agent), None

            # get min value and its corresponding action
            min_value = float('inf')
            actions = game.get_actions(state)

            # order actions based on heuristic values
            actions.sort(key=lambda a: heuristic(game, game.get_successor(state, a), agent), reverse=True)  # Order moves based on heuristic evaluation

            # for each action, get its value recursivly
            for action in actions:
                next_state = game.get_successor(state, action)
                value, _ = recursive_minimax(next_state, depth + 1, alpha, beta)
                if value < min_value:
                    min_value = value
                    best_action = action
                # update beta
                beta = min(beta, min_value)
                if beta <= alpha:
                    break  # Alpha cut-off

            return min_value, best_action

    # start recursion
    return recursive_minimax(state, 0, float('-inf'), float('inf'))

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    agent = game.get_turn(state)
    depth = game.cache().get('depth', 0)

    # update depth
    game.cache().__setitem__('depth', depth + 1)

    terminal, values = game.is_terminal(state)
    if terminal: return values[0], None

    # check if reached max depth
    if max_depth != -1 and depth >= max_depth:
        value, action = heuristic(game, state, agent), None
        if agent != 0:
            value *= -1
    # max node
    elif agent == 0:
        # get max value
        value = float('-inf')
        best_action = None
        actions = game.get_actions(state)
        for action in actions:
            next_state = game.get_successor(state, action)
            result = expectimax(game, next_state, heuristic, max_depth)[0]
            if result > value:
                value = result
                best_action = action
        action = best_action
    # average node
    else:
        # get average values
        value = 0
        actions = game.get_actions(state)
        for action in actions:
            next_state = game.get_successor(state, action)
            result = expectimax(game, next_state, heuristic, max_depth)[0]
            value += result
        value /= len(actions)
        action = None
    game.cache().__setitem__('depth', depth)

    return value, action