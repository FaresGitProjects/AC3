
import sudoku
import time


class Solver:
    def AC3(self, csp, queue=None, removals=None):
        ''' YOUR CODE HERE
        return True if it is consistent;
        otherwise, return False
        '''
        if queue is None:
            queue = []
            for var in csp.variables:
                queue.extend(self.get_queue(csp, var))
        while len(queue) != 0:
            pair = queue.pop()
            if self.revise(csp, pair[0], pair[1], removals):
                if len(csp.curr_domains[pair[0]]) == 0:
                    return False
                for neighbor in csp.neighbors[pair[0]]:
                    if neighbor != pair[1]:
                        queue.append((neighbor, pair[0]))
        return True

    def revise(self, csp, Xi, Xj, removals):
        ''' YOUR CODE HERE
        return True if the domain is revised;
        otherwise, return False
        '''
        cd = csp.curr_domains[Xi]
        for ival in cd:
            if all([not csp.constraints(Xi, ival, Xj, jval) for jval in csp.curr_domains[Xj]]):
                # print(f'before {csp.curr_domains[Xi]}')
                removals = csp.prune(Xi, ival, removals)
                # print(f'after {csp.curr_domains[Xi]}')
                return True

        return False

    ''' recursive call '''

    def backtracking_search(self, csp):
        return self.backtrack({}, csp)

    def backtrack(self, assignment, csp):
        if csp.goal_test(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment, csp)
        for val in self.order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, val, assignment) == 0:
                csp.assign(var, val, assignment)
                sup = csp.suppose(var, val)
                inf = csp.infer_assignment()
                if inf is not None:
                    result = self.backtrack(assignment, csp)
                    if result is not None:
                        return result
                csp.restore(sup)
            csp.unassign(var, assignment)
        return None
        ''' YOUR CODE HERE '''

    # START: DEFINED ALREADY
    def select_unassigned_variable(self, assignment, csp):
        unassigned = []
        for i in csp.variables:
            if i not in assignment:
                unassigned.append(i)

        sorted_unassigned = sorted(unassigned, key=lambda var: len(csp.domains[var]))
        return sorted_unassigned[0]

    def order_domain_values(self, var, assignment, csp):
        return sorted(csp.domains[var], key=lambda val: csp.nconflicts(var, val, assignment))

    def get_queue(self, csp, var):
        queue = []
        for i in csp.neighbors[var]:
            queue.append((i, var))
        return queue
    # END: DEFINED ALREADY


if __name__ == '__main__':
    '''
    Some board test cases, each string is a flat enumeration of all the board positions
    where . indicates an unfilled location
    Impossible: 123456789.........123456789123456789123456789123456789123456789123456789123456789
    Easy ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
    Easy ...7.46.3..38...51.1.9.327..34...76....6.8....62...98..473.6.1.68...13..3.12.5...
    Difficult ..5...1.3....2.........176.7.49....1...8.4...3....7..8.3.5....2....9....4.6...9..
    '''

    # board = sudoku.Sudoku('12.456789.........12.45678912.45678912.45678912.45678912.45678912.45678912.456789')
    board = sudoku.Sudoku('..5...1.3....2.........176.7.49....1...8.4...3....7..8.3.5....2....9....4.6...9..')
    # Accessing the board as a csp, i.e. display the variable and domains
    # See the extra document for exapmles of how to use the  CSP class

    # Display this nonsensical board
    board.display(board)

    # Show the "flat" variables
    print(board.variables)

    # show the domeians (curr_domains beocmes populated by infer_assignment())
    print(board.curr_domains)

    '''You'll need to manipulate the CSP domains and variables, so here are some exampels'''

    # this is a list of (variable, domain value) pairs that you can use to keep track
    # # of what has been removed from the current domains
    removals = []

    # #show domains for variable 3
    print("Domain for 3: " + str(board.curr_domains[3]))
    # #remove the possible value '8' form domain 3
    # #not the differences int key for the first dictionary and the string keys

    board.prune(3, '8', removals)  # This line may not work if the domain for 3 does not contain "8"

    print("Domain for 3: " + str(board.curr_domains[3]))
    print("Removal List: " + str(removals))

    # Prune some more
    print("Domain for 23: " + str(board.curr_domains[23]))
    board.prune(23, '1', removals)
    board.prune(23, '2', removals)
    board.prune(23, '3', removals)
    print("Domain for 23: " + str(board.curr_domains[23]))
    print("Removal List: " + str(removals))

    # ooopes took away too muche! Restore removals
    board.restore(removals)
    print("Domain for 23: " + str(board.curr_domains[23]))

    # For assigning vaeiables use a dictionary like
    assignment = {}
    board.assign(23, '8', assignment)
    # ocne all the variables are assigned, you can use goal_thest()

    # find the neighbors of a varaible
    print("Neighbors of 0: " + str(board.neighbors[0]))

    # check for a constraint, need to plug in a specific var,val, var val combination
    # since 0 and 1 and neighbors, they should be different values
    print(board.constraints(0, '0', 1, '0'))  # should be false
    print(board.constraints(0, '0', 1, '1'))  # should be true i.e. not a constraint

    '''to check your implementatios:'''

    # AC3 should return false for impossible example above
    sol = Solver()
    start = time.perf_counter()
    print("Running AC3...")
    print(sol.AC3(board))
    print("\n" + "time: " + str(time.perf_counter() - start))
    print("Ran AC3")
    board.display(board)

    # backtracking search usage example
    start = time.perf_counter()
    print("Running Backtrack...")
    print(sol.backtracking_search(board))
    print("\n" + "time: " + str(time.perf_counter() - start))
    print("Ran Backtrack")
    board.display(board)
