from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("*", ["pism_label_components.pyx"],
        include_dirs=[numpy.get_include()]),
]

setup(
    name="PISM's connected component labeling code",
    ext_modules=cythonize(extensions),
)
