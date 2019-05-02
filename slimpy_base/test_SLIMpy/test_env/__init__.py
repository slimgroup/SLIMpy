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

from test_singleton import suite as sin_suite
from test_GlobalVars import suite as gv_suite
from test_GraphManager import suite as gm_suite
from test_hashTable import suite as ht_suite
from test_InstanceManager import suite as im_suite
from test_KeyStone import suite as ks_suite

def suite():
    return TestSuite( [sin_suite(),
                       gv_suite(),
                       gm_suite(),
                       ht_suite(),
                       im_suite(),
                       ks_suite(),                       
                       ] )

