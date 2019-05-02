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
from slimpy_base.Core.MutiProcessUtils.EmploymentCenter import EmploymentCenter

center = EmploymentCenter( 'test_env' )

NI = False

class EmploymentCenterTester( TestCase ):
    
    def setUp(self):
         
        center.__del_instance__( 'test_env' )
        center.__new_instance__( 'test_env' )
        
        center.subscribe('name', 'proc')
        
    def tearDown(self):
        pass
    
    def testhas_nothing_todo( self ):
        
        self.failUnless( center.has_idle() )
        self.failUnless( center.has_nothing_todo( 'name', 'proc' ) )
        
        center.post( 'name', 'proc', 'job123' )
        
        self.failIf( center.has_idle() )
        self.failIf( center.has_nothing_todo( 'name', 'proc' ) )
        
        job_id = center.get_my_job( 'name', 'proc' )
        center.finished( 'name', 'proc', job_id )

        self.failUnless( center.has_idle() )
        self.failUnless( center.has_nothing_todo( 'name', 'proc' ) )


    def testpop( self ):
        np = ('name', 'proc')
        
        self.failUnlessEqual( center.pop(), np )


    def testnotify( self ):
        
        center.notify( 'name' , 'proc')
        post = center[ 'name' , 'proc' ]
        
        self.failUnless( post.event.isSet() )
        

    def testremove_from_waiting_list( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testhas_todo( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test_get_nodenames( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testset_alarm( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testreset( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testset_event( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testwait_for_avail( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test__getitem__( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testacquire( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testabort_all( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testfinished( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testadd_to_waiting_list( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test_get_error( self ):
        if NI: raise NotImplementedError("test not implemented")

    def testpost( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testwait_for_job( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testdump_finished( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testformat_poc( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testprettyprint( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testhas_idle( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testrelease( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test_get_done( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testget_my_job( self ):
        if NI: raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( EmploymentCenterTester )


