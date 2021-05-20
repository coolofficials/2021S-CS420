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
            parameters:[Parameter{type: int, identifier: a}, Parameter{type: int, identifier: b}],
            statements:[Statement{line_number: 13, Return{Expression{Calculation{BinaryOp{Add, a, b,}}}}}}]
        }
    }
}
```
