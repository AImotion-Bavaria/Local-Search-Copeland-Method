import logging
from os import listdir
from os.path import isfile, join
import os
import pickle
import numpy as np
import iterative_copeland as ic
import matplotlib.pyplot as plt

logging.basicConfig(filename="minizinc-python.log", level=logging.DEBUG)

from minizinc import Instance, Model, Result, Solver, Status

#print solutions obtained from random search, in batch of 10,
#then print solutions obtained from diversity max search, in batch of 10
#want to observe the difference between these solution sets

#use photo_placement_bipolar

#first function: random search first n solutions
def normal_search(n, model, datafile):
    model_file = "./models/" + model + "/" + model + ".mzn"

    m = Model(model_file)  # "./models/photo_placement.mzn"
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("chuffed")  #why chuffed?
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, m)
    instance.add_file("./models/" + model + "/data/" + datafile + ".dzn")
    #save_at = model + "_profiles/"
    results_position = []
    results_agent = []
    welfare_vals = []

    with instance.branch() as inst:
        inst["old_solutions"] = []
        inst.add_string("solve satisfy;")
        result = inst.solve(all_solutions=True)
        diversity_vals = []
        utility_vals = []
        for i in range(len(result)):
            diversity_vals.append(result[i, "diversity_variables_of_interest"])
            utility_vals.append(result[i, "util_per_agent"])

    # print('normal_search')
    # print(model_file)
    for i in range(n):
        results_position.append(result[i].position_of_agent)
        results_agent.append(result[i].agent_of_position)
        welfare_vals.append(result[i].social_welfare)

    return results_position, results_agent, utility_vals, welfare_vals, diversity_vals

#second function: diversity max first n solutions
#these to be found with respect to another
#type = 'count' or 'abs'..... what about count?
def diversity_search(n, model, datafile, type = 'abs'):
    model_file = "./models/" + model + "/" + model + ".mzn"

    m = Model(model_file)  # "./models/photo_placement.mzn"
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("chuffed")  # why chuffed?
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, m)
    instance.add_file("./models/" + model + "/data/" + datafile + ".dzn")
    # save_at = model + "_profiles/"

    sol_pool = []
    results_position = []
    results_agent = []
    welfare_vals = []
    utility_vals = []
    diversity_vals = []
    search_more = True

    while (search_more):
        with instance.branch() as inst:
            if ( len(sol_pool) == 0 ):
                inst.add_string("solve satisfy;")
            else:
                inst.add_string("solve maximize diversity_abs;")

            inst["old_solutions"] = sol_pool
            result = inst.solve()
            results_position.append(result["position_of_agent"])
            results_agent.append(result["agent_of_position"])
            utility_vals.append(result["util_per_agent"])
            welfare_vals.append(result["social_welfare"])
            diversity_vals.append(result["diversity_variables_of_interest"])
            sol_pool.append(result["position_of_agent"])
            #print(result)

            if (len(sol_pool)==n):
                search_more = False

    return results_position, results_agent, utility_vals, welfare_vals, diversity_vals


if __name__ == "__main__":
    n=20
    for datafile_name in ['6', '7', '8']:
        print("================================================================================")
        print("================================================================================")
        print(datafile_name)
        print('--------------------------')
        results_position_norm, results_agent_norm, utility_vals_norm, welfare_vals_norm, diversity_vals_norm = normal_search(n, 'photo_placement_bipolar', datafile_name)
        results_position_div, results_agent_div, utility_vals_div, welfare_vals_div, diversity_vals_div = diversity_search(n, 'photo_placement_bipolar', datafile_name, type = 'abs')

        #compare normal vs diversity search
        print('                                 normal                 diversity maximization')
        for i in range(n):
            print(f'result {i} ---------------------------------------------------------------------')
            print('position_of_agent:       ', f'{results_position_norm[i]}'.ljust(30), f'{results_position_div[i]}'.ljust(30))
            #print('agent_of_position:       ', f'{results_agent_norm[i]}'.ljust(30), f'{results_agent_div[i]}'.ljust(30))
            print('utility value:           ', f'{utility_vals_norm[i]}'.ljust(30), f'{utility_vals_div[i]}'.ljust(30))
            print('social welfare value:    ', f'{welfare_vals_norm[i]}'.ljust(30), f'{welfare_vals_div[i]}'.ljust(30))
            #print('diversity value:         ', f'{diversity_vals_norm[i]}'.ljust(30), f'{diversity_vals_div[i]}'.ljust(30))

        #create social welfare plot
        plt.figure(figsize=(8, 6))
        index = np.arange(1,(n+1))
        plt.scatter(index, welfare_vals_norm, c = 'red', label = 'normal_search')
        plt.plot(index, welfare_vals_norm, c = 'red')
        plt.scatter(index, welfare_vals_div, c = 'blue', label = 'diversity_maximization_search')
        plt.plot(index, welfare_vals_div, c = 'blue')

        plt.title('Photo Placement Bipolar: Social Welfare vs Search Type')
        plt.xlabel('Solution #')
        plt.ylabel('Social Welfare')
        plt.legend()
        plt.show()

    #what is the diversity value for the photo_placement_bipolar = position_of_agent
    #what about the count for the differences? diversity_count not implemented?

    # print(f'result {i} ----------')
    # print(f'position_of_agent:     {result[i].position_of_agent}')
    # print(f'agent_of_position:     {result[i].agent_of_position}')
    # print(f'utility value:         {utility_vals[i]}')
    # print(f'social welfare value:  {result[i].social_welfare}')
    # print(f'diversity value:       {diversity_vals[i]}')

    # print('diversity_search')
    # print(model_file)
    # for i in range(n):
    #     print(f'result {i} ----------')
    #     print(f'position_of_agent:     {results_position[i]}')
    #     print(f'agent_of_position:     {results_agent[i]}')
    #     print(f'utility value:         {utility_vals[i]}')
    #     print(f'social welfare value:  {welfare_vals[i]}')
    #     print(f'diversity value:       {diversity_vals[i]}')