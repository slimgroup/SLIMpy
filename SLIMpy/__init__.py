## @package SLIMpy
# this is the main init file for SLIMpy 
# 
""" 

SLIMpy is a tool that interfaces Abstract numerical algorithms 
with a variety of lower lever software packages.
SLIMpy uses Operator overloading to build an abstract computational tree
which can be applied to many other software environments such as RSF.

helper functions:
    shelp( *names ) -> prints SLIMpy help on names
    listLinop() -> prints a list of all the linear operator classes 
    listPlugins() -> print the plugins available ( ie. rsf )
    printglobal() -> prints all global variables in 'slimvars'
    
"""

__copyright__ = """
Copyright 2008 Sean Ross-Ross
"""
__license__ =  """
This file is part of SLIMpy .

SLIMpy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SLIMpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SLIMpy . If not, see <http://www.gnu.org/licenses/>.
"""



from slimpy_base.utils.RegisterType import slimpy_funcs
from sys import version_info
assert version_info > ( 2, 4 ) , ( "Please use a version"
                                    " of Python greater than 2.4" )
del version_info

import slimpy_base

## major version number 
__version_major__ = slimpy_base.__version_major__
## minor version number 
__version_minor__ = slimpy_base.__version_minor__
## svn revision number 
__revision__ = slimpy_base.__revision__

__version__ = slimpy_base.__version__
__date__ = slimpy_base.__date__

import time as __time__

from slimpy_base.Environment.InstanceManager import InstanceManager

env = InstanceManager()

End = env.Execute
Execute = env.Execute 
# Main functionality of slimpy is setup in here
#keystone.setup()

from slimpy_base.User.adiFactories import VectorFactory as __VectorFactory__
# calling the vectorFactory a vector tricks the user into thinking they are 
# using the vectors directly
# This is because a lot of work goes into creating
# a vector from user generated data
# Internal slimpy does not use this
vector = __VectorFactory__()

###############################################################
# function loader
###############################################################

from slimpy_base.api.functions.functionLoader import fLoader as __Loader
__loader__ = __Loader()
__loader__.load( locals(), globals() )

###############################################################
# All linear oprtator imports
###############################################################
from slimpy_base.Core.User.linop.linear_operator import LinearOperator, Identity, CompoundOperator,ArithmaticOperator

from slimpy_base.Core.User.linop.NewLinOp import NewLinop
from slimpy_base.api import linear_operators
from slimpy_base.api.linear_operators import *

#===============================================================================
# # Augmented Matrix Tools
#===============================================================================
#from User.AumentedMatrix.Aug_matrix import aug_oper, aug_vec
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.User.AumentedMatrix.AugOperator import AugOperator
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
from slimpy_base.User.AumentedMatrix.HelperFunctions import Diag

#from slimpy_base.Core.User.Spaces import voidSpace, Space
from slimpy_base.Core.Interface.PSpace import voidSpace,PSpace
from slimpy_base.Core.User.Structures.VectorSpace import VectorSpace,VectorAddition
Space = VectorSpace


#===============================================================================
# # set up the commandline arguments
# # slimOptionParser is also a singleton class
#===============================================================================
from slimpy_base.setup.cmndLineParse import SlimOptionParser
from slimpy_base.setup.ParseEnv import parse_env
# to set the slimOptionParser class
optionparser = SlimOptionParser()
# conviniently place this class method in the users namespace
parse_args = optionparser.parse
check_required = optionparser.check_required


#===============================================================================
# # test stuff: 
#===============================================================================
def test( descriptions=1, verbosity=1, stream=None):
    """
    Imports the test module and runs the test suite.
    descriptions and verbosity are the arguments to pass to
    the default test runner
    """
    if stream is None:
        from sys import stderr
        stream = stderr
    
    from slimpy_base.test_SLIMpy import test as __test
    
    return __test( descriptions=descriptions, verbosity=verbosity, stream=stream )
    

#===============================================================================
# utils
#===============================================================================
#from slimpy_base.utils.Logger import Log


#===============================================================================
# Create singleton instances for the main namespace
#===============================================================================
log = env[ 'record' ]

#===============================================================================
# Bring class mwthods into the main namespace
#===============================================================================


# _GlobalVars methods INTO the main namespace 
slimvars = env['slimvars']
printglobal = slimvars.printGlobals
setglobal = slimvars.setglobal

#from SLIMmath.function import max
from slimpy_base.api.functions.scalar_functions import *

from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType as _rlt

listLinop = _rlt.print_opers

from slimpy_base.shelp import shelp

keystone = env['keystone']

# keystone methods INTO the main namespace
listPlugins = keystone.listPlugins

#function.__dict__ = slimpy_funcs

from slimpy_base.utils.DotTest import DotTest

