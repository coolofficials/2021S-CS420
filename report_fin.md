# CS420 Term Project Final Report

### 20130117 Kim, Siwon. 20150608 Lee, Jun Hyeong. 20160625 Cho, Min Jun.

## Project Design

We have written two separate programs to interpret the input code: the Pasrer and the Runtime Simulator.       
The Interpreter parses through the input code, written in the Mini-C language. If the input code has no syntactical errors, it will be converted into an AST structure.     
The AST structure is passed on to the AST Parser, which will simulate and demonstrate the "runtime" environment of the input code, according to the command line inputs.        
However our implementation fails to correctly simulate many features of the C language, and there is no feature to pass the AST from the parser to the simulator.

## Parser

### Fully implemented AST (parser2.py).
`AST(code: raw c code)` will return list of abstract syntax trees having each statements as a root node.

#### Not yet implemented features

Printf  
FunctionCall  
Binary&UnaryOp -> remove whitespaces between operator characters will correct every errors. 

## Runtime Simulator (Debugger)

### State

The Runtime Simulator maintains the information used to simulate the Runtime in a `State` object. The `State` keeps track of the following members:

* The `Scope`, which consists of the `History` of declared variables, and the `Function Table` of declared functions.
  * The `History` is the table of declared variables in a given *Scope*. Each entry must hold the variable identifier and the records of all the value assignments that were done to it. Each record of value assignment must hold its line number and the assigned value.
  * The `Function Table` is the list of declared functions in a given *Scope*. Each entry must hold the function identifier and a function context.
* The `Heap`, which is holds the state of the dynamically allocated memory space. The `malloc` and `free` function calls in the input code will alter the *Heap* state.
* `statements`, which is the list of statements (instructions) to execute, in sequential order.
* `ip`, which indicates the next statement among *statements* to execute.
* `goback`, which is a queue of `Scope`, `ip`, and `statements`. These data are utilized to handle change in control flow.

The code for the above features would be as below:

    class State:
    def __init__(self, statements):
        self.scope = Scope() # consists of History and FunctionTable
        self.heap = Heap()
        self.statements = statements
        self.ip = 0
        self.goback = deque()


## Runtime Simulator (Debugger)

### State

The Runtime Simulator maintains the information used to simulate the Runtime in a `State` object. The `State` keeps track of the following members:

* The `Scope`, which consists of the `History` of declared variables, and the `Function Table` of declared functions.
  * The `History` is the table of declared variables in a given *Scope*. Each entry must hold the variable identifier and the records of all the value assignments that were done to it. Each record of value assignment must hold its line number and the assigned value.
  * The `Function Table` is the list of declared functions in a given *Scope*. Each entry must hold the function identifier and a function context.
* The `Heap`, which is holds the state of the dynamically allocated memory space. The `malloc` and `free` function calls in the input code will alter the *Heap* state.
* `statements`, which is the list of statements (instructions) to execute, in sequential order.
* `ip`, which indicates the next statement among *statements* to execute.
* `goback`, which is a queue of `Scope`, `ip`, and `statements`. These data are utilized to handle change in control flow.

The code for the above features would be as below:

    class State:
    def __init__(self, statements):
        self.scope = Scope() # consists of History and FunctionTable
        self.heap = Heap()
        self.statements = statements
        self.ip = 0
        self.goback = deque()

### Executing Statements

The `State` executes one statement in `statements` via the `execute_stmt` method, and finds the next statement to execute via the `advance_stmt` method. The `advance_stmt` detects whether there are any more statments to execute in `statements`, and if there is none, checks the `goback` queue. If `goback` is not empty, a change in control flow must be made, and the last entry is `pop()`ed. The simulator currently does this for "for" loops and "if-else" statements. Returns from function calls must also be handled, but our simulator currently does not handles this case and therefore function calls are not supported.       
There is one small difference between our simulator and the gdb debugger. The gdb debugger evaluates the condition of a for loop on the "next" command *after* each iterations, whereas our implementation does that right after the end of each iteration, *before* the following "next" command is called. This means if an error occurs during evaluating the condition, our simulator will terminate one line earlier than gdb.

#### Evaluating Expressions

During runtime, the simulator evaluates various `Expressions`. This is done by the `evaluate` method, which supports various forms of `Expressions` such as variables and operations. Various mathmatical, logical, and bitwise operations are supported by our simulator. However, arrays are not supported.

#### Implementing "next"

