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


from slimpy_base.Core.Runners.RunnerBase import Runner
from slimpy_base.Core.Graph.Builders.SConsBuilder import SConsBuilder

class sconsRunner( Runner ):
    """
    print a SConstruct compatible script to stdout
    """
    type = "scons"    
    
    def __init__( self ):
        Runner.__init__( self )
    def set_graph(self,graph):
        
        self.graph = graph
        
        
    def run( self ):
        """
        run the current graph with targets
        """        
        
        scons = SConsBuilder( self.graph, None )
        print scons.printSCons()

