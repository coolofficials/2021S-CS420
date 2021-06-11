import copy

from parser2 import *

class FunctionTableEntry:
    def __init__(self, id, return_type, line_number, parameters, statements):
        self.id = id
        self.type = return_type
        self.line_number = line_number
        self.parameters = parameters
        self.statements = statements
        self.scope = None # Needs to be assigned by the caller

class FunctionTable:
    def __init__(self):
        self.table = list()
    
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
        
        self.table.append(fte)
    
    def call(self, function_id, arguments):
        # function_id (str): name of function
        # arguments (list): Constants (not Expressions!)
        
        if function_id not in self.table:
            # Undefined Function
            raise RuntimeError(None)
        
        else:
            # Parameter number and type matching
            func = self.table[function_id]
            if len(arguments) != len(func.parameters):
                raise RuntimeError(None)
            
            else:
                args = list(arguments)
                for (argument, parameter) in zip(arguments, func.parameters):
                    args.append(Constant.totype(argument, parameter.child.type))
                
                # function scope is returned "as is"
                # parameter values should be assigned by caller
                return func.scope, func.return_type, func.parameters, args, func.statements
