"""
Default applications to import
"""
from slimproj_core.builders.my_de_call import DefaultEnvCall as _DefaultEnvCall

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

from SCons.Script import DefaultEnvironment as _def_env
Solve = _DefaultEnvCall( 'Solve', 'Solve', None )

def Rush( target, source, rush_action, *p,**kw ):
    """
    Default environment call. 
    The same as native Command builder. 
    """
    
    denv = _def_env( )
    env = denv.Clone( )
    env._Rush( target, source, rush_action=rush_action, *p, **kw )
