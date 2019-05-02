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

from slimpy_base.Core.Runners.dottestRunner import dottestRunner
from SCons.Script import Builder,Action,ARGUMENTS
from slimproj_core.builders.BuilderFunctions import DEFAULT_PROFILES

class DotTester( object ):
    
    def __init__(self,name):
        self.name = name
        self.act = None
        self._built = False
        
    def __str__(self):
        return "DotTester( )" %self.name
    
    def set_action(self, act):
#        print "setting action for",self,"with",act  
        self.act = act
        
    def set_env(self,target,source,env):
#        print "set env "
        self.target = target[:]
        self.source = source[:]
        self.env = env.Clone()
        
        
    def dot_test(self):
#        print "calling profile",self
        
        if self._built:
#            print "has been built"
            return
        action  = Action( self.build, "Dottest '%s' " %( self.act.__name__) )
        builder = Builder( action=action,
                           emitter=self.emitter
                            )
        
        
        builder( self.env , self.name )
        
        self._built = True
        
    def emitter(self,target,source,env):
        
        DEFAULT_PROFILES.append( target[0] )

        source = self.source
        
        env.Alias( 'dot-test',  target )
        return target,source
        
    def build(self,target,source,env):
        
        
#        env['runtype'] = 'dryrun'
        env['verbose'] = ARGUMENTS.get('verbose',0)
        
        debug  = ARGUMENTS.get('debug',None)
        if debug:
            debug = debug.split(',')
        else:
            debug = []
        env['debug'] = debug
        env['logfile'] = None
        
        runner = dottestRunner()
        
        from slimpy_base.Environment.InstanceManager import InstanceManager
        __env__ = InstanceManager( )
        __env__['graphmgr'].setRunner( runner )

        self.act( target, source, env )
        

