"""
class to run as many simultaneous commands at the same time
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


from slimpy_base.Core.Graph.Cleaner import cleaner
from slimpy_base.Core.Runners.RunnerBase import Runner
import pdb


class presStack( Runner ):
    """
    class to run as many simultaneous commands at the same time  
    """
    
    def __init__(self):
        Runner.__init__( self )
        
    def set_graph( self, graph ):
        self.status = {}
        self.ready = {}
        self.sources = set()
        self.cleaner = cleaner( graph )
        self.G = graph
        
        for u in self.G.getSourceNodes():
            self.ready[u] = True

        return 
#        """
#            for v in self.G.adj( u ):
#                bool = True
#                for w in self.G.invAdj( v ):
#                    bool = bool and self.sources.get( w, False )
#                if bool:
#                    self.ready[v] = True
#        """ #IGNORE:W0101,W0105 
            
    def pull( self , u=None ):
        """
        pull a command of the top of the ready stack
        may return none if there are no 
        ready nodes
        """
        if u is None:
            if not self.ready.keys():
                return None
            u = self.ready.keys()[0]
            
        
        del self.ready[u]
        self.status[u] = 'working'
        return u
    
    def pop( self, u ):
        """
        @param u: node in the graph
        @precondition: u was a node pulled by the 
            pull command
        @postcondition:
            1. for each 'D' a dependent of u if all of 'D's dependencies 
               are met, 'D' will be added to the ready stack
            2. u will be passes to the current cleaner
            3. u will be added to the graphs source nodes
            
        """
        
        if not self.status.has_key(u):
            raise Exception( "node %s has not been pulled from top of stack" %u )
        if not self.status[u] == 'working':
            return False
        self.status[u] = 'done'
        
        self.sources.add( u )
        
#        self.G.addSource( u )
        self.clean( u )

        for v in self.G.adj( u ):
            isready = True
            for w in self.G.invAdj( v ):
                isready = isready and w in self.sources
            if isready:
                self.ready[v] = True
        return True
    
    def has_ready(self):
        return len( self.ready) 
    
    def has_ready_data(self):
        return len([ key for key in self.ready.keys() if not isinstance( key, tuple) ])
    
    def pull_data(self):
        for key in self.ready.keys():
            if isinstance(key, tuple):
                continue
            else:
                return self.pull(key)
            
        return False
    
        
    def has_more_jobs(self):
        ready = self.has_ready()
        working = self.num_working()
        return ready or working 

    def num_working(self):
        return len( [ stat for stat in self.status.values() if stat == 'working' ] )
    
    def clean( self, node ):
        """
        adds a node to the cleaner
        """
        self.cleaner.clean( node )
    
#    def get_new_targets(self):
#        cleaned_nodes = self.cleaner.get_cleaned_nodes()
#        remaining = self.created_nodes.difference( cleaned_nodes )
#        
#        return remaining
        
        
        
    
