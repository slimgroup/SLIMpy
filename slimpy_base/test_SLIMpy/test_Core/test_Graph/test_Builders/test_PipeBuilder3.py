"""
"""

#from slimpy_base.Core.Graph.Builders.PipeBuilder3 import PipeBuilder
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Core.Builders.PipeBuilder import PipeBuilder
from slimpy_base.Core.Graph.Graph.GraphPrinter import GraphPrinter
from slimpy_base.Core.Graph.Graph.DiGraph import DiGraph
#from slimpy_base.utils.GlobalVars import GlobalVars

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
test that the pipe builder is working correctly
"""

env = InstanceManager( )
import unittest


class PipeBuilderFixture( unittest.TestCase ):
    """
    compairs an expected graph with a one built with
    the pipebulider class
    """
    
    def makeGraph( self ):
        """
        returns an empty graph
        """
        return DiGraph(),set(),set(),set()
    
    def makeAns( self ):
        """
        returns an empty graph
        """
        return DiGraph()
    
    def setUp( self ):
        """
        builds the answer from the method makeGraph()
        
        """
        
        graph,targets,sources,breakpoints = self.makeGraph()
        
        pb  = PipeBuilder(  )
        
        self.pipeG = pb.build(graph,targets,sources,breakpoints)
        
#        self.pipeG = self.pipe.toGraph()
        
#        self.str_rep = GraphPrinter.printInvDep( self.pipeG )
#        self.str_repans = GraphPrinter.printInvDep( self.pipeAns )

        self.pipeAns = self.makeAns()
        
        a = set()
        b = set()
        
        for v,u in self.pipeG.iter_edges():
            a.add( (str(v), str(u) ) )

        for v,u in self.pipeAns.iter_edges():
            b.add( (str(v), str(u) ) )
        
        self.diff = a.symmetric_difference( b )
        s = []
        push = s.append
        for v,u in self.diff:
            if (v,u) in a:
                gr = "got"
            elif   (v,u) in b:
                gr = "ept"
            else:
                raise Exception
            push( "%(gr)s: %(v)s --> %(u)s" %vars())
        
        self.strdiff = "\n".join(s) 
        
    def testSameNodes( self ):
        """
        test that the expected and resulting graphs have 
        the same nodes 
        """
        sdiff = self.strdiff
        
        lenpipeg = len( self.pipeG )
        actualnodes = list( self.pipeG )
        
        lenpipeans = len( self.pipeAns )
        expnodes = list ( self.pipeAns )
        
        self.assertEqual( lenpipeg, lenpipeans , "%(lenpipeg)s != %(lenpipeans)s \n"
                                               "expected nodes: %(expnodes)s\n"
                                               "actual nodes:   %(actualnodes)s \n"
                                               "%(sdiff)s\n"
                                                %vars() )
        
        for node in self.pipeAns:
            #assert_(exp,float) is the correct formate for assert_ now.
            #self.assert_(node in self.pipeG ,
            # "%expected node:'(node)s' not in pipe" %vars())
            self.assert_( node in self.pipeG , "%(sdiff)s\n" %vars() )

    
    def testEdges( self ):
        """
        test that the expected and resulting graphs have 
        the same edges 
        """
        sdiff = self.strdiff

        ans = self.pipeAns
        
        exp = self.pipeG
        
        for node in ans:
            
            nlst = ans.adj( node )
            
            nlstexp = exp.adj( node )
            
            self.assertEqual( set( nlst ) , set( nlstexp ), 
                  "'%(nlst)s != %(nlstexp)s' given by DiGraph.adj(%(node)s)\n"
                                               "%(sdiff)s\n"
                                                %vars() )

        
class PBTest2( PipeBuilderFixture ):
    """
    d1 = c1 - d2
    """
    
    def makeAns( self ):
        
        g =  DiGraph()
        
        g.appendEdge( 'd1' , ( 'd1', 'c1' ) , False, 'black' )

        g.appendEdge( ( 'd1', 'c1' ) , 'd2' , False, 'black' )
#        g.appendEdge( ('d1','c1') , 'c1' ,False,'black')
        return g
        
    def makeGraph( self ):

        
        g = DiGraph()
        g.appendEdge( 'd1', 'c1' , True, 'red' )
        g.appendEdge( 'c1', 'd2' , False, 'green' )
#        g.setBuildTargets( 'd2' )
        
        targets = set(['d2'])
        sources = set( ['d1'] )
        breakponts = set( )
                
        return g,targets,sources,breakponts
        
    
class PBTestMIG( PipeBuilderFixture ):
    """
    d1 - mig - d2 = plus1 = d3
    """
    
    def makeAns( self ):
        
        g =  DiGraph()
        
        g.appendEdge( 'd1', ('mig',) , False, 'black' )
        g.appendEdge( ('mig',), 'd2' , False, 'black' )
        g.appendEdge( 'd2', ( 'd2', 'plus1', 'd3' ) , False, 'black' )
        g.appendEdge( ( 'd2', 'plus1', 'd3' ), 'd3' , False, 'black' )
        
#        g.appendEdge(('d1', 'c1', 'd2') , 'd2' , False, 'black')
#        g.appendEdge('d2', ('c2', 'd3') , False, 'black')
#        g.appendEdge('d3', ('c3', 'd4') , False, 'black')
#        g.appendEdge('d4', ('c4', 'd5') , False, 'black')
#        g.appendEdge('d5', ('c5', 'd6') , False, 'black')
        return g
        
    def makeGraph( self ):

        
        g = DiGraph()
        g.appendEdge( 'd1', 'mig' , False, 'red' )
        g.appendEdge( 'mig', 'd2' , False, 'green' )
        g.appendEdge( 'd2', 'plus1' , True, 'red' )
        g.appendEdge( 'plus1', 'd3' , True, 'green' )
#        g.addSource( 'd1' )
#        g.setBuildTargets( 'd3' )
        
        targets = set(['d3'])
        sources = set( ['d1'] )
        breakponts = set( )
                
        return g,targets,sources,breakponts
        
         
class PipeBuilderTestBranchAndJoin( PipeBuilderFixture ):
    """
          c1 = d2
       //         \\
    d1             c3 = d4
       \\         /
          c2 = d3 
    
    """
    def makeAns( self ):
        
        g =  DiGraph()
        g.appendEdge( ( 'd1', 'c1', 'd2', 'c3', 'd4' ), 'd4' , False, 'black' )
        
        g.appendEdge( 'd3' , ( 'd1', 'c1', 'd2', 'c3', 'd4' ) , False, 'black' )
        g.appendEdge( 'd1' , ( 'd1', 'c1', 'd2', 'c3', 'd4' ) , False, 'black' )
        
        g.appendEdge( ( 'd1' , 'c2' , 'd3' ) , 'd3' , False, 'black' )
        g.appendEdge( 'd1' , ( 'd1' , 'c2' , 'd3' )  , False, 'black' )

        return g
    
    def makeGraph( self ):

        g = DiGraph()
        g.appendEdge( 'd1', 'c1' , True, 'red' )
        g.appendEdge( 'c1', 'd2' , True, 'green' )
        g.appendEdge( 'd1', 'c2' , True, 'red' )
        g.appendEdge( 'c2', 'd3' , True, 'green' )
        g.appendEdge( 'd2', 'c3' , True, 'red' )
        g.appendEdge( 'd3', 'c3' , False, 'red' )
        g.appendEdge( 'c3', 'd4' , True, 'green' )
#        g.addSource( 'd1' )
#        g.setBuildTargets( 'd4' )
        
        targets = set(['d4'])
        sources = set( ['d1'] )
        breakponts = set( )
                
        return g,targets,sources,breakponts
        
    
class PBTest3FDCT( PipeBuilderFixture ):
    """
                   sizes
                /         \
    data  = fdct           fdctInv = final
                \\       //
                 newdata
    """
    def makeAns( self ):
        
        g = DiGraph()
        
        g.appendEdge( 'data', ( 'data' , 'fdct' , 'newdata' ) )
        
        g.appendEdge( ( 'data' , 'fdct' , 'newdata' ) , 'newdata' )
        g.appendEdge( ( 'data' , 'fdct' , 'newdata' )  , 'sizes' )
        
        g.appendEdge( 'newdata' , ( 'newdata' , 'fdctInv' , 'final' ) )
        g.appendEdge( 'sizes' , ( 'newdata' , 'fdctInv' , 'final' ) )
        
        g.appendEdge( ( 'newdata' , 'fdctInv' , 'final' ) , 'final' )
        
        return g
    
    def makeGraph( self ):
        

        g = DiGraph()
        g.appendEdge( 'data', 'fdct' , True, 'red' )
        g.appendEdge( 'fdct', 'sizes' , False, 'green' )
        g.appendEdge( 'sizes', 'fdctInv' , False, 'red' )
        g.appendEdge( 'fdct', 'newdata' , True, 'green' ) 
        g.appendEdge( 'newdata', 'fdctInv' , True, 'red' )
        g.appendEdge( 'fdctInv', 'final' , True, 'green' )
        
#        g.addSource( 'data' )
#        g.setBuildTargets( 'final' )
        
        targets = set(['final'])
        sources = set( ['data'] )
        breakponts = set( )
                
        return g,targets,sources,breakponts
        
    
    
#class PBTest6FDCT( PipeBuilderFixture ):
#    """
#     zeros = fdctmap - sizes
#                    /         \
#        data  = fdct           fdctInv = final
#                    \\       //
#                     newdata
#    """
#    def makeAns( self ):
#        
#        g = DiGraph()
#        
#        g.appendEdge( 'data', ( 'data' , 'fdct' , 'newdata' ) )
#        
#        g.appendEdge( ( 'data' , 'fdct' , 'newdata' ) , 'newdata' )
#        g.appendEdge( ( 'data' , 'fdct' , 'newdata' )  , 'sizes' )
#        
#        g.appendEdge( 'newdata' , ( 'newdata' , 'fdctInv' , 'final' ) )
#        g.appendEdge( 'sizes' , ( 'newdata' , 'fdctInv' , 'final' ) )
#        
#        g.appendEdge( ( 'newdata' , 'fdctInv' , 'final' ) , 'final' )
#        
#        return g
#    
#    def makeGraph( self ):
#        
#
#        g = DiGraph()
#        g.appendEdge( 'data', 'fdct' , True, 'red' )
#        g.appendEdge( 'fdct', 'sizes' , False, 'green' )
#        g.appendEdge( 'fdctmap', 'sizes', False, 'green' )
#        g.appendEdge( 'zeros', 'fdctmap', False, 'green' )
#        
#        g.appendEdge( 'sizes', 'fdctInv' , False, 'red' )
#        g.appendEdge( 'fdct', 'newdata' , True, 'green' ) 
#        g.appendEdge( 'newdata', 'fdctInv' , True, 'red' )
#        g.appendEdge( 'fdctInv', 'final' , True, 'green' )
#        
#        g.addSource( 'data' )
#        g.setBuildTargets( 'final' )
#        
#        return g
    
    
class PBTest4( PipeBuilderFixture ):
    
    """
     c1 = d1
             \
              c3 = d3
             /
     c2 = d2
    """
    def makeAns( self ):
        
        g = DiGraph()

        g.appendEdge( ( 'c1' , 'd1' ), 'd1' )
        g.appendEdge( ( 'c2' , 'd2' ), 'd2' )
        
        g.appendEdge( 'd1' , ( 'c3' , 'd3' ) )
        g.appendEdge( 'd2' , ( 'c3' , 'd3' ) )
        
        g.appendEdge( ( 'c3' , 'd3' ) , 'd3' )
        return g
    
    def makeGraph( self ):
        
        g = DiGraph()
        g.appendEdge( 'c1', 'd1' , True, 'green' )
        g.appendEdge( 'c2', 'd2' , True, 'green' )
        
        g.appendEdge( 'd1', 'c3' , False, 'red' )
        g.appendEdge( 'd2', 'c3' , False, 'red' )
        
        g.appendEdge( 'c3', 'd3' , True, 'green' )        

