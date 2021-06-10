import copy
from collections import deque

from parser2 import *

class HistoryEntry:
    def __init__(self, type_, layer = 0):
        # id (str): identifier of variable
        # type_: type of variable
        # layer (int): scope of declaration; 0 means local
        self.type = type_
        self.layer = layer
        self.log = list()
    
    def updateVal(self, line_number, val):
        self.log.append((line_number, val))
        

class History:
    def __init__(self):
        self.table = dict()
    
    def declare(self, id, type_):
        # id (str): identifier of variable
        if id not in self.table:
            self.table[id] = list()
            self.table[id].append(HistoryEntry(type_))
        else:
            if self.table[id][-1].layer == 0:
                raise RuntimeError("redeclaration of \'{}\'".format(id))
            else:
                self.table[id].append(HistoryEntry(type_))
    
    def assign(self, id, constant, line_number):
        if id not in self.table:
            raise RuntimeError("\'{}\' undeclared".format(id))
        else:
            hte = self.table[id][-1]
            # if hte.type == constant.type:
            #     hte.updateVal(line_number, constant.value)
            if hte.type == constant["type"]:
                hte.updateVal(line_number, constant["value"])
            else:
                raise RuntimeError("type mismatch")
                # TODO: type-casting
    
    def print(self, id):
        if id not in self.table:
            # Not defined
            print("Invisible variable")
        
        else:
            hte = self.table[id][-1]
            if hte.log:
                # Defined and assigned
                print(hte.log[-1][1])
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
            # Dilemma: what to do if variable had value(s) assigned,
            # but was re-declared in the current scope and was not assigned?
            # For now, only trace the assignments after the last declaration.
            
            hte = self.table[id][-1]
            if hte.log:
                # for he in self.table[id]:
                for line_number, val in hte.log:
                    print("{} = {} at line {}".format(id, val, line_number))
            else:
                # Defined yet not assigned
                print("N/A")
        
        # TODO: type-checking
        # Pointers should print "Invalid typing of the variable name"
        
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
            
        return history
    
    def get_const(self, id):
        if id not in self.table:
            raise RuntimeError()
        else:
            hte = self.table[id][-1]
            return Constant(hte.type , hte.log[-1][1])
    
# if __name__ == "__main__":
#     # Test Code
#     history = History()
#     history.declare("x", "int")
#     history.assign("x", {"type":"int", "value":100}, 1)
#     history.assign("x", {"type":"int", "value":200}, 2)
#     history.print("x")
#     history.trace("x")
#     history = history.deepcopy(-1)
#     history.trace("x")