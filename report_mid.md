# CS420 Term Project: 21May Report

### 20130117 Kim, Siwon. 20150608 Lee, Jun Hyeong. 20160625 Cho, Min Jun.

## Project Design

We will write two separate programs to interpret the input code: the Interpreter and the AST Parser.       
The Interpreter will parse through the input code, written in the Mini-C language. If the input code has no syntactical errors, it will be converted into an AST structure.     
The AST structure will be passed on to the AST Parser, which will simulate and demonstrate the "runtime" environment of the input code, according to the command line inputs.

## Parser (AST Generator)

The parser will generate the AST from the input source code. Few parts AST structures are as below.

```
Statement{
    int line_number,
    Statement-subtypes,
}

Statement-subtypes{
    Expression,
    Function,
    Declaration,
    Assignment,
    For, 
    If,
    Return,
    Printf,
    Free,
}

Expression-subtypes{
    Calculation (including Comparisons),
    Factor,
    Malloc,
}

Calculation sub-types{
    BinaryOp,
    UnaryOp,
}

BinaryOp{
    BinaryOp-subtypes,
    Expression operand_first,
    Expression operand_last,
}

BinaryOp-subtypes{
    Add,
    Subt,
    Mult,
    Div,
    Greater,
    Less
}

Function{
    string identifier,
    string return_type, // int or float.
    int end_line,
    list<Parameter> parameters,
    list<Statement> statements, 
}

Parameter{
    string type, // int or float.
    string identifier,
}

Return{
    Expression,
}

Declaration{
    string type, // int or float.
    string identifier,
}

Assignment{
    identifier variable,
    Expression value,
}

Factor{
    FunctionCall,
    Constant,
    Variable,
}

FunctionCall{
    string identifer,
    list<Expression> arguments,
}

Constant{
    string type, // int or float.
    type value, // for corresponding type.
}

Variable{
    string type, // for type checking.
    string identifier,
}

Printf{
    list<Token> format,
    list<Expression> arguments,
}
```

### Test cases of input codes and their AST outputs

For example, the AST for 

```
line 1: a + b;
```

will be
```
Statement{
    line_number: 1,
    Expression{
        Calculation{
            BinaryOp{
                Add,
                a,
                b,
            }
        }
    }
}
```

and the AST for
```
line 12: int add(int a, int b){
line 13: return a + b
line 14: }
```

will be
```
Statement{
    line_number: 12,
    Expression{
        Function{
            identifier: add,
            return_type: int,
            end_line: 14,
            parameters:[Parameter{type:int, identifier: a}, Parameter{type:int, identifier: b}],
            statements:[Statement{line_number: 13, Return{Expression{Calculation{BinaryOp{Add, a, b,}}}}}}]
        }
    }
}
```

For a strip of code including the `main` function:
```
line 20: int main(){
line 21:    int a;
line 22:    a = add(5, 10);
line 23:    printf(a);
line 24:    return 0;
line 25: }
```

the corresponding AST structure is:
```
Statement{
    line_number: 20,
    Expression{
        Function{
            identifier: main,
            return_type: int,
            end_line: 25,
            parameters:[],
            statements:[Statement{line_number: 21, Declaration{type: int, identifier: a}}, Statement{line_number: 22, Assignment{variable: a, value: Expression{Factor{FunctionCall{identifier: add, arguments: [Expression{Factor{Constant{type: int, value: 5}}}, Expression{Factor{Constant{type: int, value: 10}}}]}}}}},
            Statement{line_number: 23, Printf{format: [], arguments: Expression{Factor{Variable{type: int, identifier: a}}}}}, Statement{line_number: 24, Return{Expression{Factor{Constant{type: int, value: 0}}}}},
            ]
        }
    }
}
```

### Syntax Error Checking

The Interpreter must also do syntax checking. The Interpreter will not return AST for input codes with syntactical errors.
```
line 20: int main(){
line 21:    int a;
line 22:    a = add(5, ); // Syntax Error!
line 23:    printf(a);
line 24:    return 0;
line 25: }
```

```
Syntax error: line 22
```


## Runtime Simulator (Debugger)

### Runtime Context Structures

The Runtime Simulator needs to keep track of the following additional contexts:

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

The `Scope` (which contains the `History` and the `Function_Table`) and the `Heap` will both dynamically change as the Simulator iterates through the `Statement`s in the AST.     
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
      }while(statment_to_do.line_number == cur_line)\


## Dynamic Memory Management

We must keep track of the heap structure for memory management. Data type for heap is list<address, size>. Address of the variable and allocating size will be saved in heap structure. In heap structure, some functions are needed to be declared as sub-functions of the heap for memory management as below:
```
class Heap:
    __init__ (self, ..):
        ...
        
    malloc(self, size):
        ...
    
    free (addr):
        ...
        
    mem (addr):
        ...
        print("Dynamic allocation : {}, {}\n".format( .., ..))
```

* Function *malloc*, for given specific size of memory field, x = malloc(heap, n) command should be able to find possible n size of memory space for variable x. Two possible errors might occur: size of malloc(heap, size) should be a positive value, and a memory space corresponding to the size must remain in the heap(Out Of Memory error).
* Function *free*, free(x) should be able to deallocate memory space corresponding to variable x. Defragmentation is operated in free() function. If the defragmentation process fails or there is no memory allocated to variable x, it returns -1.
* Function *mem*, mem command prints “Dynamic allocation : x, y” where x is the number of allocated variables and y is total currently allocated memory size.
