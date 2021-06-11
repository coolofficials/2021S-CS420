# TODO: Printf

# -----------------------------------------------------------------------------------------------
# Helper functions.
# TODO: Temporary error_handler.
def syntaxError():
    pass


# A helper for lexing.
# Wrap code into class CodeBlock.
# TODO: break down into a list of statements.
class CodeBlock:
    def __init__(self, code):
        # Store CodeBlock without leading & trailing whitespaces.
        self.code = code.strip()

    # Return first word of CodeBlock.
    def getFirstWord(self):
        return self.code.split(" ")[0]

    # Return index of end char of first word of CodeBlock.
    def getFirstWordIdx(self):
        index = 0
        while self.code[index] != " " and index < len(self.code):
            index += 1
        return index - 1

    # Return index and character of next character from input index.
    def getNextChar(self, index):
        index += 1
        if index > len(self.code):
            syntaxError()
        while self.code[index] == " ":
            index += 1
        if index > len(self.code):
            syntaxError()
        return {"idx": index, "char": self.code[index]}

    # Return next word and last index of it.
    def getNextWord(self, index):
        index += 1
        while self.code[index] == " ":
            index += 1
        if index > len(self.code):
            syntaxError()
        start = index
        index += 1
        if index > len(self.code):
            syntaxError()
        while self.code[index] != " ":
            index += 1
        if index > len(self.code):
            syntaxError()
        return {"idx": index - 1, "word": self.code[start, index]}

    # Note that this method is vague but enough for our implementation.
    # To be precise, check {, (, [ in different way.
    def parenthesesMatching(self, index):
        if not self.code[index] in {"{", "(", "["}:
            print("Not a parentheses")
        depth = 1
        index += 1
        while depth > 0:
            if self.code[index] in {"{", "(", "["}:
                depth += 1
            elif self.code[index] in {"}", ")", "]"}:
                depth -= 1
            index += 1

        if index > len(self.code):
            syntaxError()

        return index - 1


def getStatements(code):
    pass


# -----------------------------------------------------------------------------------------------
# Sub-types of Statements.
# -----------------------------------------------------------------------------------------------
#
# Declaration: type("int", "float") identifier;
# Return: return (expr)
# If: if (condition: expr) {then stmts} else(if any) {else stmts}
# For: for (initializer: expr; condition: expr; step: expr) {stmts}
# Function: type("int", "float") identifier (params: declaration) {stmt}
# Expression: Expressions.
# -----------------------------------------------------------------------------------------------


class Statement:
    def __init__(self):
        self.tag = "Statement"
        self.child = None

    # Parse into sub-types.
    # Make class code and make parentheses matching by index of opening, and keyword.
    def parse(self, statement):
        stmt = CodeBlock(statement)

        # if-else control flow.
        # if (condition) {statements} else {statements}.
        # No 'else if', but nested if-else allowed.
        if stmt.getFirstWord() == "if":
            # A pivot tracing statement.
            # Searching for condition.
            next = stmt.getNextChar(stmt.getFirstWordIdx())
            if next["char"] != "(":
                syntaxError()
            cond_start = next["idx"]
            cond_end = stmt.parenthesesMatching(cond_start)
            condition = stmt.code[cond_start + 1, cond_end]

            # Searching for then statement.
            next = stmt.getNextChar(cond_end)
            if next["char"] != "{":
                syntaxError()
            then_start = next["idx"]
            then_end = stmt.parenthesesMatching(then_start)
            then = getStatements(stmt.code[then_start + 1, then_end])

            # Searching for else statement.
            next = stmt.getNextWord(then_end)
            if next["word"] != "else":
                else_ = None
                # If there are something after then statements other than else, raise error.
                if then_end != len(stmt.code) - 1:
                    syntaxError()
            else:
                next = stmt.getNextChar(next["idx"])
                if next["char"] != "{":
                    syntaxError()
                else_start = next["idx"]
                else_end = stmt.parenthesesMatching(else_start)
                else_ = getStatements(stmt.code[else_start + 1, else_end])

                # if there are something after else statements, raise error.
                if else_end != len(stmt.code) - 1:
                    syntaxError()

            self.child = If().parse(condition, then, else_)

        # return expr;
        elif stmt.getFirstWord() == "return":
            if stmt.code[-1] != ";":
                syntaxError()
            expr = stmt.code[stmt.getNextChar(stmt.getFirstWordIdx())["idx"] :]
            self.child = Return().parse(expr)

        # Function or Declaration.
        elif stmt.getFirstWord() in {"int", "float"}:
            type = stmt.getFirstWord()

            # Declartion: type identifier; or type identifier [size] ;
            if stmt.code[-1] == ";":
                next = stmt.getNextWord(stmt.getFirstWordIdx())
                identifier = next["word"]
                next = stmt.getNextChar(next["idx"])
                if next["char"] == ";":
                    if next["idx"] != len(stmt.code) - 1:
                        syntaxError()
                    size = 0
                elif next["char"] == "[":
                    size_end = stmt.parenthesesMatching(next["idx"])
                    size = stmt.code[next["idx"] + 1, size_end]

                    # If there are something after size, raise error.
                    next = stmt.getNextChar(size_end)
                    if next["char"] != ";":
                        syntaxError()
                    if next["idx"] != len(stmt.code) - 1:
                        syntaxError()

                else:
                    syntaxError()

                self.child = Declaration().parse(type, identifier, size)

            # Function: type identifier (parameters) {statements}
            elif stmt.code[-1] == "}":
                next = stmt.getNextWord(stmt.getFirstWordIdx())
                identifier = next["word"]
                next = stmt.getNextChar(next["idx"])

                # No params following identifier, raise error.
                if next["char"] != "(":
                    syntaxError()

                param_start = next["idx"]
                param_end = stmt.parenthesesMatching(param_start)
                # TODO: breakdown stmts.
                parameters = getStatements(stmt.code[param_start + 1, param_end])
                next = stmt.getNextChar(param_end)
                if next["char"] != "{":
                    syntaxError()

                body_start = next["idx"]
                body_end = stmt.parenthesesMatching(body_start)
                body = getStatements(stmt.code[body_start + 1, body_end])
                if body_end != len(stmt.code) - 1:
                    syntaxError()

                self.child = Function().parse(type, identifier, parameters, body)

        # For control flow.
        elif stmt.getFirstWord() == "for":
            next = stmt.getNextChar(stmt.getFirstWordIdx())
            if next["char"] != "(":
                syntaxError()
            for_states_start = next["idx"]
            for_states_end = stmt.parenthesesMatching(for_states_start)
            for_states = getStatements(stmt.code[for_states_start + 1, for_states_end])
            if len(for_states) != 3:
                syntaxError()
            initializer = for_states[0]
            condition = for_states[1]
            step = for_states[2]
            next = stmt.getNextChar(for_states_end)
            if next["char"] != "{":
                syntaxError()

            body_start = next["idx"]
            body_end = stmt.parenthesesMatching(body_start)
            body = getStatements(stmt.code[body_start + 1, body_end])
            if body_end != len(stmt.code) - 1:
                syntaxError()

            self.child = For().parse(initializer, condition, step, body)

        else:
            self.child = Expression().parse(stmt.code)

        return self


