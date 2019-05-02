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

from SCons.Script import Builder,Action,ARGUMENTS
from slimproj_core.builders.BuilderFunctions import DEFAULT_PROFILES

class Profiler( object ):
    
    def __init__(self,name):
        self.name = name
        self.act = None
        self._built = False
        
    def __str__(self):
        return "Profiler('%s.hotshot')" %self.name
    
    def set_action(self, act):
#        print "setting action for",self,"with",act  
        self.act = act
        
    def set_env(self,target,source,env):
#        print "set env "
        self.target = target[:]
        self.source = source[:]
        self.env = env.Clone()
        
        
    def profile(self):
#        print "calling profile",self
        
        if self._built:
#            print "has been built"
            return
        action  = Action( self.build, "Profile '%s' [%s]" %( self.act.__name__, self.name) )
        builder = Builder( action=action,
                           emitter=self.emitter,
                           suffix='.hotshot' )
        
        
        builder( self.env , self.name )
        
        self._built = True
        
    def emitter(self,target,source,env):
#        print 'emitting'
#        node = env.File(self.name)
        DEFAULT_PROFILES.append( target[0] )
#        target = [node]
        source = self.source
#        print 'targ',[str(t) for t in target]
#        print 'src',[str(t) for t in source]
        env.Alias( 'profile',  target )
        return target,source
        
    def build(self,target,source,env):
        
        import hotshot
        
        env['runtype'] = 'dryrun'
        env['verbose'] = ARGUMENTS.get('verbose',0)
        env['logfile'] = ARGUMENTS.get('log',None)
        env['callbacks'] = []
        
        prof = hotshot.Profile( str( target[0] ) )
        
        prof.runcall( self.act, self.target, source, env )
        prof.close()

