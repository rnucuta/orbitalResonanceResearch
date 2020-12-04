#python setup.py build_ext --inplace -f "thermal_cython.pyx"

import distutils.core
import Cython.Build
import argparse
import numpy


# parser = argparse.ArgumentParser()
# parser.add_argument("-f","--filename", help="python file name to cythonize", type=str)
# args=parser.parse_args()

# distutils.core.setup(
#     ext_modules = Cython.Build.cythonize(args.filename))

distutils.core.setup(
    ext_modules = Cython.Build.cythonize("thermal_cython.pyx"),
    include_dirs=[numpy.get_include()]
    )