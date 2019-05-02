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

class HashTableTester( TestCase ):

    def testremoveSource( self ):
        raise NotImplementedError("test not implemented")



    def test__getitem__( self ):
        raise NotImplementedError("test not implemented")



    def test__str__( self ):
        raise NotImplementedError("test not implemented")



    def test__clean__( self ):
        raise NotImplementedError("test not implemented")



    def testgetActiveSet( self ):
        raise NotImplementedError("test not implemented")



    def test__new_instance__( self ):
        raise NotImplementedError("test not implemented")



    def test__setitem__( self ):
        raise NotImplementedError("test not implemented")



    def testprintHash( self ):
        raise NotImplementedError("test not implemented")



    def testgetRef( self ):
        raise NotImplementedError("test not implemented")



    def testappend( self ):
        raise NotImplementedError("test not implemented")



    def test__contains__( self ):
        raise NotImplementedError("test not implemented")



    def testitems( self ):
        raise NotImplementedError("test not implemented")



    def testclear( self ):
        raise NotImplementedError("test not implemented")



    def testclear_at_exit( self ):
        raise NotImplementedError("test not implemented")



    def testgetHash( self ):
        raise NotImplementedError("test not implemented")



    def testvalues( self ):
        raise NotImplementedError("test not implemented")



    def test__repr__( self ):
        raise NotImplementedError("test not implemented")


    def testget_scalars_map( self ):
        raise NotImplementedError("test not implemented")

def suite():
    return defaultTestLoader.loadTestsFromTestCase( HashTableTester )

