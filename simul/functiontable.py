class FunctionTableEntry:
    def __init__(self, id, return_type, line_number, parameters, statements):
        self.id = id
        self.type = return_type
        self.line_number = line_number
        self.parameters = parameters
        self.statements = statements

class FunctionTable:
    def __init__(self):
        self.table = list()