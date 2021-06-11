import os, sys

# Local
from state import *

def parse_cli(cli):
    tokens = cli.split()
    if len(tokens) == 0:
        return False, None, None
    
    cmd = tokens[0].lower()
    if (cmd == "help"):
        print(
            "next [LINES]\n"
            "print VARIABLE\n"
            "trace VARIABLE\n"
            "mem\n"
            "exit"
        )
        return False, None, None
    
    elif (cmd == "next"):
        msg = "Incorrect command usage : try \'next [lines]\'"
        lines = 0
        if len(tokens) == 1:
            lines = 1
        elif len(tokens) > 2:
            None
        elif not tokens[1].isdigit():
            None
        else:
            lines = int(tokens[1])
        
        if lines <= 0:
            print(msg)
            return False, None, None
        else:
            return True, "next", lines
        
    elif (cmd == "print" or cmd == "trace"):
        msg1 = "Incorrect command usage : try \'{} [variable]\'".format(cmd)
        msg2 = "Invalid typing of the variable name"
        id = None
        if len(tokens) != 2:
            print(msg1)
            None
        elif not tokens[1].isidentifier():
            print(msg2)
            None
        else:
            id = tokens[1]
        
        return bool(id), cmd, id
    
    elif (cmd == "mem"):
        msg = "Incorrect command usage : try \'mem\'"
        valid = (len(tokens) == 1)
        if not valid:
            print(msg)
        
        return valid, cmd, None
    
    elif (cmd == "exit"):
        msg = "Incorrect command usage : try \'exit\'"
        valid = (len(tokens) == 1)
        if not valid:
            print(msg)
        
        return valid, cmd, None
    
    else:
        print("Incorrect command usage: try \'help\'")
        return False, None, None


if __name__ == "__main__":
    state = State([])
    
    do_next_loop = True
    while(do_next_loop):
        cli = input(">> ")
        valid, cmd, arg = parse_cli(cli)
        
        if not valid:
            None
        else:
            if (cmd == "exit"):
                do_next_loop = False
            else:
                if (cmd == "next"):
                    state.do_next_lines(arg)
                elif (cmd == "print"):
                    state.scope.history.print(arg)
                elif (cmd == "trace"):
                    state.scope.history.trace(arg)
                elif (cmd == "mem"):
                    state.heap.mem()