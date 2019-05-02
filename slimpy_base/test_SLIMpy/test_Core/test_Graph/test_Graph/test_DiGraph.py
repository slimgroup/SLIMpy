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

import unittest

from slimpy_base.Core.Graph.Graph.DiGraph import DiGraph
from slimpy_base.Core.Graph.Graph.tests import mk3

class TestDiGraph(unittest.TestCase):

    def setUp(self):
        
        self.srcnodes = ['d1']
        g = self.makeG()
        
        self.g = g

    def makeG(self):
        g = DiGraph()
        g.appendEdge( 'd1', 'c1' ,True,'red')
        g.appendEdge( 'c1', 'd2' ,True,'green')
        g.appendEdge( 'd1', 'c2' ,True,'red')
        g.appendEdge( 'c2', 'd3' ,True,'green')
        g.appendEdge( 'd2', 'c3' ,True,'red')
        g.appendEdge( 'd3', 'c3' ,False,'red')
        g.appendEdge( 'c3', 'd4' ,True,'green')
        return g
    def tearDown(self):
        del self.g


#    def testSetGetBuildTargets(self):
#        self.g.setBuildTargets('d4')
#        
#        buildtargets = self.g.getBuildTargets()
#        
#        self.assertEquals(1,len(buildtargets))
#        
#        self.assert_('d4' in buildtargets)
#        
#        self.g.setBuildTargets('d3')
#        
#        buildtargets = self.g.getBuildTargets()
#        
#        self.assertEquals(2,len(buildtargets))
#        
#        self.assert_('d4' in buildtargets and 'd3' in buildtargets)
#        
#        self.assertRaises(AssertionError, self.g.setBuildTargets,('notInGraph',))
        
    def testAppendEdge( self ):
        g = DiGraph()
        g.appendEdge( 'd1', 'c1' ,True,'red')
        

        self.assert_('d1' in g)
        self.assert_('c1'in g)
        
        self.assertEqual( g.adj('d1') , ['c1'] , "test that d1 -> c1")
        self.assertRaises( KeyError , g.adj,('c1',) ) # "test that c1 -/> d1" 
        
        self.assertEqual( g.invAdj('c1') , ['d1'] , "test that c1 <- d1 in inv")
        self.assertRaises( KeyError , g.invAdj,('d1',) ) # "test that c1 -/> d1 in inv" 
        
         
        self.assert_(g.getEdge('d1', 'c1'))
        self.assert_(g.getEdge('c1', 'd1'))
        
        self.assertEqual(g.getEdgeColour('d1', 'c1') , 'red')
        self.assertEqual(g.getEdgeType('d1', 'c1') , True)        
    

    def testIter( self ):
        
        setofG  = set(self.g)
        
        complete = set(['c1','d1', 'c2','d2','d3',  'c3','d4'])
        
        
        
        self.assertEqual(setofG , complete, "test that all of the nodes are represented with iter")
        
        
        self.assertEqual( set ( self.g.getAllNodes() ),complete)

#    def testAddSource(self):
#        g = self.g
#        
#        g.addSource('d3')
#        
#        self.assertEqual(g.getSources(),set(['d3']))
#        
#        self.assertEqual(g.getSources(),set(['d3']))
    

    
    def testGetSourceNodes( self ):
        self.assertEqual( list(self.g.getSourceNodes()) , self.srcnodes )
        
        g = DiGraph()
        g.appendEdge( 'd1', 'c1' ,True,'red')
        g.appendEdge( 'd2', 'c2' ,True,'green')
        
        self.assertEqual( set(g.getSourceNodes() ) , set( ['d2','d1'] ) )
        
        
    
    def testClean(self):
        
        self.g.clean()
        
        self.assertEqual(0 , len(self.g))
        
class TestDiGraphTransp(TestDiGraph):
    def setUp(self):
        self.srcnodes = ['d4']
        g = self.makeG()
        self.g = g.transp()

def tdgsuite():
    tdg = unittest.TestLoader().loadTestsFromTestCase(TestDiGraph)
    return tdg

def tdgtsuite():
    tdg = unittest.TestLoader().loadTestsFromTestCase(TestDiGraphTransp)
    return tdg


def suite():
    
    return unittest.TestSuite( [ tdgsuite() , tdgtsuite() ] )

