# Local
from history import *
from functiontable import *

class Scope:
    def __init__(self):
        self.history = History()
        self.ftable = FunctionTable()
    
    def deepcopy(self, delta_layer = 0):
        scope = Scope()
        scope.history = self.history.deepcopy(delta_layer)
        scope.ftable = copy.deepcopy(self.ftable)
        return scope
