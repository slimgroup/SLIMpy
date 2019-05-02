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

class queue(list):
    def push(self,item):
        self.insert(0,item)


class DFS(object):

    def __init__(self,G):
        self.colour = {}
        self.pi = {}
        self.d = {}
        self.time = 0
        self.f = {}
        self.G = G
        self.Top = []

        
        self.dfs()
    
    def dfs(self):
        
        for u in self.G:
            self.colour[u] = "white"
            self.pi[u] = None

        self.time = 0
        
        for u in self.G.getSourceNodes():
            if self.colour[u] == "white":
                self.dfsVisit(u)
                
    def dfsVisit(self,u):
        
        self.colour[u] = "grey"    # white vertex u has just been discovered
        self.time += 1
        self.d[u] = self.time
        
        for v in self.G.adj(u):    # explore edge (u,v)
            if self.colour[v] == "white":
                self.pi[v] = u
                self.dfsVisit(v)
                
        self.colour[u] = "black"
        self.f[u] = self.time = self.time+1
        self.Top.insert(0,u)
        
    def printPath(self,s,v):
        if v == s:
            print s
        elif self.pi[v] == None:
            print "No path from %s to %s exists" %(s,v)
        else:
            self.printPath(s, self.pi[v])
            print v

    def printTop(self):
        for u in self.Top:
            print u
    
    def printDF(self):
        print " %13s  | d | f " %("Node")
        for u in self.d.keys():
            print "  %13s  | %s | %s "%(u,self.d[u],self.f[u])



class BFS(object):

    
    def __init__(self,G,s):
        self.colour = {}
        self.d = {}
        self.pi = {}
        self.G = G
        self.bfs(s)
        


    def bfs(self,s):
        Q = queue()
        
        for u in self.G:
            self.colour[u] = "white"
            self.d[u] = None
            self.pi[u] = None
            
        self.colour[s] = "grey"
        self.d[s] = 0
        self.pi[s] = None
        Q.push(s)
        
        while len(Q) is not 0:
            u = Q.pop()
            print "u=",u,
            for v in self.G.adj(u):
                if self.colour[v] == "white":
                    self.colour[v] == "grey"
                    self.d[v] = self.d[u] + 1
                    self.pi[v] = u
                    Q.push(v)
            self.colour[u] = "black"
            
    def printPath(self,s,v):
        
        if v == s:
            print s
        elif self.pi[v] == None:
            print "No path from %s to %s exists" %(s,v)
        else:
            self.printPath(s, self.pi[v])
            print v

