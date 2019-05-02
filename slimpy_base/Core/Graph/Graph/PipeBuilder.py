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

from slimpy_base.Core.Graph.Graph.DiGraph import DiGraph


class PipeBuilder(object):

    def __init__(self,g,sources,*targets):

        self.Colour = {}
        self.G = g
        self.lst = []
        self.done = {}
        self.colourSources(sources)
        self.bld(*targets)

    
    def colour(self,node):
        return self.Colour.get(node,'white')

        
    
    def bld(self,*targets):
        print self.G.buildTargets.union(targets)
        for target in self.G.buildTargets.union(targets):
    
            if self.colour(target) == 'grey':
                continue
            
            ff = True
#            if not self.isSource(target):
            List = {'Target':[target],'Command':[target],'Source':[]}
            self.lst.append(List)
            dep = self.G.invAdj(target)


            for node in dep:

                sig = ff
                stdinFlag = self.G.invAdjacencyList[target][node]
                depFlag = len(self.G.adjacencyList[node]) <=1

                self.c2(ff, stdinFlag, depFlag, List, node)
                
        return
                
    def createCom(self,node,List):
        ff = True
        dep =  self.G.invAdj(node)

        for prev in dep:
            
            stdinFlag = self.G.invAdjacencyList[node][prev]
            depFlag = len( self.G.adjacencyList[prev] ) <= 1

            #depFlag = True
            
            ff == self.c2(ff, stdinFlag, depFlag, List, prev)

    def c2(self, ff, stdinFlag, depFlag, List, prev):
        sig = ff
        if ff and stdinFlag and depFlag:
            ff = False
            List['Command'].insert(0,prev)
            if not self.colour(prev) == 'grey':
                self.Colour[prev] = 'grey'
                self.createCom(prev, List)
        else:
            List['Source'].append(prev)
            
            if not self.colour(prev) == 'grey':
                
                newList = {'Target':[prev],'Command':[prev],'Source':[]}
                self.lst.insert(0,newList)
                self.Colour[prev] = 'grey'
                self.createCom(prev, newList)
                
        if sig and stdinFlag and not depFlag:
 
            List['Command'].insert(0,prev)
            
        return ff
    
    def toGraph(self):
        g = DiGraph()
        
        for l in self.lst:
            
            for source in l['Source']:
                g.appendEdge(source, tuple(l['Command']))
            for target in l['Target']:
                g.appendEdge( tuple(l['Command']),target)
        
        g.setBuildTargets(*self.G.buildTargets)
        
        return g


    
    
    


