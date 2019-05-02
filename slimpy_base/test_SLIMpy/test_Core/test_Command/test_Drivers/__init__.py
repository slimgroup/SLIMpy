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

from test_UnixPipes import suite as up_suite
from test_remoteDriver import suite as rd_suite
#from test_MultiDriver import suite as md_suite
from test_OutOfCoreDriver import suite as ooc_suite
from unittest import TestSuite


def suite():

    tests = [ 
             up_suite(),
             rd_suite(),
#             md_suite(),
             ooc_suite()
             ]
    
    return TestSuite(tests)
