╔═╗╔╦╗╔═╗╔╦╗╔═╗  ╔╦╗╔═╗╔╗ ╦  ╔═╗  
╚═╗ ║ ╠═╣ ║ ║╣    ║ ╠═╣╠╩╗║  ║╣   
╚═╝ ╩ ╩ ╩ ╩ ╚═╝   ╩ ╩ ╩╚═╝╩═╝╚═╝  
╔═╗╔═╗╔╗╔╔═╗╦═╗╔═╗╔╦╗╔═╗╦═╗       
║ ╦║╣ ║║║║╣ ╠╦╝╠═╣ ║ ║ ║╠╦╝       
╚═╝╚═╝╝╚╝╚═╝╩╚═╩ ╩ ╩ ╚═╝╩╚═       
----------------------------------------------------                                     
╦ ╦╔═╗╔═╗╦═╗  ╔╦╗╔═╗╔╗╔╦ ╦╔═╗╦    
║ ║╚═╗║╣ ╠╦╝  ║║║╠═╣║║║║ ║╠═╣║    
╚═╝╚═╝╚═╝╩╚═  ╩ ╩╩ ╩╝╚╝╚═╝╩ ╩╩═╝ 
----------------------------------------------------
(c) 2015, Joshua Isaac Pabilona

- Requires Java 6 >=

A. INSTRUCTIONS ON HOW TO START THE PROGRAM
1. Clone this repository. 
2. Start up a terminal of your choice inside the cloned repository's root directory. 
3. Type in the command line: 'java -jar State_Table_Generator.jar' 
(without the single quotes)

After these steps, the program should start running.

*Some windows devices can just double-click 
the jar to run it, some can't.
If the latter happens, follow the aforementioned
steps.

B. INSTRUCTIONS ON HOW TO USE THE PROGRAM:
* There are tooltips if you hover over the JComponents
To start generating, enter these:
a) Number of flip-flops
Permissible values: positive integers from 1-8 (FLIP-FLOPS ARE REQUIRED) (UP TO A WHOPPING 8!!!!!!!!!!) (((((M E G A B O N U S))))
b) Number of inputs
Permissible values: positive integers from 0-8 (Inputs are optional)  (8!!!!!!)
c) NUmber of outputs 
Permissible values: positive integers from 0-8 (Outputs are optional) (OMG 8 AGAIN!!!! ISN'T THAT AMAZING)

For the flip-flop input functions and output functions:
Only UPPERCASE LETTERS are allowed. 
Parentheses are also handled.
Flip-flop variables can only start from A (CAPTIAL A)
then followed by B (CAPITAL B) then followed by C (CAPITAL C) 
until the last flip-flop has been declared. If this is not followed
then the program could give out faulty outputs.

Input variables are NOT to be inputted as x,y,z; rather,
it should be next letter after the last flip-flop variable.

Ex. 1
2 flip-flops
1 input
1 output

A - flip flop 1
B - flip flop 2
C - input 1

Ex. 2
3 flip-flops
2 inputs
0 outputs
A - flip flop 1
B - flip flop 2
C - flip flop 3
D - input 1
E - input 2

OPERATORS:
. - AND
* - XOR
+ - OR
' - NOT

Example functions:
A' 
A+B'
(A+B)'
A.B + B.C' // AB + BC'
(A*C).(D*(B+C)) //(A XOR C) AND (D XOR(B OR C))

An example run-through of the program:
1. Type inputs
Flip-flop type: D Flip-flop 
Number of Flip-flops: 2
Number of Inputs: 1
Number of Outputs: 1
Flip-flop functions
DA: A.C + B.C 
DB: A'.C
Output functions
Output Function 1: (A+B).C'
*functions taken from module, page 55

2. Click 'Generate State Table'
3. View your state table
4. To continue execution, and enter new input configurations

There is error handling present when:
1) An input field has been left blank
2) Flip-flop quantity has been left blank
3) Mismatched parentheses
4) Users cannot input string values to the spinners

After an error has occurred, the program reverts to its default state.

Open javadoc/index.html to view the app's API.


