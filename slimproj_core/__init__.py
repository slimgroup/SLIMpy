"""
@package slimproj_core SLIMpy integration with SCons

@defgroup sconsint SLIMpy/SCons Integration

This group contains all of the SLIMpy SCons integration functionality such as 
SCons Builders, Tools and helper functions  
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

try:
    from SCons.Script import EnsureSConsVersion as _EnsureSConsVersion 
    from SCons.Script import EnsurePythonVersion as _EnsurePythonVersion
except:
    print
    print "Error: SCons 0.98 or greater required"
    print
    raise

 
_EnsureSConsVersion(0,98)
_EnsurePythonVersion(2,5)
