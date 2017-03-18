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
            opname = inst.opname
            if opname == 'NOP':
                pass
            # General instructions
            elif opname == 'POP_TOP':
                self.pop()
            elif opname == 'ROT_TWO':
                a = self.pop()
                b = self.pop()
                self.push(a)
                self.push(b)
            elif opname == 'ROT_THREE':
                a = self.pop()
                b = self.pop()
                c = self.pop()
                self.push(a)
                self.push(b)
                self.push(c)
            elif opname == 'DUP_TOP':
                a = self.pop()
                self.push(a)
                self.push(a)
            elif opname == 'DUP_TOP_TWO':
                a = self.pop()
                b = self.pop()
                self.push(b)
                self.push(a)
                self.push(b)
                self.push(a)
            # Unary operations
            elif opname == 'UNARY_POSITIVE':
                a = self.pop()
                self.push(+a)
            elif opname == 'UNARY_NEGATIVE':
                a = self.pop()
                self.push(-a)
            elif opname == 'UNARY_NOT':
                a = self.pop()
                self.push(not a)
            elif opname == 'UNARY_INVERT':
                a = self.pop()
                self.push(~a)
            elif opname == 'GET_ITER':
                a = self.pop()
                self.push(iter(a))
            elif opname == 'GET_YIELD_FROM_ITER':
                a = self.pop()
                # If TOS is a generator iterator or coroutine object
                if any([isinstance(a, collections.abc.Generator),
                        isinstance(a, collections.abc.AsyncGenerator),
                        ]):
                    self.push(a)
                else:
                    self.push(iter(a))
            # Binary operations
            elif opname == 'BINARY_POWER':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 ** tos)
            elif opname == 'BINARY_MULTIPLY':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 * tos)
            elif opname == 'BINARY_MATRIX_MULTIPLY':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 @ tos)
            elif opname == 'BINARY_FLOOR_DIVIDE':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 // tos)
            elif opname == 'BINARY_TRUE_DIVIDE':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 / tos)
            elif opname == 'BINARY_MODULO':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 % tos)
            elif opname == 'BINARY_ADD':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 + tos)
            elif opname == 'BINARY_SUBTRACT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 - tos)
            elif opname == 'BINARY_SUBSCR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1[tos])
            elif opname == 'BINARY_LSHIFT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 << tos)
            elif opname == 'BINARY_RSHIFT':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 >> tos)
            elif opname == 'BINARY_AND':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 & tos)
            elif opname == 'BINARY_XOR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 ^ tos)
            elif opname == 'BINARY_OR':
                tos = self.pop()
                tos1 = self.pop()
                self.push(tos1 | tos)
            # Not implemented operator
            else:
                raise NotImplementedError(
                    'the opname `{}` is not implemented.'.format(opname)
                )
