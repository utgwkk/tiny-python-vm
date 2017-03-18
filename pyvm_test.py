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

if __name__ == '__main__':
    unittest.main()
