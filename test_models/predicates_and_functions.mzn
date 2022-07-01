var 1..10: x;
var 1..10: y; 
var 1..10: z;

predicate x_greater_by2_than_y(var int: x, var int: y) = 
 x = y + 2;
constraint x_greater_by2_than_y(x, y);

function var int: double_input(var int: x) = 
  x * 2;

constraint z = double_input(x);

solve satisfy;