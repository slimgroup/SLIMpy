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

from  unittest import TestSuite
from SLIMTestCaseLoader import SLIMTextTestRunner
import sys

from test_Core import suite as CoreSuite
from test_utils import suite as utilsSuite
from test_env import suite as envSuite
from test_User import suite as userSuite
__all__ = ["test"]

def suite():
    tests = [CoreSuite(),
             utilsSuite(),
             envSuite(),
             userSuite(),
             
             ]
    return TestSuite(tests)




def test(stream=sys.stderr, descriptions=1, verbosity=1):
    
    SLIMpyTestRunner = SLIMTextTestRunner(stream, descriptions, verbosity)
    
    return SLIMpyTestRunner.run(suite())
