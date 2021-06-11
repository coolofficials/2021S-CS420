# Abort Printf, Free, Malloc.

# -----------------------------------------------------------------------------------------------
# Helper functions.
# TODO: Temporary error_handler.
def syntaxError():
    pass


# -----------------------------------------------------------------------------------------------
class Statement:
    def __init__(self):
        # TODO: Temporary assign
        self.child = Expression()
        pass

    def parse(self):
        return self


# -----------------------------------------------------------------------------------------------
# Sub-types of Statements.
# -----------------------------------------------------------------------------------------------
# 0) Expression: some code line gives value.
# 1) Assignment: 'variable = value;'
# 2) Function: 'type identifier(parameter: types) {}'
# 3) Declaration: 'type variable;'
# 4) For: 'for (variable: iterator; condition; step) {}'
# 5) If: 'if (Condition) {}'
# 6) Return: 'return Statement(Expression);'

# Expressions: Calculations (UnaryOp, BinaryOp) / Factors (Identifier, FunctionCall, Constant)
class Expression:
    def __init__(self):
        self.tag = "Expression"
        self.child

    # Parse into sub-types.
    def parse(self, expr):
        # TODO: Temporary assignment of sub-types.
        if expr == "UnaryOp":
            self.child = UnaryOp().parse()
        elif expr == "BinaryOp":
            self.child = BinaryOp().parse(0, 0, 0)
        elif expr == "FunctionCall":
            self.child = FunctionCall().parse(0, 0)
        elif expr == "Identifier":
            self.child = Identifier().parse(0)
        elif expr == "Constant":
            self.child = Constant().parse(0)

        return self

    def is_lvalue(self):
        return self.child.is_lvalue


class Declaration:
    def __init__(self):
        self.type
        self.identifier
        self.size
        self.tag = "Declaration"

    # type = {"int", "float"}, identifier: consider naming convention, size: if any (default: None).
    def parse(self, type, identifier, size):
        if type not in {"int", "float"}:
            syntaxError()
        self.type = type
        self.identifier = Identifier().parse(identifier)
        self.size = size

        return self


class Return:
    def __init__(self):
        self.expr
        self.tag = "Return"

    # expr: as string.
    def parse(self, expr):
        self.expr = Statement().parse(expr)
        if self.expr.child.tag != "Expression":
            syntaxError()

        return self


class If:
    def __init__(self):
        self.condition = []
        self.then = []
        self.else = []
        self.tag = "If"

    def parse(self, condition, then, else):
        self.condition = Statement().parse(condition)
        if self.condition.child.tag != "Expression":
            syntaxError()
        for stmt in then:
            self.then.append(Statement().parse(stmt))
        for stmt in else:
            self.else.append(Statement().parse(stmt))
        
        return self


class For:
    def __init__(self):
        self.initializer
        self.condition
        self.step
        self.statements = []
        self.tag = "For"

    def parse(self, initializer, condition, step, statements):
        self.initializer = Statement().parse(initializer)
        if self.initializer.child.tag != "Expression":
            syntaxError()
        self.condition = Statement().parse(condition)
        if self.condition.child.tag != "Expression":
            syntaxError()
        self.step = Statement().parse(step)
        if self.step.child.tag != "Expression":
            syntaxError()
        for stmt in statements:
            self.statements.append(Statement().parse(stmt))

        return self


class Function:
    def __init__(self):
        self.type
        self.identifier
        self.parameters = []
        self.statements = []
        self.tag = "Function"

    def parse(self, type, identifier, parameters, statements):
        if type not in {"int", "float"}:
            syntaxError()
        self.type = type
        self.identifier = Identifier().parse(identifier)
        for param in parameters:
            parameter = Statement().parse(param)
            if parameter.child.tag != "Declaration":
                syntaxError()
            self.parameters.append(parameter)
        for stmt in statements:
            self.statements.append(Statement().parse(stmt))
            
        return self


# -----------------------------------------------------------------------------------------------
# Sub-types of Expressions.
#
# 1) UnaryOp
# 2) BinaryOp
# 3) FunctionCall
# 4) Identifier
# 5) Constant
# -----------------------------------------------------------------------------------------------

# pre++, pre--, post++, post--, sizeof(?), *, &, +, -, ~, !
class UnaryOp:
    def __init__(self):
        self.tag = "UnaryOp"
        self.operator

        # Statement(Expression)
        self.operand

        self.is_lvalue = False

    def parse(self, operator, operand):
        self.operator = operator
        self.operand = Statement().parse(operand)

        if self.operand.child.tag != "Expression":
            syntaxError()

        if operator in {"pre++", "pre--", "post++", "post--", "&", "*"}:
            if not self.operand.child.is_lvalue():
                syntaxError()

        return self


