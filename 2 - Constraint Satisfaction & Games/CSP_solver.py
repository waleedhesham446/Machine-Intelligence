from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
import copy

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # NotImplemented()

    # loop over all constraints in the problem
    for constraint in problem.constraints:
        
        # check if this constraint is not a UnaryConstraint
        if isinstance(constraint, UnaryConstraint):
            continue
        
        # cast the constraint to its original class `BinaryConstraint`
        constraint: BinaryConstraint = constraint
        v1, v2 = constraint.variables

        # check if the assigned variable is involved in this constraint
        if assigned_variable not in constraint.variables:
            continue
        
        # get the other involved variable
        other_variable = constraint.get_other(assigned_variable)

        # get the domain of the other involved variable
        other_variable_domain = domains.get(other_variable, set())

        # check if the other involved variable has no domain (already assigned)
        if len(other_variable_domain) == 0:
            continue
        
        # make a copy of the variable domain to keep the length constant because of deletion in the loop
        other_variable_domain_copy = other_variable_domain.copy()

        # loop over all values in the other variable domain
        for other_value in other_variable_domain_copy:

            # prepare the variables order
            param1, param2 = other_value, assigned_value
            if assigned_variable == v1:
                param1, param2 = assigned_value, other_value

            # check if the constraint is violated
            if constraint.condition(param1, param2) == False:
                # remove the assigned value from the other involved variable domain (if exist)
                other_variable_domain.discard(other_value)
                # check if the other involved variable domain became empty
                if len(other_variable_domain) == 0:
                    return False

    # no constraint made any variable's domain empty, valid assignment
    return True

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    # NotImplemented()
    
    # retrieve the domain of the variable to assign
    variable_domain = domains[variable_to_assign]

    # create a dictionary that have the domain values of the variable to assign as keys and the values are initialized with zeros to represent the dependency between each value in the domain and the domains of other variables
    domain_values_dependency = { value: 0 for value in variable_domain }

    # iterate through each value in the domain
    for value in variable_domain:
        
        # count the number of remaining values for neighboring variables if 'value' is assigned
        count = 0
        for constraint in problem.constraints:
            # check if it is a binary constraint and the variable to assign is involved in this constraint
            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:
                # get the variables of this constraint
                v1, v2 = constraint.variables

                # get the other variable
                other_variable = constraint.get_other(variable_to_assign)

                # get the other variable domain
                other_variable_domain = domains.get(other_variable, set())
                
                # loop over all values of the other variable domain
                for other_value in other_variable_domain:
                    
                    # prepare the variables order
                    param1, param2 = other_value, value
                    if variable_to_assign == v1:
                        param1, param2 = value, other_value

                    # check if the condition is not breaked
                    if constraint.condition(param1, param2):
                        continue
                    # condition is breaked and the count will be incremented
                    else:
                        count += 1
        
        # store the count for the current value
        domain_values_dependency[value] = count

    # sort the values based on the count of remaining values in ascending order
    return sorted(variable_domain, key=lambda val: (domain_values_dependency[val], val))
    
# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    # NotImplemented()

    # define the backtrack function which will do the backtracking algorithm
    def backtrack(problem: Problem, assignment: Assignment, domains: Dict[str, set]) -> Optional[Assignment]:

        # return the assignment in case it is complete
        if problem.is_complete(assignment):
            return assignment
        
        # get the variable with the minimum remaining values
        variable = minimum_remaining_values(problem, domains)

        # get the values of this variable sorted based on the least conflicting with other variables
        values = least_restraining_values(problem, variable, domains)

        # remove the domain of this variable, marking it as assigned
        variable_domain = domains.pop(variable)

        # loop over all values of the selected variable
        for value in values:
            # make a deep copy of the domain
            domains_copy = copy.deepcopy(domains)
            # add assignation of the variable
            assignment[variable] = value
            # update the domains and check if this assignation will not make another variable wih empty domain
            if forward_checking(problem, variable, value, domains_copy):
                # the assignation is valid, backtrack again with this assignation and the updated domains
                result = backtrack(problem, assignment, domains_copy)
                # check if the returned result is valid to return it
                if result is not None:
                    return result
            # remove the assigned variable to not conflict with other assignations
            del assignment[variable]
        # add back the deleted domain of the selected variable 
        domains[variable] = variable_domain

        # return None if no assignation was valid
        return None

    # apply one consistency and check if the problem is not solvable after applying it
    if not one_consistency(problem):
        return None
    
    # start backtracking
    return backtrack(problem, {}, problem.domains)