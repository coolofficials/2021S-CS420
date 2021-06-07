from linter import lint

# List of statements.
# 1) Assignment: 'variable = value;'
# 2) Function: 'type identifier(parameter: types) {}'
# 3) Declaration: 'type variable;'
# 4) For: 'for (variable: iterator; condition; step) {}'
# 5) If: 'if (Condition) {}'
# 6) Return: 'return ~;'
# 7) Printf: 'printf ();'
# 8) Free: 'free ();'


def getFirstWord(string):
    return string.split(" ")[0]


def getSecondWord(string):
    return string.split(" ")[1]


# AST().parse(source) will return a list of ASTs from a given C file.
class AST:
    def __init__(self) -> None:
        # Store list of linted lines from source code.
        self.codes = []

        # Store list of statements with getStatements().
        self.roots = []

    # Get source C file and split into lines of codes, lint and store as a list of strings.
    # source: path of source C file.
    def sourceLine(self, source):
        f = open(source, "r")
        self.codes = lint([line.rstrip("\n") for line in f])

    # Get Statement class items by parsing.
    def getStatements(self):
        while self.codes:
            code_line = self.codes.pop(0)
            if code_line[-1] == ";":
                body = [code_line]
                statement = Statement()
                statement.parse(body)
                self.roots.append(statement)

            # TODO: Need to handle better for nested for, if, function, etc. (Count { and }).
            elif code_line[-1] == "{":
                body = []
                while code_line != "}":
                    body.append(code_line)
                    code_line = self.codes.pop(0)
                body.append(code_line)
                Statement(body)
                self.roots.append(Statement().parse(body))

    # Generate a list a ASTs, root of each AST is each statement of source.
    def parse(self, source):
        self.sourceLine(source)
        self.getStatements()


class Statement:
    # Get a list of lines of codes.
    def __init__(self):
        # Child node by parsing.
        self.child
        self.tag = "Statement"

    # Perform appropriate parsing for the statement.
    # body: A list of lines of code.
    # TODO: parse, especially parsing statements... handle nested parenthesis.
    def parse(self, body):
        key = getFirstWord(body[0])

        # TODO: statements.
        if key == "if":
            # get conditions and body.
            # body[0] = 'if (conditon) {'
            # body[1~-2] = self.child.body, statements.
            # body[-1] = '}'
            self.child = If()
            self.child.parse(condition, statements)

        # TODO: statements.
        elif key == "for":
            # body[0] = 'for (initializer: assignment; condition: expr; step: expr) {'
            # body[1~-2] = self.child.body, statements.
            # body[-1] = '}'
            self.child = For()
            self.child.parse(initializer, condition, step, statements)

        # Done
        elif key == "return":
            # body[0] = 'return expr;'
            expr = body[0].split(" ", 1)[1][:-1]
            self.child = Return()
            self.child.parse(expr)

        # TODO: get token
        elif key == "printf":
            # body[0] = 'printf(token);'
            self.child = Printf()
            self.child.parse(token)

        # Done
        elif key == "Free":
            # body[0] = 'free (variable);'
            variable = body[0].split(" ", 1)[1][1:-2]
            self.child = Free()
            self.child.parse(variable)

        # TODO: get params & statements.
        elif key in {"int", "float"} and body[0][-1] == "{":
            # body[0] = 'int/float identifier (parameters) {'
            signature = key
            identifier = getSecondWord(body[0])
            self.child = Function()
            self.child.parse(signature, identifier, parameters, statements)

        # Done
        elif key in {"int", "float"}:
            # body[0] = 'int/float identifier;'
            signature = key
            identifier = getSecondWord(body[0])
            self.child = Declaration()
            self.child.parse(signature, identifier)

        # Done
        elif getSecondWord(body[0]) == "=":
            # body[0] = 'identifier = expr;'
            identifier = body[0].split(" ")[0]
            expr = body[0].split(" ", 2)[2][:-1]
            self.child = Assignment()
            self.child.parse(identifier, expr)

        # Done
        else:
            # body[0] = 'expr;'
            expr = body[0][:-1]
            self.child = Expression()
            self.child.parse(expr)


# Done
class If:
    def __init__(self):
        self.condition
        self.statements = []
        self.tag = "If"

    def parse(self, condition, statements):
        self.condition = Statement()
        self.condition.parse([condition])
        if self.condition.child.tag != "Expression":
            # TODO: explicit error handler.
            print("syntax error")
        for statement in statements:
            self.statements.append(Statement().parse(statement))


# Done
class For:
    def __init__(self):
        self.initializer
        self.condition
        self.step
        self.statements = []
        self.tag = "For"

    def parse(self, initializer, condition, step, statements):
        self.initializer = Assignment()
        self.initializer.parse(initializer)
        self.condition = Expression()
        self.condition.parse(condition)
        self.step = Expression()
        self.step.parse(step)
        for statement in statements:
            stmt = Statement()
            stmt.parse(statement)
            self.statements.append(stmt)


# Done
class Return:
    def __init__(self):
        self.expr
        self.tag = "Return"

    def parse(self, expr):
        self.expr = Expression()
        self.expr.parse(expr)


# TODO: Specify Token
class Printf:
    def __init__(self):
        self.token
        self.tag = "Printf"

    def parse(self, token):
        self.token = token


# TODO: variable?
class Free:
    def __init__(self):
        self.variable
        self.tag = "Free"

    def parse(self, variable):
        self.variable = Variable()
        self.variable.parse(variable)


# Done
class Declaration:
    def __init__(self):
        self.signature
        self.identifier
        self.tag = "Declaration"

    def parse(self, signature, identifier):
        self.signature = signature
        self.identifier = identifier


# TODO: parameters?
class Function:
    def __init__(self):
        self.signature
        self.identifier
        self.parameters = []
        self.statements = []
        self.tag = "Function"

    def parse(self, signature, identifier, parameters, statements):
        self.signature = signature
        self.identifier = identifier
        for param in parameters:
            parameter = Parameter()
            parameter.parse(param)
            self.parameters.append(parameter)
        for statement in statements:
            stmt = Statement()
            stmt.parse(statement)
            self.statements.append(stmt)


# Done
class Assignment:
    def __init__(self):
        self.identifier
        self.expr
        self.tag = "Assignment"

    def parse(self, identifier, expr):
        self.identifier = identifier
        self.expr = Expression().parse(expr)


# TODO: specify classification
class Expression:
    def __init__(self):
        self.type
        self.tag = "Expression"

    def parse(self, expr):
        pass


# TODO from here.
class Calculation:
    def __init__(self):
        self.type
        self.tag = "Calculation"

    def parse(self):
        pass


class BinaryOp:
    def __init__(self, statement):
        self.type
        self.tag = "BinaryOp"

    def parse(self):
        pass


class UnaryOp:
    def __init__(self, statement):
        self.type
        self.tag = "UnaryOp"

    def parse(self):
        pass


class Factor:
    def __init__(self, statement):
        self.type
        self.tag = "Factor"

    def parse(self):
        pass


class Parameter:
    def __init__(self):
        self.tag = "Parameter"

    def parse(self):
        pass


class Variable:
    def __init__(self, statement):
        self.type
        self.tag = "Variable"

    def parse(self):
        pass


class Constant:
    def __init__(self, statement):
        self.type
        self.tag = "Constant"

    def parse(self):
        pass


class FunctionCall:
    def __init__(self, statement):
        self.type
        self.tag = "FunctionCall"

    def parse(self):
        pass


input = ["if(i<=0){", "a<1;", "}"]
classifier = {"return", "printf", "free", "if", "for", "int", "float"}


print(getFirstWord("if (i == 0) {"))
