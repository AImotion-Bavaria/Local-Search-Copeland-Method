%include "../simple_diversity_mixin.mzn";
include "vehicle_routing_core.mzn";
include "../../test_models/copeland_constraint.mzn";

%----------------------------------------------------------------------------
% connecting the model hook from the diversity mixin to this model
%diversity_variables_of_interest = startOfVisit; % all other variables depend on this assignment  

new_sol = util_per_agent;
num_var = card(Passenger);

predicate get_better_pareto(array[int] of int: compare) =
  exists(i in index_set(util_per_agent)) (util_per_agent[i] > compare[i]);
