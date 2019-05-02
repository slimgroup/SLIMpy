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
from slimpy_base.User.AumentedMatrix.AugOperator import AugOperator


class AugOperatorTester( TestCase ):

    def test_adj( self ):
        raise NotImplementedError("test not implemented")


    def testapplyop( self ):
        raise NotImplementedError("test not implemented")


    def testdomain( self ):
        raise NotImplementedError("test not implemented")




    def testgetdim( self ):
        raise NotImplementedError("test not implemented")


    def testnormalize( self ):
        raise NotImplementedError("test not implemented")


    def testminvelconst( self ):
        raise NotImplementedError("test not implemented")


    def testrange( self ):
        raise NotImplementedError("test not implemented")


    def test__mul__( self ):
        raise NotImplementedError("test not implemented")


    def test__call__( self ):
        raise NotImplementedError("test not implemented")


    def testadj( self ):
        raise NotImplementedError("test not implemented")


    def testnorm( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( AugOperatorTester )

