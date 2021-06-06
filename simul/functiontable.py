import copy

class FunctionTableEntry:
    def __init__(self, id, return_type, line_number, parameters, statements):
        self.id = id
        self.type = return_type
        self.line_number = line_number
        self.parameters = parameters
        self.statements = statements
        self.context = None # Needs to be assigned by the caller

class FunctionTable:
    def __init__(self):
        self.table = list()
    
    def define(self, function, context):
        fte = FunctionTableEntry(
            function["id"],
            function["return_type"],
            function["line_number"],
            function["parameters"],
            function["statements"],
        )
        # copy context at definition; recursion is not possible
        fte.context = copy.deepcopy(context)
        
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
                context = copy.deepcopy(func.context)
                for (argument, parameter) in zip(arguments, func.parameters):
                    if argument["type"] != parameter["type"]:
                        # might be parameter[1]; depends on AST implementation
                        raise RuntimeError(None)
                
                # function context is returned "as is"
                # parameter values should be assigned by caller
                return func.context, func.return_type, func.line_number, func.parameters, func.statements
