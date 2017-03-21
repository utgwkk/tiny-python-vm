import vm
import unittest

class PyVMTest(unittest.TestCase):
    def setUp(self):
        self.vm = vm.PythonVM()

    def tearDown(self):
        self.vm._reset()

    def test_load_const_num(self):
        self.assertEqual(
            10,
            self.vm.eval('10')
        )

    def test_load_const_num_float(self):
        self.assertEqual(
            10.55,
            self.vm.eval('10.55')
        )

    def test_load_const_str(self):
        self.assertEqual(
            "hoge",
            self.vm.eval('"hoge"')
        )

    def test_eval_empty(self):
        self.assertEqual(
            None,
            self.vm.eval('')
        )

    def test_assign_const(self):
        self.vm.eval('a = 1')
        self.assertDictEqual(
            {'a': 1},
            self.vm._locals
        )

    def test_binary_add(self):
        self.vm.eval('a = 3\nb = 8\nc = a + b')
        self.assertEqual(
            11,
            self.vm._locals.get('c')
        )

    def test_binary_sub(self):
        self.vm.eval('a = 3\nb = 8\nc = a - b')
        self.assertEqual(
            -5,
            self.vm._locals.get('c')
        )

    def test_if_statement_true(self):
        self.vm.eval('cond = True\nif cond: x = 1')
        self.assertEqual(
            1,
            self.vm._locals.get('x')
        )

    def test_if_statement_false(self):
        self.vm.eval('cond = False\nif cond: x = 1')
        self.assertEqual(
            None,
            self.vm._locals.get('x')
        )

    def test_if_else_statement_true(self):
        self.vm.eval('cond = True\nif cond: x = 1\nelse: x = 2')
        self.assertEqual(
            1,
            self.vm._locals.get('x')
        )

    def test_if_else_statement_false(self):
        self.vm.eval('cond = False\nif cond: x = 1\nelse: x = 2')
        self.assertEqual(
            2,
            self.vm._locals.get('x')
        )
    
    def test_swap(self):
        self.vm.eval('x = 1; y = 2; x, y = y, x')
        self.assertEqual(
            2,
            self.vm._locals.get('x')
        )
        self.assertEqual(
            1,
            self.vm._locals.get('y')
        )

    def test_while_loop(self):
        self.vm.eval('i = 5\nwhile i: i = i - 1')
        self.assertEqual(
            0,
            self.vm._locals.get('i')
        )

    def test_eval_with_default_locals(self):
        self.vm._reset(_locals={'a': 8, 'b': 3})
        self.assertEqual(
            6,
            self.vm.eval('a + b - 5')
        )

    def test_eval_with_complex_expression(self):
        self.vm._reset(_locals={'a': 8, 'b': 3})
        self.assertEqual(
            -17,
            self.vm.eval('a + 2 - 5 - b * a + 2')
        )

    def test_hello_world(self):
        self.vm.eval("print('Hello, world!')")

if __name__ == '__main__':
    unittest.main()
