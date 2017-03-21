import sys
import argparse
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
        if node.id not in self.co_names:
            self.co_names.append(node.id)

    def visit_Num(self, node):
        # XXX: 1 == True
        if not any(x is node.n for x in self.co_consts):
            self.co_consts.append(node.n)

    def visit_Str(self, node):
        if node.s not in self.co_consts:
            self.co_consts.append(node.s)

    def visit_NameConstant(self, node):
        if node.value not in self.co_consts:
            self.co_consts.append(node.value)


class PythonVM:
    def __init__(self, _globals=None, _locals=None):
        self._reset()

    def push(self, value):
        self._stack.appendleft(value)

    def pop(self):
        return self._stack.popleft()

    def _reset(self, _globals=None, _locals=None):
        if _globals is None:
            _globals = globals()
        if _locals is None:
            _locals = {}
        self._stack = deque()
        self.co_blocks = deque()
        self._globals = _globals
        self._locals = _locals
        self.co_names = []
        self.co_consts = []
        self.pc = 0

    def eval(self, bytecode):
        _ast = ast.parse(bytecode)
        # Store names and constants into co_names and co_consts
        ConstantOrNameCollector(self.co_names, self.co_consts).visit(_ast)

        # Add None to the end of co_consts if not exists
        if None not in self.co_consts:
            self.co_consts.append(None)

        # Get information of bytecode
        insts = list(dis.get_instructions(bytecode))
        while self.pc < len(insts):
            inst = insts[self.pc]
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
                # FIXME: what are 'generator iterator' or 'coroutines'
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
            elif opname == 'LOAD_NAME':
                if self.co_names[arg] in self._locals:
                    self.push(self._locals.get(self.co_names[arg]))
                elif self.co_names[arg] in self._globals:
                    self.push(self._globals.get(self.co_names[arg]))
                elif self.co_names[arg] in dir(self._globals['__builtins__']):
                    self.push(getattr(self._globals['__builtins__'], self.co_names[arg]))
                elif isinstance(self._globals['__builtins__'], dict) and self.co_names[arg] in self._globals['__builtins__']:
                    self.push(self._globals['__builtins__'][self.co_names[arg]])
                else:
                    raise NameError("name '{}' is not defined".format(self.co_names[arg]))
            elif opname == 'STORE_NAME':
                tos = self.pop()
                self._locals[self.co_names[arg]] = tos
            elif opname == 'POP_JUMP_IF_TRUE':
                tos = self.pop()
                if tos:
                    self.pc = arg // 2 - 1
            elif opname == 'POP_JUMP_IF_FALSE':
                tos = self.pop()
                if not tos:
                    self.pc = arg // 2 - 1
            elif opname == 'JUMP_FORWARD':
                self.pc += arg // 2
            elif opname == 'JUMP_ABSOLUTE':
                self.pc = arg // 2 - 1
            elif opname == 'SETUP_LOOP':
                self.co_blocks.appendleft((self.pc, self.pc + arg // 2))
            elif opname == 'POP_BLOCK':
                self.co_blocks.popleft()
            elif opname == 'CALL_FUNCTION':
                args, kwargs = [], {}
                argc = arg & 0x0f
                kwargc = (arg & 0xf0) >> 8

                # Get keyword arguments first
                # TODO: WIP

                # Get positional arguments
                for i in range(argc):
                    tos = self.pop()
                    args.insert(0, tos)

                # Get a function
                function = self.pop()
                if function.__name__ in self._locals:
                    frame = PythonVM()
                    retval = frame.eval(function)
                else:
                    retval = function(*args, **kwargs)
                self.push(retval)
            # Not implemented operator
            else:
                raise NotImplementedError(
                    'the opname `{}` is not implemented.'.format(opname)
                )
            self.pc += 1

def main(argv):
    vm = PythonVM()
    if len(argv) > 0:
        with open(argv[0], 'rt') as f:
            code = f.read()
            vm.eval(code)
    else:
        vm.eval(sys.stdin.read())

if __name__ == '__main__':
    main(sys.argv[1:])