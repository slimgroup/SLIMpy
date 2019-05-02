
"""
This is the Runner Class.  It should inherit from the PresidenceStack 
to allow for operators.
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

from slimpy_base.Core.Runners.PresidenceStack import presStack 

class dryrunRunner( presStack ):
    type = "dryrun"
    
    def __init__( self ):
        presStack.__init__( self )
        
    def set_graph(self, graph):
        presStack.set_graph( self, graph )
    
    
    def run( self ):
        """
        run the current graph with targets
        """
#        if targets.__len__() != 0:
#            self.__init__(other.buildGraph(*targets))
        
        command_or_data = self.pull()
        numberRan = 0
        while command_or_data:
            if isinstance( command_or_data, tuple ):
                command = command_or_data
                items = [ self.table[item] for item in command ] 

                # add commands returns a runnable object 'runnable' and a datacontainer 'target'
                runnable = self.add( items )
                
                # set the data to the result of running the command
                print >> self.log( 1, "command" ), runnable
                numberRan += 1
            else:
                data = command_or_data
                self.addSource( data )
                
            self.pop( command_or_data )
            command_or_data = self.pull()
        return numberRan
