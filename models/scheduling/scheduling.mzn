include "scheduling_core.mzn";
%include "../simple_diversity_mixin.mzn";
include "../../test_models/copeland_constraint.mzn";

%diversity_variables_of_interest = [start[j,t] | j in JOBS, t in TASKS] ;
% diversity_variables_of_interest = util_per_agent;

%solve
%:: worst_case
%satisfy;

new_sol = util_per_agent;
num_var = n_agents;

predicate get_better_pareto(array[int] of int: compare) =
  exists(i in index_set(util_per_agent)) (util_per_agent[i] > compare[i]);
