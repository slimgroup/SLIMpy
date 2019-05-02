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
GraphBuilder CLASS
manages the graph,the pipe builder and the runner
"""
from unittest import TestCase
from unittest import defaultTestLoader

class GraphManagerTester( TestCase ):
    """
    The graph builder class manages the builders.
    It 
    """
    def test__new_instance__(self):
        raise NotImplementedError("test not implemented")
    
    def testgetBreakpoints(self):
        raise NotImplementedError("test not implemented")
    

    def testsetBreakpoints(self):
        raise NotImplementedError("test not implemented")

    def testgetSources(self):
        raise NotImplementedError("test not implemented")

    def testsetSources( self ):
        raise NotImplementedError("test not implemented")

    def testgetTargets(self):
        raise NotImplementedError("test not implemented")
    

    def testsetTargets( self ):
        raise NotImplementedError("test not implemented")
    

    def testadd_breakpoint(self):
        raise NotImplementedError("test not implemented")

    def testadd_breakpoint_id( self ):
        raise NotImplementedError("test not implemented")

    def testadd_source( self ):
        raise NotImplementedError("test not implemented")
    
    def testadd_source_id(self ):
        raise NotImplementedError("test not implemented")
    

    def testadd_target(self ):
        raise NotImplementedError("test not implemented")
    def testadd_target_id(self ):
        
        raise NotImplementedError("test not implemented")
        
    def testgraphAppend( self ):
        raise NotImplementedError("test not implemented")
            
    def testget_graph( self ):
        raise NotImplementedError("test not implemented")    
    
    def testset_graph( self):
        raise NotImplementedError("test not implemented")
        
    
        
    def testset_builder( self ):
        """
        replace the current builders with new ones
        """
        raise NotImplementedError("test not implemented")
    
    def testget_builder( self ):
        'return builder instance'
        raise NotImplementedError("test not implemented") 
 
    
    def testsetRunner( self ):
        """
        replace the current runner with a new one
        if runner is None the current runner becomes 
        the default runner of SLIMpy
        """
        raise NotImplementedError("test not implemented")
        
    def testget_runner(self):
        raise NotImplementedError("test not implemented")

    def testflush( self ):
        """
        Complement to run , flush uses python objects instead of 
        object IDs to create a command chain
        also flush performs a clean after a graph run has been performed
        """
        raise NotImplementedError("test not implemented")
            
    def testaddBreakPoint( self ):
        """
        @type container: DataContainer
        add container to set of breakpoints
        @precondition: container is in the graph
        @postcondition: the container will always
        be built even if it breaks a pipe
         
        """
        raise NotImplementedError("test not implemented")
        
    def test__clean__( self ):
        """
        for each item in the graph try to remove its data
        """
        raise NotImplementedError("test not implemented")
            
        
    def testEnd( self ):
        """
        end  all current slimpy ativity
        runs the graph and cleans all nodes in the
        graph and hash table
        """
        raise NotImplementedError("test not implemented")

def suite():
    return defaultTestLoader.loadTestsFromTestCase( GraphManagerTester )

