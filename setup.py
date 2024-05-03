from setuptools import setup
from Cython.Build import cythonize

setup(
    name="PISM's connected component labeling code",
    ext_modules=cythonize("pism_label_components.pyx"),
)
