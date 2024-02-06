from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        

        # add the primary variables of the problem
        problem.variables = set(LHS0 + LHS1 + RHS)
        # add the domains of these variables which are from 0 to 9
        problem.domains = { variable: set(range(10)) for variable in problem.variables }
        # add unary constraints to the first characters to prevent zeros at the beginning
        problem.constraints = [ UnaryConstraint(first_letter, lambda x: x != 0) for first_letter in [LHS0[0], LHS1[0], RHS[0]] ]

        # add binary constraints between all variables to make their values unique
        for idx, variable in enumerate(problem.variables):
            for other in range(idx + 1, len(problem.variables)):
                problem.constraints.append(BinaryConstraint((variable, list(problem.variables)[other]), lambda x, y: x != y))

        LHS0 = LHS0[::-1]
        LHS1 = LHS1[::-1]
        RHS = RHS[::-1]

        # add empty variable in case the 2 operands are not the same length
        if len(LHS0) - len(LHS1) != 0:
            empty_var = '0'
                        
            problem.variables.add(empty_var)
            problem.domains[empty_var] = set([0])
            problem.constraints.append(UnaryConstraint(empty_var, lambda x: x == 0))

            if len(LHS0) < len(LHS1):
                LHS0 = LHS0 + empty_var * (len(LHS1) - len(LHS0))
            else:
                LHS1 = LHS1 + empty_var * (len(LHS0) - len(LHS1))
        
        # loop over all characters of the operands
        for i in range(len(LHS0)):
            # case 1: the 2 operands are the same character
            if LHS0[i] == LHS1[i]:
                # no carry in
                if i == 0:
                    problem.constraints.append(BinaryConstraint((LHS0[i], RHS[i]), lambda x, y: ((2 * x) % 10) == y))
                
                # there is a carry in
                else:
                    prev_lhs0 = LHS0[i-1]
                    prev_lhs1 = LHS1[i-1]
                    
                    # prev characters are the same
                    if prev_lhs0 == prev_lhs1:
                        new_aux_var = prev_lhs0 + '_cout_' + LHS0[i]
                        
                        problem.variables.add(new_aux_var)
                        problem.domains[new_aux_var] = set(f'{num}{x}' for num in range(10) for x in range(2))

                        # need to be generalized
                        last_constraint = BinaryConstraint((RHS[i], new_aux_var), lambda x, y: x == (((2 * int(y[0])) + int(y[1])) % 10))
                        is_last_char_and_all_lengths_equal = len(LHS0) == len(LHS1) == len(RHS) == i+1
                        if is_last_char_and_all_lengths_equal:
                            last_constraint = BinaryConstraint((RHS[i], new_aux_var), lambda x, y: x == (((2 * int(y[0])) + int(y[1]))))

                        problem.constraints.extend([
                            BinaryConstraint((prev_lhs0, new_aux_var), lambda x, y: ((2 * x) // 10) == int(y[1])),
                            BinaryConstraint((LHS0[i], new_aux_var), lambda x, y: x == int(y[0])),
                            last_constraint
                        ])
                    else:
                        prev_aux_var = LHS0[i-1] + LHS1[i-1] if LHS0[i-1] < LHS1[i-1] else LHS1[i-1] + LHS0[i-1]
                        new_aux_var = prev_aux_var + LHS0[i]
                        
                        problem.variables.add(new_aux_var)
                        problem.domains[new_aux_var] = set(f'0{num:02}' for num in range(19)).union(set(f'1{num:02}' for num in range(19)))
                        
                        problem.constraints.extend([
                            BinaryConstraint((prev_aux_var, new_aux_var), lambda a, b: ((int(a[0]) + int(a[1])) // 10) == int(b[0])),
                            BinaryConstraint((LHS0[i], new_aux_var), lambda a, b: f'{(2 * a):02}' == b[1:]),
                            BinaryConstraint((RHS[i], new_aux_var), lambda a, b: a == ((int(b[0]) + int(b[1:])) % 10))
                        ])
            
            # case 2: the 2 operands are different characters
            else:
                # no carry in
                if i == 0:
                    aux_var = LHS0[i] + LHS1[i] if LHS0[i] < LHS1[i] else LHS1[i] + LHS0[i]
                    # if aux_var not in problem.variables:
                    problem.variables.add(aux_var)
                    problem.domains[aux_var] = set(f'{num:02}' for num in range(100) if (num // 10 != num % 10))
                    
                    problem.constraints.extend([
                        BinaryConstraint((aux_var[0], aux_var), lambda x, y: x == int(y[0])),
                        BinaryConstraint((aux_var[1], aux_var), lambda x, y: x == int(y[1])),
                        BinaryConstraint((RHS[i], aux_var), lambda x, y: x == ((int(y[0]) + int(y[1])) % 10))
                    ])

                # there is a carry in
                else:
                    prev_lhs0 = LHS0[i-1]
                    prev_lhs1 = LHS1[i-1]

                    # prev characters are the same
                    if prev_lhs0 == prev_lhs1:
                        aux_var = (LHS0[i] + LHS1[i] if LHS0[i] < LHS1[i] else LHS1[i] + LHS0[i]) + prev_lhs0
                        problem.variables.add(aux_var)
                        problem.domains[aux_var] = set(f'{num:02}{x}' for num in range(100) if (num // 10 != num % 10) for x in range(2))

                        problem.constraints.extend([
                            BinaryConstraint((aux_var[0], aux_var), lambda x, y: x == int(y[0])),
                            BinaryConstraint((aux_var[1], aux_var), lambda x, y: x == int(y[1])),
                            BinaryConstraint((aux_var[2], aux_var), lambda x, y: ((2 * x) // 10) == int(y[2])),
                            BinaryConstraint((RHS[i], aux_var), lambda x, y: x == ((int(y[0]) + int(y[1]) + int(y[2])) % 10))
                        ])
                    else:
                        prev_aux_var = (prev_lhs0 + prev_lhs1 if prev_lhs0 < prev_lhs1 else prev_lhs1 + prev_lhs0)
                        curr_aux_var = (LHS0[i] + LHS1[i] if LHS0[i] < LHS1[i] else LHS1[i] + LHS0[i])

                        if i <= 1:
                            aux_var = prev_aux_var + '_cout_' + curr_aux_var

                            problem.variables.add(aux_var)
                            problem.domains[aux_var] = set(f'{num:02}{x}' for num in range(100) if (num // 10 != num % 10) for x in range(2))

                            problem.constraints.extend([
                                BinaryConstraint((curr_aux_var[0], aux_var), lambda x, y: x == int(y[0])),
                                BinaryConstraint((curr_aux_var[1], aux_var), lambda x, y: x == int(y[1])),
                                BinaryConstraint((prev_aux_var, aux_var), lambda x, y: ((int(x[0]) + int(x[1])) // 10) == int(y[2])),
                                BinaryConstraint((RHS[i], aux_var), lambda x, y: x == ((int(y[0]) + int(y[1]) + int(y[2])) % 10))
                            ])

                        if i > 1:
                            prev_prev_lhs0 = LHS0[i-2]
                            prev_prev_lhs1 = LHS1[i-2]

                            if prev_prev_lhs0 == prev_prev_lhs1:
                                prev_prev_aux_var = (prev_prev_lhs0 + prev_prev_lhs1 if prev_prev_lhs0 < prev_prev_lhs1 else prev_prev_lhs1 + prev_prev_lhs0)
                            else:
                                prev_prev_aux_var = (prev_prev_lhs0 + prev_prev_lhs1 if prev_prev_lhs0 < prev_prev_lhs1 else prev_prev_lhs1 + prev_prev_lhs0)
                                prev_cout_aux_var = prev_prev_aux_var + '_cout_' + prev_aux_var
                                prev_prev_aux_cout_var = prev_aux_var + '_cout_' + curr_aux_var

                                problem.variables.add(prev_prev_aux_cout_var)
                                problem.domains[prev_prev_aux_cout_var] = set(f'{num:02}{x}' for num in range(100) if (num // 10 != num % 10) for x in range(2))

                                problem.constraints.extend([
                                    BinaryConstraint((curr_aux_var[0], prev_prev_aux_cout_var), lambda x, y: x == int(y[0])),
                                    BinaryConstraint((curr_aux_var[1], prev_prev_aux_cout_var), lambda x, y: x == int(y[1])),
                                    BinaryConstraint((prev_cout_aux_var, prev_prev_aux_cout_var), lambda x, y: ((int(x[0]) + int(x[1]) + int(x[2])) // 10) == int(y[2])),
                                    BinaryConstraint((RHS[i], prev_prev_aux_cout_var), lambda x, y: x == ((int(y[0]) + int(y[1]) + int(y[2])) % 10))
                                ])
                                
                        
        if len(RHS) > len(LHS0):
            if LHS0[-1] == LHS1[-1]:
                problem.constraints.append(BinaryConstraint((LHS0[-1], RHS[-1]), lambda x, y: ((2 * x) // 10) == y))
            else:
                if len(LHS0) > 2:
                    aux_var = (LHS0[-1] + LHS1[-1] if LHS0[-1] < LHS1[-1] else LHS1[-1] + LHS0[-1])
                    prev_aux_var = (LHS0[-2] + LHS1[-2] if LHS0[-2] < LHS1[-2] else LHS1[-2] + LHS0[-2])
                    prev_prev_aux_var = (LHS0[-2] + LHS1[-2] if LHS0[-2] < LHS1[-2] else LHS1[-2] + LHS0[-2])
                    prev_cout_aux_var = prev_prev_aux_var + '_cout_' + prev_aux_var
                    problem.variables.add(aux_var)
                    problem.domains[aux_var] = set(f'{num:02}{x}' for num in range(100) if (num // 10 != num % 10) for x in range(2))
                    problem.constraints.extend([
                        BinaryConstraint((aux_var[0], aux_var), lambda x, y: x == int(y[0])),
                        BinaryConstraint((aux_var[1], aux_var), lambda x, y: x == int(y[1])),
                        BinaryConstraint((prev_cout_aux_var, aux_var), lambda x, y: ((int(x[0]) + int(x[1]) + int(x[2])) // 10) == int(y[2])),
                        BinaryConstraint((RHS[-1], aux_var), lambda x, y: x == ((int(y[0]) + int(y[1]) + int(y[2])) // 10))
                    ])
                else:
                    aux_var = (LHS0[-1] + LHS1[-1] if LHS0[-1] < LHS1[-1] else LHS1[-1] + LHS0[-1])
                    problem.variables.add(aux_var)
                    problem.domains[aux_var] = set(f'{num:02}' for num in range(100) if (num // 10 != num % 10))
                    problem.constraints.extend([
                        BinaryConstraint((aux_var[0], aux_var), lambda x, y: x == int(y[0])),
                        BinaryConstraint((aux_var[1], aux_var), lambda x, y: x == int(y[1])),
                        BinaryConstraint((RHS[-1], aux_var), lambda x, y: x == ((int(y[0]) + int(y[1])) // 10))
                    ])

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())