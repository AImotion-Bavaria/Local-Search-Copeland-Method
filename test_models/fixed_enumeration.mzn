% Use this editor as a MiniZinc scratch book
include "table.mzn";

var 0..10: x;
var 0..10: y;
var 0..10: line;

constraint table([line, x,y], 
  [|1,  1, 3 | 2,  4, 2 | 3,   5, 5 |]);

solve 
:: int_search([line], input_order, indomain_min, complete)
satisfy;