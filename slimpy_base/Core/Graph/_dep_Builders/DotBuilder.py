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
Deprecated
"""

#from slimpy_base.Core.Graph.Runers.AddComand import addCommands
from slimpy_base.Core.Graph.Builders.SLIMBuilder import SLIMBuilder 


class DotBuilder( SLIMBuilder ):
    node = 0
    
    def __init__( self, graph, name='SLIMpy', abr=True ):
        self.counterC = 0
        self.counterD = 0

        self.abr = abr
        self.dot = self.toDot( graph, name=name, abr=abr )
    
    def printDot( self ):
        return self.dot
    
    def toDot( self, graph, name='SLIMpy', abr=True ):
        start = 'digraph %s {\n' %name
        end = '\n}'
        datastr = 'node [shape = "ellipse"];\n\n'
        commstr = 'node [shape = "box"];\n\n'
        middle = "\n\n"

        
        dataDict = {}
        commandDict = {}

        for u in graph:
            for v in graph.adj( u ):
                
                nodestru = self.nodeToString( u, dataDict, commandDict )
                nodestrv = self.nodeToString( v, dataDict, commandDict )
                middle += '''%(nodestru)s -> %(nodestrv)s; \n''' %vars()
        
        datastr += "\n".join( ['%(val)s [ label = "%(key)s" ]' %vars() for key, val in dataDict.items()] ) +"\n\n\n"
        commstr += "\n".join( ['%(val)s [ label = "%(key)s" ]' %vars() for key, val in commandDict.items()] ) + '\n\n\n'
        
        
        return self.abbrige( start + datastr + commstr + middle + end, abr )
    
    def abbrige( self, s, abr ):
        if abr:
            for item in self.slimvars['abridgeMap'].items():
                s = s.replace( *item )
                
        return s

    def nodeToString( self, node, dataDict, commandDict ):
        """
        function to work with data in the hashtable 
        """
        if isinstance( node, tuple ):
            
            nodes = [self.table[n] for n in node ]
            
            s = str( nodes ).replace( '"', "'" )
            
            val = "d%d" %self.counterC
            if commandDict.has_key( s ):
                return commandDict[s]
            else:
                self.counterC+=1
                commandDict[s] = val
            
            return val
                
            
        else:
            nodes =  self.table[node]
        
            s = str( nodes ).replace( '"', "'" )
            
            val = "c%d" %self.counterD
            
            if dataDict.has_key( s ):
                return dataDict[s]
            else:
                self.counterD+=1
                dataDict[s] = val
            return val
                        
