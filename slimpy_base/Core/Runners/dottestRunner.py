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


from slimpy_base.Core.Runners.RunnerBase import Runner
from slimpy_base.utils.DotTest import DotTester
from unittest import TextTestRunner
from sys import stdout


class dottestRunner( Runner ):
    """
    runs a dot-test on all currently defined linear operators
    does not run script
    """
    type = "dottest"
    
    def __init__( self ,places=3):
        self.places = places

    def set_graph(self, graph):
        pass
    
    def run( self ):
        """
        run the current graph with targets
        """
                
        del self.env['graphmgr']

        tester = DotTester(  )
        
        print 'running dot-tests:'
        print str( tester )
        print '-building test suite'

        suite = tester.buildTestSuite( places=self.places )
        print '-running test suite'
        testRunner = TextTestRunner( stdout, 1, 1 )
        tester.clear( )
        
        
        #Now that we are in the DotTest Runner, set the runner to the defaultRunner to run the dottest.
        from slimpy_base.Core.Runners.defaultRunner import defaultRunner as runner
        self.env['graphmgr'].setRunner( runner() )
        
        return testRunner.run( suite )

