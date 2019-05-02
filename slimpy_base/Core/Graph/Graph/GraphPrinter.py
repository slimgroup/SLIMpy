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


even = lambda x: not bool(x%2)

class GraphPrinter(object):
    
    
    @staticmethod
    def nodeToString(node):
        return str(node)
    
    @staticmethod
    def _print(*things):
        return map(str,list( things ) )
            
    
    @classmethod
    def printAdj( cls, graph, v, depth=0 , fetch=False ):
        s = []
        extend = s.extend
        lines = cls._print ( "%s+ %s" %( "".join( ['  ']*depth ) , cls.nodeToString(v) ) )
        extend(lines)
        for u in graph.adj( v ):
            lines = cls.printAdj(graph, u, depth+1 )
            extend(lines)
        return "\n".join(s)
    
    @classmethod
    def printInvAdj( cls, graph, v, spacer="" , fetch=False ):
        
        s = []
        extend = s.extend
        push = s.append
        #even = lambda x: not bool(x%2)
        
        lines = cls._print ( "%s+-%s" %( spacer, cls.nodeToString(v) ) )
        extend(lines)
        if not even(len(spacer)/3):
            spacer += '|  '
        else:
            spacer += '   '
        
        for u in graph.invAdj( v ):
            lines = cls.printInvAdj(graph, u, spacer )
            push(lines)
        return "\n".join(s)
    
    @classmethod
    def printDep( cls, graph, fetch=False ):
        s = []
        extend = s.extend

        lines = cls._print ( "---------Graph---------" )
        extend(lines)
        for u in graph :
            lines = cls._print ( '+' , cls.nodeToString(u) )
            extend(lines)
            for v in graph.adj( u ):
                lines = cls._print ( '--+', cls.nodeToString(v),"colour = %s , Etype=%s" %(graph.getEdgeColour(u, v),graph.getEdgeType(u, v))  )
                extend(lines)
        lines = cls._print ( "------Graph--End-------" )
        extend(lines)
        return "\n".join(s)

    @classmethod
    def printInvDep( cls, graph, fetch=False ):
        s = []
        extend = s.extend
        
        lines = cls._print ( "---------Graph---------" )
        extend(lines)
        for u in graph:
            lines = cls._print ( '+' + cls.nodeToString(u) )
            extend(lines)
            for v in graph.invAdj( u ):
                lines = cls._print ( '--+' +cls.nodeToString(v) )
                extend(lines)
        
        lines = cls._print ( "------Graph--End-------" )   
        extend(lines)
        return "\n".join(s)
    
#    @classmethod
#    def toDot( cls, graph, file=None, name='SLIMpy',abr=True ):
#        if not file:
#            file = graph.log
#        
#        if isinstance( file, str ):
#            file = open( file, 'w' )
#        
#        start = 'digraph %s {\n' %name
#        end = '\n}'
#        middle = ""
#
#        for u in graph:
#            for v in graph.adj( u ):
#                
#                nodestru = cls.nodeToString(u).replace('"',"'")
#                nodestrv = cls.nodeToString(v).replace('"',"'")
#                middle += ''' "%(nodestru)s" -> "%(nodestrv)s"; \n''' %vars()
#        if abr:
#            from slimpy_base.utils.SLIMpyGlobal import GlobalVars
#            gv = GlobalVars()
#            for item in gv.abridgeMap.items():
#                middle = middle.replace(*item)
#        file.write( start )
#        file.write( middle )
#        file.write( end )