The debugger command `next [LINES]` must cause the simulator to execute and advance through all statements in the next `LINES` code-lines. This is done by checking the `line_number` member of each `Statement`, and calling `execute_stmt()` and `advance_stmt()` for the next `LINES` distinct values of `line_number`.

    def do_next_lines(self, lines):
        for i in range(lines):
            if not self.do_next_line():
                print("End of Program")
                break
    
    def do_next_line(self):
        if len(self.statements) <= self.ip:
            # advance_stmt() will leave self.ip in this state
            # only if End of Program is reached
            return False
        
        stmt = self.statements[self.ip]
        cur_line_number = stmt.line_number
        while True:
            self.execute_stmt()
            self.advance_stmt()
            if len(self.statements) <= self.ip:
                # advance_stmt() will leave self.ip in this state
                # only if End of Program is reached
                return True
            else:
                stmt = self.statements[self.ip]
                if stmt.line_number != cur_line_number:
                    return True

If the user tries to advance through the program even after it has terminated, i.e. both `statements` and `goback` is empty, the simulator will print out the message `"End of Program"`.

Now lets take a closer look at each of the above features.

### Scope

The `Scope` reflects the "transparency" at the current position in the program. For example, local variables declared and assigned inside a block or a function should not be trackable after exiting the block or returning from the function.

    {
        int x;
        x = 10
    }
    printf("%d", x); // ERROR!
   
The above is an example of change in `Scope`. The variable `x`, defined in the local block, cannot be accessed after the program exists from the block, and any attempt to do so results in an error.       
The `Scope` consists of two objects: `History`, and `FunctionTable`.        


    class Scope:
        def __init__(self):
            self.history = History()
            self.ftable = FunctionTable()


### History

The `History` object keeps track of variable declarations and assignments. Each `History` object holds a `table` member, which is a dictionary object that has variable identifiers as keys and lists of `HistoryEntry` objects as values. Note that our simulator currently does not support arrays.     
Each `HistoryEntry` object represents one declaration, and its following assignments. Note that one identifier might be mapped to multiple `HistoryEntry`s. This is in the C language, a variable may be declared multiple times, such as the below snippet.

    # This is valid C code!
    int x;
    x = 1;
    float x;
    x = 2.0;
    int x;
    x = 3;

A `HistoryEntry` must keep track of one declaration and any number of value assignments; the former is stored in the `type` member, and the latter is tracked by the `log` member.     
The member `log` is a list of assigned values, and the `line_number`s of the assignments in the original C code. The `line_number` must be stored in order to process the debugger commands `print` and `trace`. 

    class HistoryEntry:
        def __init__(self, type_, layer = 0):
            # id (str): identifier of variable
            # type_: type of variable
            # layer (int): scope of declaration; 0 means local
            self.type = type_
            self.layer = layer
            self.log = list()

From the above code, you can see that a `HistoryEntry` object also stores a number in the member `layer`. This member represents the "locality" of each declarations, and is maintained to correctly handle variable transparencies on changes of `Scope`. Take the below code snippet as an example.

    int x;
    x = 10;
    printf("%d\n", x); // 10
    {
        x = 20;
        float x;
        x = 1.0;
        printf("%f\n",x); // 1.0
    }
    printf("%d\n", x); // 20

The variable `x` was declared and assigned as `int` type in the outer scope, and re-declared as `float` type in the inner scope. After exiting the block, all history after the re-declaration as `float` must be discarded. Yet, the re-assignment *before* the re-declaration (i.e. `x = 20;`) must not be nullified.     
Our implementation handles cases such as these by utilizing the `layer` member of the `HistoryEntry` class. On declaration, the `HistoryEntry` object has `layer` initialized to 0; which means the declaration has taken place in the "current" scope. When the scope is "lowered", i.e. the program enters a relatively "local" scope such as blocks and function calls, all `HistoryEntry`s tracked inside `History` have their `layer` incremented by one. When the scope is "elevated", i.e. the program exists a local scope, all `HistoryEntry`s have their `layer` decremented by one. At this stage, some `HistoryEntry`s might have negative `layer` values. This means that they represent declarations made in the exited scope, and must be deleted. This process is handled by the `deepcopy` method of the `HistoryEntry` class.

    def deepcopy(self, delta_layer = 0):
            # deepcopy()s the current scope (i.e. self), 
            # and modifies layer values of all entries by delta_layer
            # removes entry if the altered layer value is less than 0 
            history =  copy.deepcopy(self)
            if delta_layer != 0:
                for id in history.table:
                    for idx, hte in enumerate(history.table[id]):
                        hte.layer += delta_layer
                        if hte.layer < 0:
                            del history.table[id][idx]
                delkeys = deque()
                for idx, id in enumerate(history.table):
                    if len(history.table[id]) == 0:
                        delkeys.append(id)
                while delkeys:
                    del history.table[delkeys.pop()]

#### Implementing "print"

