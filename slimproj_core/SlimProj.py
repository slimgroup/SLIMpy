"""
SLIMpy scons project tool 
"""

from os.path import dirname as _dname,join as _join
import SCons.Defaults as _scons_defaults
import SCons.Tool

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

#__all__ = ["Rush",'slim_builder','slim_builder_simple']

this_path = _dname(__file__)
slim_toolpath = _join( this_path, 'slim_tools')

#slim_tool = _scons_tool( 'slim_doc', toolpath=[slim_toolpath] )
#rush_tool = _scons_tool( 'Rush', toolpath=[slim_toolpath] )

def add_to_default_toolpath( toolpath ):
    SCons.Tool.DefaultToolpath.append( toolpath )
    

def add_to_default_tools( atool ):
    if 'TOOLS' in _scons_defaults.ConstructionEnvironment:
        _scons_defaults.ConstructionEnvironment[ 'TOOLS' ].append( atool )
    else:
        _scons_defaults.ConstructionEnvironment[ 'TOOLS' ] = [ 'default', atool ]


add_to_default_toolpath( slim_toolpath )

