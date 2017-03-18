import dis
from collections import deque


class PythonVM:
    def __init__(self):
        self._stack = deque()
        self._globals = {}
        self._locals = {}

    def push(self, value):
        self._stack.pushleft(value)

    def pop(self):
        return self._stack.popleft()

    def eval(self, bytecode):
        insts = dis.get_instructions(bytecode)
        for inst in insts:
            opcode = inst.opcode
            if opcode == 'NOP':
                pass
            # General instructions
            elif opcode == 'POP_TOP':
                self.pop()
            elif opcode == 'ROT_TWO':
                a = self.pop()
                b = self.pop()
                self.push(a)
                self.push(b)
            elif opcode == 'ROT_THREE':
                a = self.pop()
                b = self.pop()
                c = self.pop()
                self.push(a)
                self.push(b)
                self.push(c)
            elif opcode == 'DUP_TOP':
                a = self.pop()
                self.push(a)
                self.push(a)
            elif opcode == 'DUP_TOP_TWO':
                a = self.pop()
                b = self.pop()
                self.push(b)
                self.push(a)
                self.push(b)
                self.push(a)
