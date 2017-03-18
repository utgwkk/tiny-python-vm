import dis
import collections.abc
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
            # Unary operations
            elif opcode == 'UNARY_POSITIVE':
                a = self.pop()
                self.push(+a)
            elif opcode == 'UNARY_NEGATIVE':
                a = self.pop()
                self.push(-a)
            elif opcode == 'UNARY_NOT':
                a = self.pop()
                self.push(not a)
            elif opcode == 'UNARY_INVERT':
                a = self.pop()
                self.push(~a)
            elif opcode == 'GET_ITER':
                a = self.pop()
                self.push(iter(a))
            elif opcode == 'GET_YIELD_FROM_ITER':
                a = self.pop()
                # If TOS is a generator iterator or coroutine object
                if any([isinstance(a, collections.abc.Generator),
                        isinstance(a, collections.abc.AsyncGenerator),
                        ]):
                    self.push(a)
                else:
                    self.push(iter(a))
            # Binary operations
            elif opcode == 'BINARY_POWER':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 ** tos)
            elif opcode == 'BINARY_MULTIPLY':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 * tos)
            elif opcode == 'BINARY_MATRIX_MULTIPLY':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 @ tos)
            elif opcode == 'BINARY_FLOOR_DIVIDE':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 // tos)
            elif opcode == 'BINARY_TRUE_DIVIDE':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 / tos)
            elif opcode == 'BINARY_MODULO':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 % tos)
            elif opcode == 'BINARY_ADD':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 + tos)
            elif opcode == 'BINARY_SUBTRACT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 - tos)
            elif opcode == 'BINARY_SUBSCR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1[tos])
            elif opcode == 'BINARY_LSHIFT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 << tos)
            elif opcode == 'BINARY_RSHIFT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 >> tos)
            elif opcode == 'BINARY_AND':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 & tos)
            elif opcode == 'BINARY_XOR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 ^ tos)
            elif opcode == 'BINARY_OR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 | tos)
            # Not implemented operator
            else:
                raise NotImplementedError(
                    'the opcode `{}` is not implemented.'.format(opcode)
                )
