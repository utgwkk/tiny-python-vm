import pyvm
import unittest

class PyVMTest(unittest.TestCase):
    def setUp(self):
        self.vm = pyvm.PythonVM()

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

    def test_if_expression_true(self):
        self.vm.eval('cond = True\nif cond: x = 1')
        self.assertEqual(
            1,
            self.vm._locals.get('x')
        )

    def test_if_expression_false(self):
        self.vm.eval('cond = False\nif cond: x = 1')
        self.assertEqual(
            None,
            self.vm._locals.get('x')
        )

if __name__ == '__main__':
    unittest.main()
