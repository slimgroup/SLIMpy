"""
test the Worker class from the WorkerThread module
"""
from __future__ import with_statement

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


from unittest import TestCase,defaultTestLoader
from slimpy_base.Core.MutiProcessUtils.WorkerThread import Worker
from slimpy_base.Environment.InstanceManager import InstanceManager

NI = False 
class WorkerTester( TestCase ):
    env = InstanceManager()
    def testrun( self ):
        
        worker = Worker( "nodename", self.env.current_env, processor=1 )
        
        
#        with self.env['center'] as center:
            
#            worker.start()
            



    def testsafe_release_lock( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test__str__( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testmain_loop( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testprint_( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testabort( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testrun_job( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test__init__( self ):
        
        worker = Worker( "nodename", self.env.current_env, processor=1 )
        
        center = self.env['center']
        
        self.failUnless( ("nodename",1) in center.idle )
        


def suite():
    return defaultTestLoader.loadTestsFromTestCase( WorkerTester )

