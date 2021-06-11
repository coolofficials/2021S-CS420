from collections import deque

# Local
from scope import *
from parser2 import *

def to_type(value, type_):
    if type_ == "int":
        return int(value)
    elif type_ == "float":
        return float(value)
    else:
        return value

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
                scope_out = scope.deepcopy(-1)
                ip = ip
                statements = statements
                
                chld = statements[ip].child
                if (chld.tag == "For"):
                    # finished iteration of [initializer] or body + [step]
                    # evaluate condition and set ip and scope appropriately
                    
                    # difference with gdb:
                    # gdb will evaluate condition on the following "next" command,
                    # whereas our implementation does that right now.
                    # this means if an error occurs during condition evaluation,
                    # our simulator will terminate one line earlier than gdb.
                    
                    forblk = chld
                    if bool(self.evaluate(forblk.condition, stmt.line_number)):
                        self.ip = 0
                        self.statements = forblk.body + [forblk.step]
                    else:
                        self.scope = scope_out
                        self.statements = statements
                        self.ip = ip + 1
                
                elif (chld.tag == "If"):
                    # finished iteration of then or else
                    # restore ip and statements. increment ip by one.
                    ifblk = chld
                    self.scope = scope_out
                    self.statements = statements
                    self.ip = ip + 1
                
                # TODO: Other cases
    
    def execute_stmt(self, stmt, aux = None):
        chld = stmt.child
        if (chld.tag == "Function"):
            function = chld
            self.ftable.define(
                function,
                self.scope
            )
        
        elif (chld.tag == "Declaration"):
            decl = chld
            self.scope.history.declare(
                decl.identifier,
                decl.type
            )
        
        elif (chld.tag == "Assignment"):
            asgn = chld
            self.scope.history.assign(
                asgn.identifier,
                asgn.constant,
                asgn.line_number
            )
        
        elif (chld.tag == "For"):
            forblk = chld
            self.goback.append(
                (self.scope.deepcopy(0), self.ip, list(self.statements))
            )
            self.scope = self.scope.deepcopy(1)
            self.statements = [forblk.initializer]
            self.ip = 0
        
        elif (chld.tag == "If"):
            ifblk = chld
            condition = ifblk.condition
            condition_result = bool(self.evaluate(condition))
            self.goback.append(
                (self.scope.deepcopy(0), self.ip, list(self.statements))
            )
            if condition_result:
                self.ip = 0
                self.statements = ifblk.then
            else:
                self.ip = 0
                self.statements = ifblk.else
    
    def evaluate(self, expression, line_number):
        chld = expression.child
        
        if (chld.tag == "UnaryOp"):
            self.eval_unary(chld, line_number)
        
        elif (chld.tag == "BinaryOp"):
            self.eval_binary(chld, line_number)
        
        elif (chld.tag == "Variable"):
            self.scope.history.get_const(chld.identifier)
        
        elif (chld.tag == "FunctionCall"):
            self.eval_functioncall(chld, line_number)
    
    def eval_unary(self, unaryop, line_number):
        operator = unaryop.operator
        operand = unaryop.operand.child
        
        ## Currently only supports Identifier for operand
        ## TODO: Array indexing support
        if operator == "pre++":
            const = copy.deepcopy(self.scope.history.get_const(operand.identifier))
            self.scope.history.assign(
                operand.identifier,
                Constant(const.type, const.value + 1),
                line_number
            )
            return const
        
        elif operator == "pre--":
            const = copy.deepcopy(self.scope.history.get_const(operand.identifier))
            self.scope.history.assign(
                operand.identifier,
                Constant(const.type, const.value + 1),
                line_number
            )
            return const
        
        elif operator == "post++":
            const = self.scope.history.get_const(operand.identifier)
            self.scope.history.assign(
                operand.identifier,
                Constant(const.type, const.value + 1),
                line_number
            )
            return copy.deepcopy(self.scope.history.get_const(operand.identifier))
        
        elif operator == "post--":
            const = self.scope.history.get_const(operand.identifier)
            self.scope.history.assign(
                operand.identifier,
                Constant(const.type, const.value + 1),
                line_number
            )
            return copy.deepcopy(self.scope.history.get_const(operand.identifier))
        
        elif operator == "&":
            #TODO
            return None
        
        elif operator == "*":
            #TODO
            return None
        
    def eval_binary (self, binaryop, line_number):
        operator = binaryop.operator
        left = binaryop.lhs.child
        right = binaryop.rhs.child
        
        if operator == "<=":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            return Constant(
                "int",
                int(left_const.value <= right_const.value)
            )
        
        elif operator == "<":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            return Constant(
                "int",
                int(left_const.value < right_const.value)
            )
        
        elif operator == ">=":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            return Constant(
                "int",
                int(left_const.value >= right_const.value)
            )
        
        elif operator == "==":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            return Constant(
                "int",
                int(left_const.value == right_const.value)
            )
        
        elif operator == "!=":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            return Constant(
                "int",
                int(left_const.value != right_const.value)
            )
        
        elif operator == "+":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            # if left_const.type not in ["int", "float"]: raise RuntimeError()
            # if right_const.type not in ["int", "float"]: raise RuntimeError()
            if left_const.type == "float" or right_const.type == "float":
                return Constant(
                    "float",
                    float(left_const.value + right_const.value)
                )
            else:
                return Constant(
                    "int",
                    int(left_const.value + right_const.value)
                )
        
        elif operator == "-":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            # if left_const.type not in ["int", "float"]: raise RuntimeError()
            # if right_const.type not in ["int", "float"]: raise RuntimeError()
            if left_const.type == "float" or right_const.type == "float":
                return Constant(
                    "float",
                    float(left_const.value - right_const.value)
                )
            else:
                return Constant(
                    "int",
                    int(left_const.value - right_const.value)
                )
        
        elif operator == "*":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            # if left_const.type not in ["int", "float"]: raise RuntimeError()
            # if right_const.type not in ["int", "float"]: raise RuntimeError()
            if left_const.type == "float" or right_const.type == "float":
                return Constant(
                    "float",
                    float(left_const.value * right_const.value)
                )
            else:
                return Constant(
                    "int",
                    int(left_const.value * right_const.value)
                )
        
        elif operator == "/":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            # if left_const.type not in ["int", "float"]: raise RuntimeError()
            # if right_const.type not in ["int", "float"]: raise RuntimeError()
            if left_const.type == "float" or right_const.type == "float":
                return Constant(
                    "float",
                    float(left_const.value / right_const.value)
                )
            else:
                return Constant(
                    "int",
                    int(left_const.value / right_const.value)
                )
        
        elif operator == "%":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(left_const.value % right_const.value)
            )
        
        elif operator == "^":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(left_const.value ^ right_const.value)
            )
        
        elif operator == "&":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(left_const.value & right_const.value)
            )
        
        elif operator == "|":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(left_const.value | right_const.value)
            )
        
        elif operator == "&&":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(bool(left_const.value) and bool(right_const.value))
            )
        
        
        elif operator == "||":
            left_const = self.evaluate(left, line_number)
            right_const = self.evaluate(right, line_number)
            
            if left_const.type != "int": raise RuntimeError()
            if right_const.type != "int": raise RuntimeError()
            
            return Constant(
                "int",
                int(bool(left_const.value) or bool(right_const.value))
            )
        
        elif operator == "=":
            # if not left.is_lvalue: raise RuntimeError()
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                self.scope.history.assign(
                    left.identifier,
                    right_const
                )
                return right_const
        
        elif operator == "+=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.sum(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
        
        elif operator == "-=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.subt(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
        
        elif operator == "*=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.mult(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
        
        elif operator == "&=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.and(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
        
        elif operator == "|=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.or(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
        
        elif operator == "^=":
            if left.child.tag == "Identifier":
                right_const = self.evaluate(right, line_number)
                left_const = self.scope.get_const(left.identifier)
                ret_const = Constant.xor(left_const, right_const)
                self.scope.history.assign(
                    left.identifier,
                    ret_const
                )
                return ret_const
    
    def eval_functioncall(self, function_call, line_number):
        function_call