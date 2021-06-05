import os, sys

# Local
from scope import *


class State:
    def __init__(self):
        self.scope = Scope()
        self.ftable = FunctionTable()
        self.heap = None

if __name__ == "__main__":
    while(True):
        command = input(">> ")
        print(command)
    