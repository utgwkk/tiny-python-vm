# tiny-python-vm
A tiny Python bytecode interpreter written in Python.

Requires Python 3.5 or later.

## Usage
### from command-line argument
```
$ python3 vm.py hoge.py
```

### from standard input
```
$ cat hoge.py | python3 vm.py
```

### run test suite
```
$ python3 test_vm.py
```

## Available syntaxes
The example of available codes are in `examples/`.

* Assigments
* Building `list`, `tuple`, `set`, `map`
* Arithmetic calculations
* `while` statements
* `if`, `elif`, `else` statements
