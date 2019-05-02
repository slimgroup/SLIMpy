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

"""
loads test suites from sub packages
"""
from  unittest import TestSuite
from test_Command import suite as comSuite
from test_CommandPack import suite as cp_suite
from test_ConstraintFunctions import suite as cf_suite
from test_Converter import suite as conv_suite
from test_MapFunctions import suite as map_suite
from test_TransformFunctions import suite as tf_suite

from test_Drivers import suite as dr_suite

def suite():
    tests = [ 
             comSuite(),
             cp_suite(),
             cf_suite(),
             conv_suite(),
             map_suite(),
             tf_suite(),
             dr_suite(),
             
             ]
    
    return TestSuite( tests )
