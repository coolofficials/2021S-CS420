# CS420 Term Project: 21May Report

### 20130117 Kim, Siwon. 20150608 Lee, Jun Hyeong. 20160625 Cho, Min Jun.

## Project Design

We will write two separate programs to interpret the input code: the interpreter and the AST parser.       
The interpreter will parse through the input code, written in the Mini-C language. If the input code has no syntactical errors, it will be converted into an AST structure.     
The AST structure will be passed on to the AST Parser, which will simulate the "runtime" of the 