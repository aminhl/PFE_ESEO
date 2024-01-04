import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','themes/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "ESEO - E-Sante ",
    version = "1.0",
    description = "Mutation Cancer Detection",
    author = "Amin Hlel",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
