### Parser implementation.

- We will generate AST from source code. Partial expample of AST structure will be as below.

```
Statement{
    int line_number,
    Statement-subtypes,
}

Statement-subtypes{
    Expression,
    Function,
    Declaration,
    Assignment,
    For, 
    If,
    Return,
    Printf,
    Free,
}

Expression-subtypes{
    Calculation (including Comparisons),
    Factor,
    Malloc,
}

Calculation sub-types{
    BinaryOp,
    UnaryOp,
}

BinaryOp{
    BinaryOp-subtypes,
    Expression operand_first,
    Expression operand_last,
}

BinaryOp-subtypes{
    Add,
    Subt,
    Mult,
    Div,
    Greater,
    Less
}

Function{
    string identifier,
    string return_type, // int or float.
    int end_line,
    list<Parameter> parameters,
    list<Statement> statements, 
}

Parameter{
    string type, // int or float.
    string identifier,
}

Return{
    Expression,
}

Declaration{
    string type, // int or float.
    string identifier,
}

Assignment{
    identifier variable,
    Expression value,
}

Factor{
    FunctionCall,
    Constant,
    Variable,
}

FunctionCall{
    string identifer,
    list<Expression> arguments,
}

Constant{
    string type, // int or float.
    type value, // for corresponding type.
}

Variable{
    string type, // for type checking.
    string identifier,
}

Printf{
    list<Token> format,
    list<Expression> arguments,
}
```

For example, AST for 

```
line 1: a + b;
```

will be
```
Statement{
    line_number: 1,
    Expression{
        Calculation{
            BinaryOp{
                Add,
                a,
                b,
            }
        }
    }
}
```

and AST for
```
line 12: int add(int a, int b){
line 13: return a + b
line 14: }
```

will be
```
Statement{
    line_number: 12,
    Expression{
        Function{
            identifier: add,
            return_type: int,
            end_line: 14,
            parameters:[Parameter{type:int, identifier: a}, Parameter{type:int, identifier: b}],
            statements:[Statement{line_number: 13, Return{Expression{Calculation{BinaryOp{Add, a, b,}}}}}}]
        }
    }
}
```

Code including `main` function:
```
line 20: int main(){
line 21:    int a;
line 22:    a = add(5, 10);
line 23:    printf(a);
line 24:    return 0;
line 25: }
```

Corresponding AST:
```
Statement{
    line_number: 20,
    Expression{
        Function{
            identifier: main,
            return_type: int,
            end_line: 25,
            parameters:[],
            statements:[Statement{line_number: 21, Declaration{type: int, identifier: a}}, Statement{line_number: 22, Assignment{variable: a, value: Expression{Factor{FunctionCall{identifier: add, arguments: [Expression{Factor{Constant{type: int, value: 5}}}, Expression{Factor{Constant{type: int, value: 10}}}]}}}}},
            Statement{line_number: 23, Printf{format: [], arguments: Expression{Factor{Variable{type: int, identifier: a}}}}}, Statement{line_number: 24, Return{Expression{Factor{Constant{type: int, value: 0}}}}},
            ]
        }
    }
}
```
AST generation will include syntax checking. For code having Syntax Error, AST will not be returned.
```
line 20: int main(){
line 21:    int a;
line 22:    a = add(5, ); // Syntax Error!
line 23:    printf(a);
line 24:    return 0;
line 25: }
```

```
Syntax error: line 22
```