#        g.setBuildTargets( 'd3' )
        
        targets = set(['d3'])
        sources = set( )
        breakponts = set( )
                
        return g,targets,sources,breakponts
        
class PBTest5( PipeBuilderFixture ):
    """
     d1 => c2 => d3
                 \.
                 c3 => d4
                 /`
               d2
    """
    def makeAns( self ):
        
        g = DiGraph()
        
        g.appendEdge( 'd1', ( 'd1', 'c2', 'd3' ) )
        g.appendEdge( ( 'd1', 'c2', 'd3' ) , 'd3' )
        
        g.appendEdge( 'd3' , ( 'c3' , 'd4' ) )
        g.appendEdge( 'd2' , ( 'c3' , 'd4' ) )
        
        g.appendEdge( ( 'c3' , 'd4' ) , 'd4' )        

        return g
    
    def makeGraph( self ):
        

        g = DiGraph()
        g.appendEdge( 'd1', 'c2' , True, 'red' )
        
        g.appendEdge( 'c2', 'd3' , True, 'green' )
        
        g.appendEdge( 'd3' , 'c3' , False, 'red' )
        
        g.appendEdge( 'c3' , 'd4' , True, 'green' ) 
        
        g.appendEdge( 'd2' , 'c3' , False, 'red' )
        
