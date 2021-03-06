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

from slimpy_base.Core.Interface.ContainerBase import DataContainer
#from slimpy_base.utils.Logger import Log
#from slimpy_base.utils.GlobalVars import GlobalVars
#from slimpy_base.utils.hashTable import HashTable

from slimpy_base.Environment.InstanceManager import InstanceManager


class BuilderBase( object ):
    """
    abstract class
    """
#    log = Log()
#    table = HashTable()
#    slimvars = GlobalVars()
    env = InstanceManager()
    
    
    def __init__(self):
        pass
    
    def build(self, g, targets, sources, breakpoints, **k):
        raise NotImplementedError("Builer subclass must implement build method")
    
    def isSource( self, val ):
        """
        test if val is a DataContainer or id of a DataContainer and 
        if that DataContainer is full
        """
        
        try:
            
            node =  self.env['table'][val]
        except KeyError:
            return False
        if isinstance( node, DataContainer ):

            return node.isfull()

        return False
    
    def get_graph(self):
        return self._graph

    def set_graph(self, graph):
        self._graph = graph
        
    graph = property( get_graph, set_graph )
    
