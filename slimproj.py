"""
slimproj allows SLIMpy integration with SCons
"""
## 
# @package slimproj SLIMpy integration with scons

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



#import slimproj_core                                                    # @UnusedImport
import slimproj_core.SlimProj                                            # @UnusedImport

from slimproj_core.DefaultApps import *                                  # @UnusedWildImport
from slimproj_core.builders.Profiler import Profiler                     # @UnusedImport
from slimproj_core.builders.DotTester import DotTester                   # @UnusedImport

from slimproj_core.builders.funtion_decorators import slim_builder        #@UnusedImport
from slimproj_core.builders.funtion_decorators import slim_builder_simple #@UnusedImport

