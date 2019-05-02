#!/usr/bin/env python
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
Test Space class
"""

from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.Core.User.Spaces import Space
from slimpy_base.Core.User.Structures.serial_vector import Vector
import unittest


class TestSpace( unittest.TestCase ):
    """
    Space class coresponding to vectors i.e. vectorspace
    this class contains one parameter instance
    """
    def setUp( self ):
        self.space1 = Space( n1=10, n2=10, plugin="adc" )
        self.space2 = Space( n1=10, n2=10, plugin="adc" )
        self.space3 = Space( n1=20, n2=20, plugin="adc" )
        self.space4 = Space( n1=10, n2=10, r="r", plugin="adc" )
            
    def test__init__( self ):
        """
        kparams should be like this:
            data_type
            vector_type
            n1, n2, ... nN
            o1, o2, ... oN
            d1, d2, ... dN
            ...
            other
        """ 
        self.assertRaises( TypeError, Space, ( 'a', 'b' ), {} )
        
        

        self.assert_( self.space1.has_key( 'n1' ) )
        self.assertEqual( self.space1['n1'], 10 )

        self.space1['n1'] = 23
        self.assertEqual( self.space1['n1'], 23 )

        self.assert_( self.space1.has_key( 'n2' ) )
        self.assertEqual( self.space1['n2'], 10 )

        self.assert_( self.space1.has_key( 'plugin' ) )
        self.assertEqual( self.space1['plugin'], DataContainer )

            
    def test__contains__( self ):
        pass
    
    def testgetParameters( self ):
        """
        Get parameter instance contained within class
        """
        pass
    
    def test__eq__( self ):
        """
        Two space instances are equall
        if their parameters are equal
        """
        self.assertEqual( self.space1, self.space2 )
        self.assertNotEqual( self.space1, self.space3 )
        self.assertNotEqual( self.space1, self.space4 )

    def testtestCommand( self ):
        """
        returns the reulting space from applying the command 
        but does not add the command to the graph
        """
        pass


    def test__repr__( self ):
        """
        no test
        """
        pass
    
    def testnewSpace( self ):
        
        """
        Returns a new space with changed keys
        """
        new = self.space1.newSpace()
        
        self.assertEqual( self.space1, new )
        self.assertNotEqual( id( new ), id( self.space1 ) )
        
        new = self.space1.newSpace( n1="50" )
        self.assertNotEqual( self.space1, new )
        
    
    def testgetShape( self ):
        """
        Tests that a shape from a space returns a list corrsponding to the
        n1,n2 .. values
        tests that the n1,n2 values must exist and be positive integers
        tests that ones are stripped from the end of the list
        """
        self.assertEqual( self.space1.shape, self.space1.getShape() )
        
        self.assertEqual( self.space1.shape, [10, 10] )
        self.assertEqual( self.space3.shape, [20, 20] )
        
        new = self.space1.newSpace( n1=-1 )
        self.assertRaises( TypeError, new.getShape, (), {} )
        new = self.space1.newSpace( n1=-0 )
        self.assertRaises( TypeError, new.getShape, (), {} )
        
        spc = Space( r=2, plugin="adc" )
        self.assertRaises( TypeError, spc.getShape, (), {} )
        
        new = self.space1.newSpace( n3=1 )
        self.assertEqual( new.shape, [10, 10] )

        new = self.space1.newSpace( n3=1, n4=2 )
        self.assertEqual( new.shape, [10, 10, 1, 2] )

        
    def test__len__( self ):
        """
        returns the number of elements in the vector space
        """
        self.assertEqual( len( self.space1 ), 100 )
        self.assertEqual( len( self.space3 ), 400 )
    
    
    def testcopy( self ):
        """
        performs a shallow copy of space instance
        """
        sp2 = self.space1.copy()
        
        self.assertNotEqual( id( sp2 ), id( self.space1 ) )
        self.assertEqual( sp2, self.space1 )
    
    def testmakeContaner( self ):
        """
        make an empty container from parameters
        """
        cont = self.space1.makeContaner()

        self.assertTrue( isinstance( cont, DataContainer ) )
        

    # CREATE
    #TODO: move away from the vector class
    def testcreate( self ):
        """
        Create a vector within this vectorspace
        """
        vec = self.space1.create()
        
        self.assertTrue( isinstance( vec, Vector ) )

    def testzeros( self ):
        """
        Create a vector of zeros within this vectorspace
        """
        pass
    
    def testones( self ):
        """
        Create a vector of ones within this vectorspace
        """
        pass
        
    def testisReal( self ):
        pass
    
    def testisComplex( self ):
        pass
    
    def testisInt( self ):
        pass
    
    def testtypeChange( self ):
        """
        change the data type of other to this vectorspaces' data type
        returns a new vector in this vectorspace
        """




def suite():
    return unittest.TestLoader().loadTestsFromTestCase( TestSpace )

if __name__ == '__main__':
    unittest.main()
