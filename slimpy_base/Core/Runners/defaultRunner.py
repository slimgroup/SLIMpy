"""

This is the Runner Class.  It should inherit from the PresidenceStack to allow for operators.
Unless this is not in the given task.

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

from pdb import set_trace

from slimpy_base.Core.Runners.PresidenceStack import presStack

class defaultRunner( presStack ):
    """
    Runs commands from the graph. uses two stacks to keep 
    track of dependencies and perhaps run several commands 
    at the same time.
    """
    type = "default"
    
    def __init__( self ):
        self.created_nodes = set()
        presStack.__init__( self )
    
    def set_graph(self,graph):
        presStack.set_graph( self , graph)
        
    def run( self ):
        """
        run the current graph with targets
        """
#        if targets.__len__() != 0:
#            self.__init__(other.buildGraph(*targets))
        
        p1 = self.pull()
        numberRan = 0
        
        table = self.env['table']
        log = self.env['record']
        while p1:
            if isinstance( p1, tuple ):
                items = [ table[item] for item in p1]

                # add commands returns a runnable object
                # 'runnable' and a datacontainer 'target'
                runnable = self.add( items )
                
                
                # set the data to the result of running the command
                
                numberRan += 1
                log.stat_update()
                if self.env['slimvars']['runtype'] == 'dryrun':
                    print >> log( 1, "cmd" ), runnable.nice_str()
                    pass
#                    runnable.add_node_name_to_targets('localhost' )
                else:
                    runnable.node_name = 'localhost'
                    runnable.run( )
                    
            else:
                self.created_nodes.add( p1 )
            self.pop( p1 )
            p1 = self.pull()
        return numberRan