# Expressions: Calculations (UnaryOp, BinaryOp) / Factors (Identifier, FunctionCall, Constant)
# Precedence.
class Expression:
    def __init__(self):
        self.tag = "Expression"
        self.child = None

    # Parse into sub-types.
    # Get expr as list of words(tokens).
    # 0) wrap () into a token.
    # 1) Detect operator and types.
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
        else:
            SyntaxError()

        return self

    def is_lvalue(self):
        return self.child.is_lvalue


class Declaration:
    def __init__(self):
        self.tag = "Declaration"
        self.type = None
        self.identifier = None
        self.size = None

    # type = {"int", "float"}, identifier: consider naming convention, size: if any (default: None).
    # Check whether if size is integer or not.
    def parse(self, type, identifier, size):
        if type not in {"int", "float"}:
            syntaxError()
        self.type = type
        self.identifier = Identifier().parse(identifier)
        self.size = Statement().parse(size)

        return self


class Return:
    def __init__(self):
        self.tag = "Return"
        self.expr = None

    # expr: as string.
    def parse(self, expr):
        self.expr = Statement().parse(expr)
        if self.expr.child.tag != "Expression":
            syntaxError()

        return self


class If:
    def __init__(self):
        self.tag = "If"
        self.condition = None
        self.then = []
        self.else_ = []

    def parse(self, condition, then, else_):
        self.condition = Statement().parse(condition)
        if self.condition.child.tag != "Expression":
            syntaxError()
        for stmt in then:
            self.then.append(Statement().parse(stmt))
        for stmt in else_:
            self.else_.append(Statement().parse(stmt))

        return self


class For:
    def __init__(self):
        self.tag = "For"
        self.initializer = None
        self.condition = None
        self.step = None
        self.statements = []

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
        self.tag = "Function"
        self.type = None
        self.identifier = None
        self.parameters = []
        self.statements = []

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

# pre++, pre--, post++, post--, sizeof, *, &, +, -, ~, !
class UnaryOp:
    def __init__(self):
        self.tag = "UnaryOp"
        self.operator = None

        # Statement(Expression)
        self.operand = None

        self.is_lvalue = False

    def parse(self, operator, operand):
        self.operator = operator
        self.operand = Statement().parse(operand)

        if self.operand.child.tag != "Expression":
            syntaxError()

        if operator in {"pre++", "pre--", "post++", "post--", "&"}:
            if not self.operand.child.is_lvalue():
                syntaxError()

        # Need to check type in runtime.
        if operator == "*":
            self.is_lvalue = True

        return self


# +, -, *, /, %, ==, <=, >=, >, <, ^, &, &&, |, ||, a[b], <<, >>, !=, =, *=, >>=, <<=, -=, +=, &=, ^=, |=
class BinaryOp:
    def __init__(self):
        self.tag = "BinaryOp"
        self.operator = None
        self.lhs = None
        self.rhs = None
        self.is_lvalue = False

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
            if not self.lhs.child.is_lvalue():
                syntaxError()
            self.is_lvalue = False

        # Size check in runtime.
        if operator == "index":
            if not self.lhs.child.is_lvalue():
                syntaxError()
            self.is_lvalue = True

        return self


# 'name:string (arguments:list of Statement(Expression))'
class FunctionCall:
    def __init__(self):
        self.tag = "FunctionCall"
        self.name = None
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
        self.name = None
        self.is_lvalue = True

    def parse(self, name):
        # Need to follow naming convention.
        if not name.isidentifier():
            syntaxError()

        self.name = name

        return self


# C constants: Integer, Float. No character, no string literal.
class Constant:
    def __init__(self):
        self.tag = "Constant"
        self.type = None
        self.value = None
        self.is_lvalue = False

    def parse(self, constant):
        self.value = constant

        if constant == float(constant):
            self.type = "float"

        if constant == int(constant):
            self.type = "int"

        return self


# -----------------------------------------------------------------------------------------------
