'''
Created on Oct 20, 2017

@author: Heidi
'''
from distutils.core import setup
import sys
sys.setrecursionlimit(5000)
import py2exe

sys.path.append('C:\Windows\WinSxS\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91')
sys.path.append('C:\ONC_Calculator\ONC_Calculator\src\root\nested')

setup(
    windows = ["testUnits.py"],
    options = {"py2exe":{"includes":["patientData"]}},
    )