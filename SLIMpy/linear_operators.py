"""
@package SLIMpy.linear_operators
This is a proxy module to import all of the linear operators from 

@page slimpyopers SLIMpy Operators
This page is for SLIMpy operators
"""
###############################################################
# All linear oprtator imports
###############################################################
from slimpy_base.Core.User.linop.linear_operator import LinearOperator, Identity, CompoundOperator,ArithmaticOperator
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.User.AumentedMatrix.AugOperator import AugOperator

from slimpy_base.Core.User.linop.NewLinOp import NewLinop
from slimpy_base.api import linear_operators
from slimpy_base.api.linear_operators import *


from slimpy_contrib.linear_operators import *
