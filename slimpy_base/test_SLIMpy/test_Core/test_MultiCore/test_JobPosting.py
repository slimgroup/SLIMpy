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

class JobPostingTester( TestCase ):

    def testtotal_time( self ):
        raise NotImplementedError("test not implemented")


    def testget( self ):
        raise NotImplementedError("test not implemented")


    def testacquire( self ):
        raise NotImplementedError("test not implemented")


    def teststop_timer( self ):
        raise NotImplementedError("test not implemented")


    def testis_working( self ):
        raise NotImplementedError("test not implemented")


    def testfinished( self ):
        raise NotImplementedError("test not implemented")


    def testnotify( self ):
        raise NotImplementedError("test not implemented")


    def testnew_todo( self ):
        raise NotImplementedError("test not implemented")


    def test_get_waiting( self ):
        raise NotImplementedError("test not implemented")


    def testpost( self ):
        raise NotImplementedError("test not implemented")


    def testwait_for_job( self ):
        raise NotImplementedError("test not implemented")


    def test__init__( self ):
        raise NotImplementedError("test not implemented")


    def testbusy( self ):
        raise NotImplementedError("test not implemented")


    def test_set_waiting( self ):
        raise NotImplementedError("test not implemented")


    def testget_time_since_start( self ):
        raise NotImplementedError("test not implemented")


    def testhas_todo( self ):
        raise NotImplementedError("test not implemented")


    def testrelease( self ):
        raise NotImplementedError("test not implemented")


    def teststart_timer( self ):
        raise NotImplementedError("test not implemented")


    def testtime_idol( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( JobPostingTester )

