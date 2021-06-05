import copy

class HistoryEntry:
    def __init__(self, type_, native=True):
        # id (str): identifier of variable
        # type_: type of variable
        # native (bool): defined in this scope
        self.type = type_
        self.native = native
        self.history = list()
    
    def updateVal(self, line_number, val):
        self.history.append((line_number, val))
        

class History:
    def __init__(self):
        self.table = dict()
    
    def declare(self, id, type_):
        # id (str): identifier of variable
        if id not in self.table:
            self.table[id] = list()
            self.table[id].append(HistoryEntry(type_, True))
        else:
            if self.table[id][-1].native:
                raise RuntimeError("redefinition of \'{}\'".format(id))
            else:
                self.table[id].append(HistoryEntry(type_, True))
    
    def assign(self, id, constant, line_number):
        if id not in self.table:
            raise RuntimeError("\'{}\' undeclared".format(id))
        else:
            he = self.table[id][-1]
            if he.type == constant["type"]:
                he.updateVal(line_number, constant["value"])
            else:
                raise RuntimeError("type mismatch")
                # TODO: type-casting
    
    def print(self, id):
        if id not in self.table:
            # Not defined
            print("Invisible variable")
        
        else:
            he = self.table[id]
            if he.history:
                # Defined and assigned
                print(he.history[-1][1])
            else:
                # Defined yet not assigned
                print("N/A")
        
        # TODO: type-checking
        # Pointers should print "Invalid typing of the variable name"
            
    
    def trace(self, id):
        if id not in self.table:
            # Not defined
            print("Invisible variable")
        
        else:
            he = self.table[id][-1]
            if he.history:
                # Defined and assigned
                
                # Dilemma: what to do if variable had value(s) assigned,
                # but was re-declared in the current scope and was not assigned?
                # For now, only trace the assignments after the last declaration.
                
                # for he in self.table[id]:
                for line_number, val in he.history:
                    print("{} = {} at line {}".format(id, val, line_number))
            else:
                # Defined yet not assigned
                print("N/A")
        
        # TODO: type-checking
        # Pointers should print "Invalid typing of the variable name"
        
    def deepcopy(self):
        # custom deepcopy, alias of deepcopy in copy module
        return copy.deepcopy(self)