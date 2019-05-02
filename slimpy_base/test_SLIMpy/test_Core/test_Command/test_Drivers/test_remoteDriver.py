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

class RemoteDriverTester( TestCase ):

    def testrun( self ):
        raise NotImplementedError("test not implemented")


    def test_get_stderr_logfile( self ):
        raise NotImplementedError("test not implemented")


    def testformat( self ):
        raise NotImplementedError("test not implemented")


    def testpipe_format( self ):
        raise NotImplementedError("test not implemented")


    def test__str__( self ):
        raise NotImplementedError("test not implemented")


    def testsetTarget( self ):
        raise NotImplementedError("test not implemented")


    def testset_node_name( self ):
        raise NotImplementedError("test not implemented")


    def testgetTarget( self ):
        raise NotImplementedError("test not implemented")


    def testget_targets( self ):
        raise NotImplementedError("test not implemented")


    def testget_sources( self ):
        raise NotImplementedError("test not implemented")


    def testsetSource( self ):
        raise NotImplementedError("test not implemented")


    def testget_node_name( self ):
        raise NotImplementedError("test not implemented")


    def testgetCmnd( self ):
        raise NotImplementedError("test not implemented")


    def testaddCommand( self ):
        raise NotImplementedError("test not implemented")


    def testmake_locals_list( self ):
        raise NotImplementedError("test not implemented")


    def testset_work_node( self ):
        raise NotImplementedError("test not implemented")


    def test__init__( self ):
        raise NotImplementedError("test not implemented")


    def test__call__( self ):
        raise NotImplementedError("test not implemented")


    def testgetSource( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( RemoteDriverTester )

