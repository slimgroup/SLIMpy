
"""
Directed graph class
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

from slimpy_base.Core.Graph.Graph.Graph import graph as __Graph
from slimpy_base.Environment.InstanceManager import InstanceManager
#from slimpy_base.utils.hashTable import HashTable
from itertools import ifilter


class DiGraph( __Graph ):
    """
    general purpose graph
    """
    env = InstanceManager()
#    log = Log()
#    table = HashTable()
    
    def __init__( self ):

        """
        method calls set the graph to empty and 
        """
        
        self.__adjacencyList = {}
        self.__invAdjacencyList = {}
        self._node_info = {}
        
#        self.__buildTargets = set()
#        self.__sources = set()
        
        

#    def setBuildTargets( self, *targets ):
#        """
#        adds targets to the __buildTargets set
#        """
#        for t in targets:
#            assert t in self, "target '%(t)s' not in graph" %vars()
#            
#        self.__buildTargets.update( targets )
#        
#    def getBuildTargets( self ):
#        return self.__buildTargets
    
    def setAdjacencyList( self, adjList ):
        """
        set the adjacency list to adjList
        """
        
        self.__adjacencyList = adjList
        
    def setInvAdjacencyList( self, adjList ):
        """
        set the adjacency list to adjList
        """
        
        self.__invAdjacencyList = adjList
        
        

    def appendEdge( self, source, target, Etype=False , colour='black' ):
        """
        Append an edge to the graph
        @param source: doesn't have to be in the graph already
        @param target: doesn't have to be in the graph already
        @param colour: 'red' if data -> container
                       'green' if container -> data
                       'black' [default] if other
        """
        
            
        self.setAdj( source, target, Etype, colour )
        
        self.setInvAdj( source, target, Etype, colour )
        
        return "|%06s | \tAdding edge: %s --> %s " %( Etype, source, target )
    
    def set_node_info( self, node, **kw ):
        info = self._node_info.setdefault(node, {})
        info.update( kw )
    
    def node_info(self, node):
        return self._node_info.setdefault(node, {})
    
    def setInvAdj( self, source, target, Etype, colour ):
        """
        called by appendEdge
        """

        #set forward adj list
        l1 = self.__invAdjacencyList.setdefault( target, {} )
        
        l1[source] = dict( Etype=Etype, colour=colour )
        
        self.__invAdjacencyList.setdefault( source, {} )
        

    def setAdj( self, source, target, Etype, colour ):
        """
        called by appendEdge
        """

        #set forward adj list
        l1 = self.__adjacencyList.setdefault( source, {} )
        
        l1[target] = dict( Etype=Etype, colour=colour )
        
        self.__adjacencyList.setdefault( target, {} )


    
    def appendNode( self, node ):
        self.adjacencyList.setdefault( node, {} )
        self.invAdjacencyList.setdefault( node, {} )
    

    def __iter__( self ):
        return self.getAdjacencyList().keys().__iter__()
    
    
    def iter_edges(self):
        for v in self.__adjacencyList.iterkeys():
            for u in self.__adjacencyList[v].iterkeys():
                yield v,u 
        return
    
#    def addSource( self, node ):
#        """
#        add a source to the list of sources
#        """
#        self.__sources.add( node )
#    
#    def getSources( self ):
#        return self.__sources
    
    def getAdjacencyList( self ):
        """
        get the adjacency matrix for the graph
        """
        return self.__adjacencyList
    
#    def isSource( self, node ):
#        """
#        find if node is in the set of sources
#        """
#        return node in self.__sources
    
        
    
    def getInvAdjacencyList( self ):
        return self.__invAdjacencyList
    

    def getEdgeColour( self, u, v ):        
        edge = self.getEdge( u, v )
            
        colour = edge.get( 'colour', 'black' )
        
        return colour
    
    def getEdgeType( self, u, v ):
        edge = self.getEdge( u, v )
            
        
        flag = edge.get( 'Etype', False )
        return flag

    def getEdge( self, u, v ):
        try:
            adjDict = self.getAdjacencyList()
            edge = adjDict[u][v]
        
        except KeyError, msg:

            adjDict = self.getAdjacencyList()
            edge = adjDict[v][u]
        return edge
        

    def adj( self, item ):
        """
        return a list of all indices pointed to by element item
        """
        adjacencyList = self.getAdjacencyList()
        return adjacencyList[item].keys()
    
    def invAdj( self, item ):
        invAdjlist = self.getInvAdjacencyList()
        try:
            return invAdjlist[item].keys()
        except KeyError, msg:
            raise 
            

    
    def getAllNodes( self, s=None ):
        "get all nodes except s"
        nodes =  self.getAdjacencyList().keys()
        if s:
            nodes.remove( s )
            
        return nodes
    
    def getSourceNodes( self ):
        """
        return all nodes which do not depend on any other node
        """
        # if the 
        return ifilter( lambda u : not len( self.invAdj( u ) ) , self )

    def transp( self ):
        from copy import copy
        g = copy( self )
        tmp = g.getAdjacencyList()
        g.setAdjacencyList( g.getInvAdjacencyList() )
        g.setInvAdjacencyList ( tmp )
        return g
    
    

    
    def __len__( self ):
        return len( self.getAdjacencyList() )
    
    def clean( self ):
        self.__init__()
        
    def numedges(self):
        'returns the number of edges in this graph'
        sum = 0
        adj = self.getAdjacencyList()
        for val in adj.values():
            sum += len(val)
        return sum

    def __repr__( self ):
        return "<SLIMpy.Digraph: %s nodes, %s edges>" % (len(self), self.numedges() )


