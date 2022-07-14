par int: num_var; 
array[int, int] of par int: old_sols;

array[1..num_var] of var int: new_sol;

%copeland score computation---------------------------------------------
%functions "a" indicate that the first input variable is a parameter, and the second is our variable solution
%functions "b" are the opposite of b.
function var int: wins_a(array[int] of int: old_sol, array[int] of var int: new_sol) = 
   sum(j in 1..length(new_sol)) (bool2int(new_sol[j] > old_sol[j]));
   
function var int: wins_b(array[int] of var int: old_sol, array[int] of int: new_sol) = 
   sum(j in 1..length(new_sol)) (bool2int(new_sol[j] > old_sol[j]));
   
function var int: losses_a(array[int] of int: old_sol, array[int] of var int: new_sol) = 
   sum(j in 1..length(new_sol)) (bool2int(new_sol[j] < old_sol[j]));
   
function var int: losses_b(array[int] of var int: old_sol, array[int] of int: new_sol) = 
   sum(j in 1..length(new_sol)) (bool2int(new_sol[j] < old_sol[j]));
   
function var int: net_a(array[int] of int: old_sol, array[int] of var int: new_sol) = 
   wins_a(old_sol, new_sol) - losses_a(old_sol, new_sol);
   
function var int: net_b(array[int] of var int: old_sol, array[int] of int: new_sol) = 
   wins_b(old_sol, new_sol) - losses_b(old_sol, new_sol);

function var int: copeland_pos(array[int, int] of int: old_sols, array[int] of var int: new_sol) =
   sum(i in index_set_1of2(old_sols)) (net_a([old_sols[i,j]|j in index_set_2of2(old_sols)],new_sol) > 0);
   
function var int: copeland_neg(array[int, int] of int: old_sols, array[int] of var int: new_sol) =
   sum(i in index_set_1of2(old_sols)) (net_b(new_sol,[old_sols[i,j]|j in index_set_2of2(old_sols)]) > 0);
   
function var int: copeland(array[int, int] of int: old_sols, array[int] of var int: new_sol) =
   copeland_pos(old_sols, new_sol) - copeland_neg(old_sols, new_sol);
%-----------------------------------------------------------------------
  
constraint forall(i in index_set_1of2(old_sols))(copeland(old_sols, new_sol) > copeland(old_sols, [old_sols[i,j]|j in index_set_2of2(old_sols)]));

solve satisfy;
