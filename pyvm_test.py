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

    def test_load_const_str(self):
        self.assertEqual(
            "hoge",
            self.vm.eval('"hoge"')
        )

if __name__ == '__main__':
    unittest.main()
