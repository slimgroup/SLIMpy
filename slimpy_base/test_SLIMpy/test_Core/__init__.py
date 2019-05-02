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

#test_SLIMpy.test_Core.__init__

from  unittest import TestSuite


from test_Command import suite as ComSuite
from test_Graph import suite as TGSuite
from test_User import suite as userSuite
from test_Interface import suite as interface_suite
from test_MultiCore import suite as multicore_suite
from test_runners import suite as runner_suite

def suite():
    tests = [ComSuite(),
             TGSuite(),
             userSuite(),
             interface_suite(),
             multicore_suite(),
             runner_suite(),
             ]
    
    return TestSuite(tests)
