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

class InstanceManagerTester( TestCase ):

    def testset_schema( self ):
        raise NotImplementedError("test not implemented")


    def testset( self ):
        raise NotImplementedError("test not implemented")


    def testEnd( self ):
        raise NotImplementedError("test not implemented")


    def test_get_lm( self ):
        raise NotImplementedError("test not implemented")


    def testget_landmark( self ):
        raise NotImplementedError("test not implemented")


    def testmanage_non_singleton( self ):
        raise NotImplementedError("test not implemented")


    def test__init__( self ):
        raise NotImplementedError("test not implemented")


    def testget_singleton( self ):
        raise NotImplementedError("test not implemented")


    def testset_env( self ):
        raise NotImplementedError("test not implemented")


    def testassure_new_instances( self ):
        raise NotImplementedError("test not implemented")


    def testset_landmark( self ):
        raise NotImplementedError("test not implemented")


    def testget_count( self ):
        raise NotImplementedError("test not implemented")


    def testget_non_singleton( self ):
        raise NotImplementedError("test not implemented")


    def testmap( self ):
        raise NotImplementedError("test not implemented")


    def test__getitem__( self ):
        raise NotImplementedError("test not implemented")


    def test__setitem__( self ):
        raise NotImplementedError("test not implemented")


    def testget_env( self ):
        raise NotImplementedError("test not implemented")


    def test__iter__( self ):
        raise NotImplementedError("test not implemented")


    def testdel_instance( self ):
        raise NotImplementedError("test not implemented")


    def test_get_instance_names( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( InstanceManagerTester )