#        g.addSource( 'd2' )
#        g.addSource( 'd1' )

        targets = set(['d4'])
        sources = set(['d1','d2'])
        breakponts = set()
                
#        g.setBuildTargets( 'd4' )
        
        return g,targets,sources,breakponts

class PBTest7( PipeBuilderFixture ):
    """

    zero = put = data  = fdct - sizes
    """
    def makeAns( self ):
        
        g = DiGraph()
        
        g.appendEdge( ( 'zero' , 'put' , 'data' , 'fdct' ) , 'sizes' )
        
        return g
    
    def makeGraph( self ):
        
        g = DiGraph()
        g.appendEdge( 'zero', 'put' , True, 'black' )
        g.appendEdge( 'put', 'data', True, 'green' )
        g.appendEdge( 'data', 'fdct' , True, 'red' )
        g.appendEdge( 'fdct', 'sizes' , False, 'green' )
#        g.setBuildTargets( 'sizes' )
        targets = set(['sizes'])
        sources = set()
        breakponts = set()
        
        return g,targets, sources, breakponts

def BandJsuite():
    tdg = unittest.TestLoader().loadTestsFromTestCase( PipeBuilderTestBranchAndJoin )
    return tdg

def PB2Suite():
    tdg = unittest.TestLoader().loadTestsFromTestCase( PBTest2 )
    
    return tdg

def PB3Suite():
    
    tdg = unittest.TestLoader().loadTestsFromTestCase( PBTest3FDCT )
    
    return tdg

def PB4Suite():
    
    tdg = unittest.TestLoader().loadTestsFromTestCase( PBTest4 )
    
    return tdg

def PB5Suite():
    
    tdg = unittest.TestLoader().loadTestsFromTestCase( PBTest5 )
    
    return tdg

def PB7Suite():
    
    tdg = unittest.TestLoader().loadTestsFromTestCase( PBTest7 )
    
    return tdg

def PBMIGSuite():
    if env['slimvars']['test_devel']:
        return unittest.TestLoader().loadTestsFromTestCase( PBTestMIG )
    else:
        return unittest.TestSuite( [] )

def suite():
    
    return unittest.TestSuite( [ BandJsuite() , PB2Suite() , PB3Suite() , PB4Suite() , 
                                 PB5Suite() , PB7Suite(), PBMIGSuite()] )


if __name__ == '__main__':
    unittest.main()
