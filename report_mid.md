# CS420 Term Project: 21May Report

### 20130117 Kim, Siwon. 20150608 Lee, Jun Hyeong. 20160625 Cho, Min Jun.

## Project Design

We will write two separate programs to interpret the input code: the Interpreter and the AST Parser.       
The Interpreter will parse through the input code, written in the Mini-C language. If the input code has no syntactical errors, it will be converted into an AST structure.     
The AST structure will be passed on to the AST Parser, which will simulate and demonstrate the "runtime" environment of the input code, according to the command line inputs.

## AST Parser

### Runtime Context Structures

The AST Parser needs to keep track of the following additional contexts:

* The *Scope*, which determines the *History* of declared variables, and the *Function Table* of declared functions.
* The *History*, which is the table of declared variables in a given *Scope*. Each entry must hold the variable identifier and the records of all the value assignments that were done to it. Each record of value assignment must hold its line number and the assigned value.
* The *Function Table*, which is the list of declared functions in a given *Scope*. Each entry must hold the function identifier and a `Function` object.
* The *Heap*, which is holds the state of the dynamically allocated memory space. The `malloc` and `free` function calls in the input code will alter the *Heap* state.

The pseudocode for the above features would be as below:

    typedef struct Scope{
      History history;
      Function_Table function_table;
    } Scope;
    
    typedef map<string, Function> Function_Table;
    
    typedef list<int, Constant> HistoryEntry;
    typedef map<string, HistoryEntry> History;
    
### Tracking the Runtime Context

The `Scope` (which contains the `History` and the `Function_Table`) and the `Heap` will both dynamically change as the Parser iterates through the `Statement`s in the AST.     
But the policy of managing the `Scope` and the `Heap` would be very different; for instance, when a function call returns in the input code, the `Scope` will be restored to that of the callee (except for global variables), but the `Heap` will remain as the same state as it was just before the function return.      

Therefore, we expect the following pseudocode will be effective:
    
    // initialize cur_line, iterator<Statement> it, scope, heap
    
    // on "next (num)" command:
    scope, heap = do_next(it)
    // on "trace (id)" command:
    scope.history.trace(id)
    // on "print (id)" command:
    scope.history.print(id)
    // on "mem" command:
    heap.show_mem()
    
    def do_next(it):
      cur_line++
      do{
          next(it)
          statement_to_do = getItem(it)
          scope, heap = do_statement(statement, scope, heap)
      }while(statment_to_do.line_number == cur_line)