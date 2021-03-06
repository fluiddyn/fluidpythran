import sys
import os
from time import sleep

import numpy as np

try:
    import pythran
except ImportError:
    pythran = None

from .util import path_cachedjit_classes
from .justintime import path_cachedjit, modules
from .pythranizer import scheduler, wait_for_all_extensions
from . import mpi
from .compat import rmtree

scheduler.nb_cpus = 2

module_name = "fluidpythran.for_test_justintime"

str_relative_path = module_name.replace(".", os.path.sep)

path_cachedjit = mpi.PathSeq(path_cachedjit)

path_pythran_dir = path_cachedjit / str_relative_path
path_classes_dir = path_cachedjit_classes / str_relative_path
path_classes_dir1 = (
    path_cachedjit / path_cachedjit_classes.name / str_relative_path
)


def delete_pythran_files(func_name):
    for path_pythran_file in path_pythran_dir.glob(func_name + "*"):
        if path_pythran_file.exists():
            path_pythran_file.unlink()


if mpi.rank == 0:
    delete_pythran_files("func1")
    delete_pythran_files("func2")
    delete_pythran_files("func_dict")

    if path_classes_dir.exists():
        rmtree(path_classes_dir)
    if path_classes_dir1.exists():
        rmtree(path_classes_dir1)

mpi.barrier()


def test_cachedjit():

    from .for_test_justintime import func1

    a = np.arange(2)
    b = [1, 2]

    for _ in range(2):
        func1(a, b)
        sleep(0.1)


def test_cachedjit_simple():

    from .for_test_justintime import func2

    func2(1)

    if not pythran:
        return

    mod = modules[module_name]
    cjit = mod.cachedjit_functions["func2"]

    for _ in range(100):
        func2(1)
        sleep(0.1)
        if not cjit.compiling:
            sleep(0.1)
            func2(1)
            break

    del sys.modules[module_name]
    del modules[module_name]

    from .for_test_justintime import func2

    func2(1)


def test_cachedjit_dict():
    from .for_test_justintime import func_dict

    d = dict(a=1, b=2)
    func_dict(d)

    if not pythran:
        return

    mod = modules[module_name]
    cjit = mod.cachedjit_functions["func_dict"]

    d = dict(a=1, b=2)
    func_dict(d)

    wait_for_all_extensions()

    for _ in range(100):
        d = dict(a=1, b=2)
        func_dict(d)
        sleep(0.1)
        if not cjit.compiling:
            sleep(0.1)
            func_dict(d)
            break


def test_cachedjit_method():
    from .for_test_justintime import MyClass

    obj = MyClass()
    obj.check()

    if not pythran:
        return

    obj = MyClass()
    obj.check()

    wait_for_all_extensions()

    obj.check()
