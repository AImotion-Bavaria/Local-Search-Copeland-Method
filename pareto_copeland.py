from minizinc import Instance, Model, Result, Solver, Status
import numpy as np
import logging
logging.basicConfig(filename="minizinc-python.log", level=logging.DEBUG)

def make_const_str(inst, prev_sols):
    """
    Given minizinc instance and list of previous solutions found in search, add constraint string to
    instance requiring that the next solution is not pareto dominated by any solution in the previous
    solutions list.
    :param inst: minizinc instance
    :param prev_sols: list of previous solutions found in minizinc search
    :return: none
    """
    for i, sol in enumerate(prev_sols):
        constraint_string = "constraint get_better_pareto(" + str(list(sol)) + ");\n"
        inst.add_string(constraint_string)
    return

def pareto_search(model, datafile):
    """
    Given a minizinc model and datafile, perform a metaheuristic search for solutions. There is a loop
    to find solutions to the minizinc model with given data, and solutions found are added to the list of
    preference profiles. These are the "old solutions" for the model, and in each loop, we require through
    additional constraints in minizinc that new solutions are not pareto dominated by the old solutions
    that were previously found. The loop continues until the model becomes unsatisfiable. Paired with the
    copeland constraint within the minizinc model directly, the last solution is the "chosen solution"
    and is the copeland winner out of the selected solutions set (or has tied copeland score) and is
    a non pareto dominated solution compared to previous solutions found while searching.

    :param model: minizinc model name
    :param datafile: data file for minizinc model
    :return: set of solutions found during looping
    """

    #set up model and datafile for minizinc
    model_file = "./models/" + model + "/" + model + ".mzn"
    m = Model(model_file)  # "./models/photo_placement.mzn"
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("chuffed")  # why chuffed?
    # Create an Instance of the n-Queens model for Gecode
    inst = Instance(gecode, m)
    inst.add_file("./models/" + model + "/data/" + datafile + ".dzn")

    pref_profiles = []
    search_more = True
    first = True
    n=1

    #find pareto optimal solutions with respect to previous solutions found:
    while search_more:
        with inst.branch() as child:
            child["old_sols"] = pref_profiles
            if first:
                child.add_string("\n")
                first = False
            else:
                make_const_str(child, pref_profiles)
            child.add_string("solve satisfy;")
            res = child.solve()

            if res.solution is not None:
                print(f'{n }------------------------------------------------------------')
                pref_profiles.append(res["util_per_agent"])
                n = n+1
                print(res["util_per_agent"])
                print(pref_profiles)
            else:
                print('no solution found')
                search_more = False

    return pref_profiles

def copeland(new_sol, old_sols):
    """
    compute copeland score of a new solution with respect to the old solution set
    :param new_sol: one new solution preference profile, array or list
    :param old_sols: 2d list or array, including possibly multiple preference profiles
    :return: copeland score of new solution
    """
    new_sol = np.array(new_sol)
    old_sols = np.array(old_sols)
    c_score = 0
    for i in range(old_sols.shape[0]):
        count = 0
        for j in range(old_sols.shape[1]):
            if new_sol[j] > old_sols[i,j]:
                count = count + 1
            elif new_sol[j] < old_sols[i,j]:
                count = count - 1
        if count > 0:
            c_score = c_score + 1
        elif count < 0:
            c_score = c_score - 1
    return c_score


if __name__ == '__main__':
    #use pareto-copeland search to find final solution

    #selected_sols = pareto_search('scheduling', '4')
    #selected_sols = pareto_search('photo_placement_bipolar', '6')
    #selected_sols = pareto_search('vehicle_routing', '3')
    selected_sols = pareto_search('project_assignment', '3')

    print('=======================================================\n')
    print(np.array(selected_sols))

    #print copeland scores of selected solutions,
    #then final copeland winner and pareto efficient solution:
    c_score_list = []
    for i in range(len(selected_sols)):
        c_score = copeland(selected_sols[i], selected_sols)
        c_score_list.append(c_score)
    print(f'\nCopeland scores of solution set: \n{c_score_list}')

    print(f'\nFinal Solution = {selected_sols[-1]}')