# +, -, *, /, %, ==, <=, >=, >, <, ^, &, &&, |, ||, a[b], <<, >>, !=, =, *=, >>=, <<=, -=, +=, &=, ^=, |=
class BinaryOp:
    def __init__(self):
        self.tag = "BinaryOp"
        self.operator
        self.lhs
        self.rhs
        self.is_lvalue

    def parse(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = Statement().parse(lhs)
        self.rhs = Statement().parse(rhs)

        if self.lhs.child.tag != "Expression":
            syntaxError()

        if self.rhs.child.tag != "Expression":
            syntaxError()

        if operator in {
            "<=",
            ">=",
            "!=",
            "=",
            "*=",
            "+=",
            "-=",
            "/=",
            "%=",
            "&=",
            "|=",
            "^=",
            "<<=",
            ">>=",
        }:
            self.is_lvalue = True

            if not self.lhs.child.is_lvalue():
                syntaxError()
        # TODO: Handle index after... use size? -> runtime.
        # if operator == "index":
        #     self.is_lvalue = True

        return self


# 'name:string (arguments:list of Statement(Expression))'
class FunctionCall:
    def __init__(self):
        self.tag = "FunctionCall"
        self.name
        self.arguments = []
        self.is_lvalue = False

    def parse(self, name, arguments):
        # Need to follow naming convention.
        if not name.isidentifier():
            syntaxError()
        self.name = name
        for arg in arguments:
            argument = Statement().parse(arg)

            # Argument should be an expression.
            if argument.child.tag != "Expression":
                syntaxError()

            self.arguments.append(argument)

        return self


# 'name: string'
class Identifier:
    def __init__(self):
        self.tag = "Identifier"
        self.name
        self.is_lvalue = True

    def parse(self, name):
        # Need to follow naming convention.
        if not name.isidentifier():
            syntaxError()

        self.name = name

        return self


# C constants: Integer, Float. No character, no string literal.
class Constant:
    def __init__(self, type_ = None, value = None):
        self.tag = "Constant"
        self.type = type_
        self.value = value
        self.is_lvalue = False
    

    def parse(self, constant):
        self.value = constant

        if constant == float(constant):
            self.type = "Float"

        if constant == int(constant):
            self.type = "Int"

        return self
    
    def sum(const_a, const_b):
        if const_a.type not in ["int", "float"]: raise RuntimeError()
        if const_b.type not in ["int", "float"]: raise RuntimeError()
        if const_a.type == "float" or const_b.type == "float":
            return Constant(
                "float",
                float(const_a.value + const_b.value)
            )
        else:
            return Constant(
                "int",
                int(const_a.value + const_b.value)
            )
    
    def subt(const_a, const_b):
        if const_a.type not in ["int", "float"]: raise RuntimeError()
        if const_b.type not in ["int", "float"]: raise RuntimeError()
        if const_a.type == "float" or const_b.type == "float":
            return Constant(
                "float",
                float(const_a.value - const_b.value)
            )
        else:
            return Constant(
                "int",
                int(const_a.value - const_b.value)
            )
    
    def mult(const_a, const_b):
        if const_a.type not in ["int", "float"]: raise RuntimeError()
        if const_b.type not in ["int", "float"]: raise RuntimeError()
        if const_a.type == "float" or const_b.type == "float":
            return Constant(
                "float",
                float(const_a.value * const_b.value)
            )
        else:
            return Constant(
                "int",
                int(const_a.value * const_b.value)
            )
    
    def div(const_a, const_b):
        if const_a.type not in ["int", "float"]: raise RuntimeError()
        if const_b.type not in ["int", "float"]: raise RuntimeError()
        if const_a.type == "float" or const_b.type == "float":
            return Constant(
                "float",
                float(const_a.value / const_b.value)
            )
        else:
            return Constant(
                "int",
                int(const_a.value / const_b.value)
            )
    
    def remain(const_a, const_b):
        if const_a.type != "int": raise RuntimeError()
        if const_b.type != "int": raise RuntimeError()
        return Constant(
            "int",
            int(const_a.value % const_b.value)
        )
    
    def and(const_a, const_b):
        if const_a.type != "int": raise RuntimeError()
        if const_b.type != "int": raise RuntimeError()
        return Constant(
            "int",
            int(const_a.value & const_b.value)
        )
    
    def or(const_a, const_b):
        if const_a.type != "int": raise RuntimeError()
        if const_b.type != "int": raise RuntimeError()
        return Constant(
            "int",
            int(const_a.value | const_b.value)
        )
    
    def xor(const_a, const_b):
        if const_a.type != "int": raise RuntimeError()
        if const_b.type != "int": raise RuntimeError()
        return Constant(
            "int",
            int(const_a.value ^ const_b.value)
        )
# -----------------------------------------------------------------------------------------------
