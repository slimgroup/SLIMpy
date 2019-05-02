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


from unittest import TestSuite,TestLoader

from test_AugmentedBase import suite as ab
from test_AugOperator import suite as ao
from test_AugVector import suite as av
from test_HelperFunctions import suite as hf
from test_MetaSpace import suite as ms

def suite():
    tests = [ ab(), ao(),av(), hf(), ms() ]

    return TestSuite(tests)

