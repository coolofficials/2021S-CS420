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
    
    
    def advance_stmt(self):
        if self.ip >= len(self.statements):
            if not self.goback:
                None
            else:
                # change of control flow
                scope, ip, statements = self.goback.pop()
                self.scope = scope.deepcopy(-1)
                self.ip = ip
                self.statements = statements
                
                stmt = self.statements[self.ip]
                if (stmt.tag == "for"):
                    # finished iteration of [initializer] or body + [step]
                    # evaluate condition and set ip and scope appropriately
                    
                    # difference with gdb:
                    # gdb will evaluate condition on the following "next" command,
                    # whereas our implementation does that right now.
                    # this means if an error occurs during condition evaluation,
                    # our simulator will terminate one line earlier than gdb.
                    
                    forblk = stmt
                    if bool(self.evaluate(forblk.condition)):
                        self.goback.append(
                            (self.scope.deepcopy(1), self.ip, list(self.statements))
                        )
                        self.ip = 0
                        self.statements = forblk.body + [forblk.step]
                    else:
                        self.ip += 1
                # TODO: Other cases
    
    def execute_stmt(self, stmt, aux = None):
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