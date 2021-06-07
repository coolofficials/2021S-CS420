from collections import deque

# Local
from scope import *


class State:
    def __init__(self, statements):
        self.scope = Scope()
        # self.history = History()
        # self.ftable = FunctionTable()
        self.heap = None
        self.statements = statements
        self.ip = 0
        self.goback = deque()
    
    def next(self):
        if self.ip >= len(self.statements):
            if(not self.goback):
                print("End of Program")
            else:
                # out of a block
                self = self.goback.pop()
                stmt = self.statements[self.ip]
                if (stmt.tag == "for"):
                    # goto stmt.fin, then evaluate condition
                    
                    # difference with gdb:
                    # gdb will evaluate condition on the following "next" command,
                    # whereas our implementation does that right now.
                    # this means if an error occurs during condition evaluation,
                    # our simulator will terminate one line earlier than gdb.
                    
                    forblk = stmt
                    self.do(forblk.fin)
                    if bool(forblk.condition.eval()):
                        self.goback.append(self) # deepcopy?
                        self.ip = 0
                        self.statements = forblk.body
                    else:
                        self.ip += 1
        
        else:
            stmt = self.statements[self.ip]
            self.do(stmt)
            self.ip += 1
        
        return self
    
    def do(self, stmt, aux = None):
        if (stmt.tag == "function"):
            function = stmt
            self.ftable.define(
                function,
                self.scope
            )
        
        elif (stmt.tag == "declaration"):
            decl = stmt
            self.scope.history.declare(
                decl.id,
                decl.type
            )
        
        elif (stmt.tag == "assignment"):
            asgn = stmt
            self.scope.history.assign(
                asgn.id,
                asgn.constant,
                asgn.line_number
            )
        
        elif (stmt.tag == "for"):
            forblk = stmt
            forblk.initial
        
        