When the debugger command `print ID` is called, the simulator checks whether the string `ID` is a valid identifier string. If so, it looks up the `History` in the current `Scope` to see if `ID` is a declared variable. If no match is found, The message `"Invisible variable"` is printed out.      
If a match is found, the debugger takes the last `HistoryEntry` object for the given `ID`. If the `log` of the `HistoryEntry` is empty, it means that the variable was declared but not yet assigned a value. In this case, the message `"N/A"` is printed out. If `log` is not empty, the simulator prints out the latest assigned value.

#### Implementing "trace"
When the debugger command `trace ID` is called, the simulator checks whether the string `ID` is a valid identifier string. If so, it looks up the `History` in the current `Scope` to see if `ID` is a declared variable. If no match is found, The message `"Invisible variable"` is printed out.      
If a match is found, the debugger takes the last `HistoryEntry` object for the given `ID`. If the `log` of the `HistoryEntry` is empty, it means that the variable was declared but not yet assigned a value. In this case, the message `"N/A"` is printed out. If `log` is not empty, the simulator prints out *all* of the assigned values with their `line_number`s.     
Note that, only the values after the __last__ declaration will be printed out. For example, with the below code snippet,

    int x; # line 1
    x = 10; # line 2
    x = 20; # line 3
    float x; # line 4
    x = 30.0; # line 5

If the command `trace x` was called after all 5 lines have been executed, the output will only print out the following.

    x = 30.0 at line 5

## FunctionTable

The `FunctionTable` is an abstraction of the list of functions declared in the given C code. A `FunctionTable` maintains a mapping of function identifiers and their meta-data. When a function definition is made, the simulator searches for entries with duplicate function identifiers. If no such entry is found, the function identifier is added to the `FunctionTable`, along with the corresponding return type, parameters (names and types), function body, and a copy of the current `Scope`.

    class FunctionTableEntry:
        def __init__(self, id, return_type, line_number, parameters, statements):
            self.id = id
            self.type = return_type
            self.line_number = line_number
            self.parameters = parameters
            self.statements = statements
            self.scope = None # Needs to be assigned by the caller, e.g. FunctionTable.define()
    
    class FunctionTable:
      def define(self, function, scope):
          if function.id in self.table: raise RuntimeError()
          fte = FunctionTableEntry(
              function.id,
              function.return_type,
              function.line_number,
              function.parameters, # Declarations
              function.statements,
          )
          # copy scope at definition; recursion is not possible
          fte.scope = copy.deepcopy(scope)

When a function call is made, the simulator evaluates the values of the arguments. After that, it validates the identifier of the called function and the number of parameters. If validity is confirmed, the arguments are type-casted into the types of the parameters. Now a manipulation of `Scope` and a change in control flow must be made, but this process is incomplete. Therefore, function calls are currently not supported by our simulator.

## Dynamic Memory Management

We must keep track of the heap structure for memory management. Maximum size of saving data is 1KB, and malloc and free uses virtual memory address as an argument. Virtual address is decided by adding available offset in virtual memory table `self.table2` and 0x100000 which is `base_address` of VM. Allocated virtual address of each variables never change until free command occurs.
Address of the variable and allocating size will be saved in `self.dic` in heap structure. In heap structure, some important functions needed to be declared as sub-functions of the heap for memory management which is coded in `memory.py` is as below:

```
class Heap:
    malloc (self, size):
        ...
    free (self, var):
        ...        
    mem (self):
        ...
dynamic_allocation (self, size):
        ...
```

* `malloc`: The function call `malloc(size)` in the input code invokes a call to `x = heap.malloc(size)` method at Runtime. The method to find possible n size of memory space for variable x. `self.table2` is used for getting virtual address for allocated space. If malloc successes, it returns the virtual address.
Two possible errors might occur: the `size` might be a negative value, or there might be not enough space left in the heap. If there is no enough space for such size, execute defragmentation in the memory space. If the defragmentation process fails or there is still not enough memory left, it returns 0(which will print “Out of memory”). If `size` is a negative value, it returns 0(which will print “size_t should be a positive integer”).
* `free`: The function call `free(var)` in the input code invokes a call to `heap.free(var)` method at Runtime. The method will deallocate memory space corresponding to `var` which is the address of such variable. If there is no allocated space for address `var`, it returns 0(which will print “not allocated address”).
* `mem`, The command line `mem` invokes a call to `heap.mem()` method in runtime. This will print out the message “Dynamic allocation : x, y” where x is the number of allocated variables and y is the total memory size of the allocated space.
* ` dynamic_allocation`, The function call `self.dynamic_allocation(self, size)` in the code `memory.py` is called to defragment the memory space when there is not enough space left for size `size` in the memory. When defragmentation occurs, the data moves forward and it updates `self.dic` for changed offset `off`. The table `self.table` moves with it too.
 If this function is called, it prints “defragmentation operated”.
