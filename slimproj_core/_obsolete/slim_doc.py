"""
SLIM tool for scons 
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


#SLIM TOOL
#
#

def generate(env):
    """Add Builders and construction variables for xlC / Visual Age
    suite to an Environment."""
#    import SCons.Script
    from os.path import join
    env['MKHOWTO'] = join("/sw/share/doc/python24/Doc/tools/mkhowto")
    
    import slimproj_core.builders.CreateBuilders
    BUILDERS=slimproj_core.builders.CreateBuilders.CreateBuilders()
    
    env.Append( BUILDERS=BUILDERS )

#    SCons.Script._SConscript
#    if SCons.Script._SConscript.GlobalDict is None:
#        SCons.Script._SConscript.GlobalDict = {}
        
#    for key,val in BUILDERS.iteritems():
#        print key
#        SCons.Script._SConscript.GlobalDict[key] = val
##        exec "SCons.Script.%s = DefaultEnvironmentCall(%s)" % (name, repr(name))
    return
#

def exists(env):
    return 1


