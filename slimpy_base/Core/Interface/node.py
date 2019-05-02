"""
Node classes for use in the graph and HashTable
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

#from slimpy_base.utils.hashTable import HashTable 
#from slimpy_base.utils.GraphManager import GraphManager
from slimpy_base.Environment.InstanceManager import InstanceManager

class Node( object ):
    """
    Node class to represent data and commands in the hash table
    
    """

    env = InstanceManager()
    
    _objID = None
    __setstate__= None
    name = "Node"
    
    def __init__( self, obj ):
        """
        take any object and store it to the hashtable 
        while tracking it with this node instance
        """
        table = self.env['table']
        self._objID = table.append( obj )
        
    def get( self ):
        """
        get object associated with this node from the hash Table
        """
        table = self.env['table']
        return table[self._objID]
    
    def getID( self ):
        """
        return int id of node object
        """
        return self._objID
    
    id = property( getID )
    
    def __str__( self ):
        return "(%s:%s)"%( self.name, self._objID )
    
    def __repr__( self ):
        return self.__str__()
    
    def __getattr__( self, attr ):
        
        return getattr( self.get(), attr )
    
    def __eq__(self, other):
        if isinstance(other, Node) and self.id == other.id:
            return True
        else:
            return False


class Target( Node ):
    """
    Target class is just to differentiate between different nodes in the command object
    """
    name = "Target"

class Source( Node ):
    """
    Source class is just to differentiate between different nodes in the command object
    """
    name = "Source"
