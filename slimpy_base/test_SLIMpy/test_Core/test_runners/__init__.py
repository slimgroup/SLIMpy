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

from unittest import TestSuite

from test_defaultRunner import suite as dr_suite
from test_dotRunner import suite as dot_suite
from test_DottestRunner import suite as dtotest_suite
from test_multicoreRunner import suite as mr_suite
from test_PresidenceStack import suite as ps__suite


def suite():
    
    tests = [
             dr_suite(),
             dot_suite(),
             dtotest_suite(),
             mr_suite(),
             ps__suite()
             ]
    
    return TestSuite(tests)
