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

#from SCons.Environment import Environment
from SCons.Script import DefaultEnvironment

class DefaultEnvCall(object):
    """A class that implements "global function" calls of
    Environment methods by fetching the specified method from the
    DefaultEnvironment's class.  """
    
    def __init__(self, method_name, tool=None, help=None ):
        self.method_name = method_name
        self._help = help
        self.tool = tool
    
    def __repr__(self):
        return "DefaultEnvCall( %s )" %repr(self.method_name)
    
    def __call__(self, *args, **kw):
        
        denv = DefaultEnvironment( )
        env = denv.Clone( )
        if self.tool:
            env.Tool( self.tool )
            
        method = getattr( env, self.method_name )
        return method( *args, **kw )
    
    def help(self):
        print self._help 


class DefaultBuilderCall( object ):
    
    def __init__(self, builder ):
        self.builder = builder
        
    def __call__(self,  *args, **kw ):
        
        
        denv = DefaultEnvironment( ) 
        env = denv.Clone()
        env['BUILDERS']['_SLIM_BUILDER'] = self.builder
        return env._SLIM_BUILDER( *args, **kw )
        
    
    
