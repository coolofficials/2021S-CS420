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
                self.roots.append(Statement().parse(body))

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

    # Perform appropriate parsing for the statement.
    # body: A list of lines of code.
    # TODO: parse, especially parsing statements... handle nested parenthesis.
    def parse(self, body):
        key = getFirstWord(body[0])
        if key == "if":
            # get conditions and body.
            # body[0] = 'if (conditon) {'
            # body[1~-2] = self.child.body, statements.
            # body[-1] = '}'
            self.child = If().parse(condition, statements)
        elif key == "for":
            # body[0] = 'for (initializer: assignment; condition: expr; step: expr) {'
            # body[1~-2] = self.child.body, statements.
            # body[-1] = '}'
            self.child = For().parse(initializer, condition, step, statements)

        # Done
        elif key == "return":
            # body[0] = 'return expr;'
            expr = body[0].split(" ", 1)[1][:-1]
            self.child = Return().parse(expr)

        # TODO: get token
        elif key == "printf":
            # body[0] = 'printf(token);'
            self.child = Printf().parse(token)

        # Done
        elif key == "Free":
            # body[0] = 'free (variable);'
            variable = body[0].split(" ", 1)[1][1:-2]
            self.child = Free().parse(variable)

        # TODO: get params & statements.
        elif key in {"int", "float"} and body[0][-1] == "{":
            # body[0] = 'int/float identifier (parameters) {'
            signature = key
            identifier = getSecondWord(body[0])
            self.child = Function().parse(signature, identifier, parameters, statements)

        # Done
        elif key in {"int", "float"}:
            # body[0] = 'int/float identifier;'
            signature = key
            identifier = getSecondWord(body[0])
            self.child = Declaration().parse(signature, identifier)

        # Done
        elif getSecondWord(body[0]) == "=":
            # body[0] = 'identifier = expr;'
            identifier = body[0].split(" ")[0]
            expr = body[0].split(" ", 2)[2][:-1]
            self.child = Assignment().parse(identifier, expr)

        # Done
        else:
            # body[0] = 'expr;'
            expr = body[0][:-1]
            self.child = Expression().parse(expr)


# Done
class If:
    def __init__(self):
        self.condition
        self.statements = []

    def parse(self, condition, statements):
        self.condition = Expression().parse(condition)
        for statement in statements:
            self.statements.append(Statement().parse(statement))


# Done
class For:
    def __init__(self):
        self.initializer
        self.condition
        self.step
        self.statements = []

    def parse(self, initializer, condition, step, statements):
        self.initializer = Assignment().parse(initializer)
        self.condition = Expression().parse(condition)
        self.step = Expression().parse(step)
        for statement in statements:
            self.statements.append(Statement().parse(statement))


# Done
class Return:
    def __init__(self):
        self.expr

    def parse(self, expr):
        self.expr = Expression().parse(expr)


# TODO: Specify Token
class Printf:
    def __init__(self):
        self.token

    def parse(self, token):
        self.token = token


# TODO: variable?
class Free:
    def __init__(self):
        self.variable

    def parse(self, variable):
        self.variable = Variable().parse(variable)


# Done
class Declaration:
    def __init__(self):
        self.signature
        self.identifier

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

    def parse(self, signature, identifier, parameters, statements):
        self.signature = signature
        self.identifier = identifier
        for param in parameters:
            self.parameters.append(Parameter().parse(param))
        for statement in statements:
            self.statements.append(Statement().parse(statement))


# Done
class Assignment:
    def __init__(self):
        self.identifier
        self.expr

    def parse(self, identifier, expr):
        self.identifier = identifier
        self.expr = Expression().parse(expr)


# TODO: specify classification
class Expression:
    def __init__(self):
        self.type

    def parse(self, expr):
        pass


# TODO from here.
class Calculation:
    def __init__(self):
        self.type

    def parse(self):
        pass


class BinaryOp:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


class UnaryOp:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


class Factor:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


class Parameter:
    def __init__(self):
        pass

    def parse(self):
        pass


class Variable:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


class Constant:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


class FunctionCall:
    def __init__(self, statement):
        self.type

    def parse(self):
        pass


input = ["if(i<=0){", "a<1;", "}"]
classifier = {"return", "printf", "free", "if", "for", "int", "float"}


print(getFirstWord("if (i == 0) {"))
