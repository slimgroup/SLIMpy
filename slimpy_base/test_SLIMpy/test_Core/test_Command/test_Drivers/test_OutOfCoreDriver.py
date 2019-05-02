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



class OutOfCoreDriverTester( TestCase ):

    def testformat( self ):
        raise NotImplementedError("test not implemented")


    def testgetCmnd( self ):
        raise NotImplementedError("test not implemented")


    def test__str__( self ):
        raise NotImplementedError("test not implemented")


    def test__repr__( self ):
        raise NotImplementedError("test not implemented")


    def test__call__( self ):
        raise NotImplementedError("test not implemented")


    def test__init__( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( OutOfCoreDriverTester )

