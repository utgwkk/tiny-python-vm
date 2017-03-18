import dis
import collections.abc
import ast
from collections import deque


class ConstantOrNameCollector(ast.NodeVisitor):
    def __init__(self, co_names, co_consts):
        ast.NodeVisitor.__init__(self)
        self.co_names = co_names
        self.co_consts = co_consts

    def visit_Name(self, node):
        self.co_names.append(node.id)

    def visit_Num(self, node):
        self.co_consts.append(node.n)

    def visit_Str(self, node):
        self.co_consts.append(node.s)


class PythonVM:
    def __init__(self):
        self._stack = deque()
        self._globals = {}
        self._locals = {}
        self.co_names = []
        self.co_consts = []

    def push(self, value):
        self._stack.appendleft(value)

    def pop(self):
        return self._stack.popleft()

    def eval(self, bytecode):
        _ast = ast.parse(bytecode)
        # Store names and constants into co_names and co_consts
        ConstantOrNameCollector(self.co_names, self.co_consts).visit(_ast)

        # Add None to the end of co_consts if not exists
        if None not in self.co_consts:
            self.co_consts.append(None)

        # Get information of bytecode
        insts = dis.get_instructions(bytecode)
        for inst in insts:
            opname = inst.opname
            arg = inst.arg
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
            # Miscellaneous opnames
            elif opname == 'RETURN_VALUE':
                tos = self.pop()
                return tos
            elif opname == 'LOAD_CONST':
                self.push(self.co_consts[arg])
            # Not implemented operator
            else:
                raise NotImplementedError(
                    'the opname `{}` is not implemented.'.format(opname)
                )
