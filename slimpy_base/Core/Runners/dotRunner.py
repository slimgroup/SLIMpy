
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
from string import Template
from slimpy_base.Core.Runners.RunnerBase import Runner
#from slimpy_base.Core.Graph.Builders.DotBuilder import DotBuilder


subgraph = Template("""
subgraph ${node}${proc} {
    label = "${node}: ${proc}";
    style= "dashed";
    color=black;
        
    ${content}
}
""")

class dotRunner( Runner ):
    """
    prints a Graphvis dot file to stdout
    """
    type = "dot"
    
    def __init__( self ,records=None):
        self.records = records
        Runner.__init__( self )
        
    def set_graph(self, graph):
        self.counterC = 0
        self.counterD = 0

        self.graph = graph
        self.dot = self.toDot( graph, name="SLIMpy", abr=True )
        
    def run( self ):
        """
        run the current graph with targets
        """        
#        dot = DotBuilder( self.graph )
        print self.dot
        

    def printDot( self ):
        """
        returns self.dot
        """
        return self.dot
    
    def toDot( self, graph, name='SLIMpy', abr=True ):
        """
        build string representation of graph in do form
        """
        start = 'digraph %s {\n' % name
        end = '\n}'
        datastr = 'node [shape = "ellipse",color=green];\n\n'
        commstr = 'node [shape = "box",color=red];\n\n'
        middle = "\n\n"
        
        dataDict = {}
        commandDict = {}
        node_dict = {}
        
        for u in graph:
            for v in graph.adj( u ):
                
                key1,nodestru = self.nodeToString( u, dataDict, commandDict )
                key2,nodestrv = self.nodeToString( v, dataDict, commandDict )
                
                self.add_to_node_dict(key1, key2, nodestru, nodestrv, node_dict)
#                middle += '''%(nodestru)s -> %(nodestrv)s; \n''' %vars()
        
        datastr += "\n".join( ['%(val)s [ label = "%(key)s" ]' %vars() for key, val in dataDict.items()] ) +"\n\n\n"
        commstr += "\n".join( ['%(val)s [ label = "%(key)s" ]' %vars() for key, val in commandDict.items()] ) + '\n\n\n'
        
        middle = self.node_dict_to_str(node_dict)
        
        return self.abbrige( start + datastr + commstr + middle + end, abr )
    
    def abbrige( self, s, abr ):
        if abr:
            for item in self.env['slimvars']['abridgeMap'].items():
                s = s.replace( *item )
                
        return s
    
    def node_dict_to_str(self,nd):

        result = ""
        
        for key,val in nd.iteritems():
            if key == ('localhost',''):
                result += "\n".join(val)
            else:
                name,proc = key
                content = "\n".join(val)
                result += subgraph.substitute(node=name,
                                              proc=proc,
                                              content=content)
        return result
    
    def add_to_node_dict(self,key1,key2,u,v,nd):
        
        middle = '''%(u)s -> %(v)s; \n''' %vars()
        
        globl = ('localhost','')
        if key1 and key2 and key1 == key2:
            lst = nd.setdefault( key1, [] )
            lst.append(middle)
        elif key1 or key2:
            key = key1 or key2
            lst = nd.setdefault( key, [] )
            lst.append(middle)
        
        else:
            lst = nd.setdefault( globl, [] )
            lst.append(middle)
        
    def nodeToString( self, node, dataDict, commandDict ):
        """
        function to work with data in the hashtable 
        """
        table = self.env['table']
        
        key = None
        if self.records:
#            print "self.records"
            for rec in self.records:
#                print rec.name,node
                if rec.name == node:
                    key = rec.node_info
        if isinstance( node, tuple ):
            nodes = [table[n] for n in node ]
            runnable = self.add( nodes )
            s = runnable.nice_str().replace( '"', "'" )
            
            val = "c%d" %self.counterC
            if commandDict.has_key( s ):
                return key,commandDict[s]
            else:
                self.counterC+=1
                commandDict[s] = val
            
            return key,val
                
            
        else:
            nodes =  table[node]
        
            s = str( nodes ).replace( '"', "'" )
            
            val = "d%d" %self.counterD
            
            if dataDict.has_key( s ):
                return key,dataDict[s]
            else:
                self.counterD+=1
                dataDict[s] = val
            return key,val
                        
