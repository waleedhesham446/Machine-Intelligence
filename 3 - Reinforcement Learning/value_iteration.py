from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        # return 0 if terminal state
        if self.mdp.is_terminal(state):
            return 0.0
        
        # initialize the utility with negative infinity
        U = float('-inf')
        # loop over all possible actions from this state
        for action in self.mdp.get_actions(state):
            # get possible successor states
            next_states = self.mdp.get_successor(state, action)
            # initialize the possible utility with 0
            R = 0.0
            # loop over all possible successor state with its probability
            for next_state, probability in next_states.items():
                # calculate the bellman equation
                next_state_reward = self.mdp.get_reward(state, action, next_state)
                R += probability * (
                    next_state_reward +
                    self.discount_factor * self.utilities[next_state]
                )
            # take the maximum utility
            U = max(U, R)
        
        return U
        
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()
        # initialize the maximum change in utility with 0
        max_u_change = 0

        # make a copy of the utilities
        utils_copy = self.utilities.copy()
        # loop over all states
        for state in self.mdp.get_states():
            prev_u = self.utilities[state]
            # compute the new utility for this state using compute_bellman
            new_u = self.compute_bellman(state)
            # update the utility in the utilities copy
            utils_copy[state] = new_u
            # take the maximum change in utility
            max_u_change = max(max_u_change, abs(new_u - prev_u))
        # update the utilities with the updated utilities copy
        self.utilities = utils_copy
        # True if the maximum change in utility is less than or equal the tolerance
        return max_u_change <= tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        # NotImplemented()
        converged = False
        iteration_count = 0

        if iterations is None:
            # if iterations is None, loop until it converges to the tolerance
            while not converged:
                converged = self.update(tolerance)
                iteration_count += 1
        else:
            # if iterations is None, loop specific number of iterations or until it converges to the tolerance
            for _ in range(iterations):
                converged = self.update(tolerance)
                iteration_count += 1
                if converged:
                    break
        
        return iteration_count
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        # return 0 if terminal state
        if self.mdp.is_terminal(state):
            return None
        
        best_action = None
        best_action_utility = float('-inf')
        # loop over all possible actions from this state
        for action in self.mdp.get_actions(state):
            # get possible successor states
            next_states = self.mdp.get_successor(state, action)
            action_utility = 0.0
            # loop over all possible successor state with its probability
            for next_state, probability in next_states.items():
                # calculate the bellman equation
                action_utility += probability * (
                    self.mdp.get_reward(state, action, next_state) + 
                    self.discount_factor * self.utilities[next_state]
                )
            # take the action with the maximum utility
            if action_utility > best_action_utility:
                best_action_utility = action_utility
                best_action = action
    
        return best_action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
