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

"""
Prints graph to SLIMpy log
"""
from slimpy_base.Core.Graph.Graph.GraphPrinter import GraphPrinter as GraphPrinter_Base
from slimpy_base.Environment.InstanceManager import InstanceManager
#from slimpy_base.utils.Logger import Log
#from slimpy_base.utils.hashTable import HashTable
#from slimpy_base.utils.GraphManager import GraphManager



class GraphPrinter( GraphPrinter_Base ):
    """
    Prints graph to SLIMpy log
    """
    
    env = InstanceManager()
#    log = Log()
#    graphmgr = GraphManager()
    
    @classmethod
    def nodeToString( cls, node ):
        """
        function to work with data in the hashtable 
        """
        table = cls.env['table']
        if isinstance( node, tuple ):
            
            nodes = [ table[n] for n in node ]
        else:
            nodes =  table[node]
        
        return str( nodes )
    
    @classmethod
    def _print( cls, *things ):
        """
        print classmethod 
        """
    #        for thing in things:
#            print >> GraphPrinter.log , thing, 
#        print >> GraphPrinter.log
        return things
    

            

    
