from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("ai_minimax_alpha_beta.py")
)