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
Test Case for base linear operator class
"""
from slimpy_base.Core.User.linop.linear_operator import CompoundOperator, Identity, LinearOperator
from slimpy_base.Core.User.Structures.VectorSpace import VectorSpace as Space 

from  unittest import TestCase, TestLoader


class linearoptester( TestCase ):
    """
    Test The base linear operator class.
    """
    
    def setUp( self ):
        self.dom = Space( "adc" , n1=10, n2=10)
        self.rng = Space( "adc" , n1=15, n2=15  )
        
        self.L = LinearOperator( self.dom, self.rng, adj=False )
    
    def tearDown( self ):
        pass
    
    def test__init__( self ):
        """
        check domain and range are set
        """
        
        self.assertEqual( self.L.range(), self.rng )
        self.assertEqual( self.L.range(), self.L.outSpace )

        self.assertEqual( self.L.domain(), self.dom )
        self.assertEqual( self.L.domain(), self.L.inSpace )
        
        self.assertEqual( self.L.kparams['adj'], False )


    def test__eq__( self ):

        L = self.L
        A = LinearOperator( self.dom, self.rng, adj=False )
#        B = LinearOperator( self.rng, self.dom , adj=False )
        
        self.assertEqual( L, A )
        
        self.assertNotEqual( L.adj(), L )
    
    def testcopy( self ):
        """
        Test that the copy operator returns a new 
        instance
        """
        L = self.L
        A = L.copy()
        
        self.assertEqual( L, A )
        
    def testadj( self ):
        """
        test that the adj method of the linear operator class works
        isadj should reflect the adj flag and the donmain and range 
        should be switched
        """
        L = LinearOperator( self.dom, self.rng, "test", foo="bar", adj=False )
        Lh = L.adj()
        
        self.assertFalse( L.isadj )
        self.assertTrue( Lh.isadj )
        
        self.assertEqual( L.domain(), Lh.range() )
        self.assertEqual( Lh.domain(), L.range() )
    
    def test__mul__( self ):
        """
        Not defined in this class
        """
        pass
    
    def test__call__( self ):
        """
        Not defined in this class
        """
        pass
            
    def testapplyop( self ):
        "test applyop mehtod "
        pass
    
    def testgetdim( self ):
        "test to see if the linear operator shape is working"
        dim = self.L.getdim()
        realdim = [len( self.dom ), len( self.rng )]
        self.assertEqual( dim , realdim )
        
        dim = self.L.adj().getdim()
        realdim.reverse()
        self.assertEqual( dim , realdim )
        
#    def testnorm( self ):
#        "test norm mehtod, should return Identity"
#        norm = self.L..norm()
#        self.assertTrue( isinstance( norm, Identity ) )
#        self.assertEqual( norm , Identity( self.rng ) )
#
#        norm = self.L.adj().norm()
#        self.assertTrue( isinstance( norm, Identity ) )
#        self.assertEqual( norm , Identity( self.dom ) )
#        
#        
#    def testnormalize( self ):
#        """
#        test normalize mehtod, should return a compound operator
#        of [Identity,self] 
#        """
#        norm = self.L.normalize()
#        
#        self.assertTrue( isinstance( norm, CompoundOperator ) )
#        self.assertTrue( isinstance( norm[0], Identity ) )
#        self.assertTrue( isinstance( norm[1], LinearOperator ) )
#        
#        self.assertEqual( norm[0], Identity( self.rng ) )
#        self.assertEqual( norm[1], self.L )
#        
#        
#        norm = self.L.adj().normalize()
#
#        self.assertTrue( isinstance( norm, CompoundOperator ) )
#        self.assertTrue( isinstance( norm[0], Identity ) )
#        self.assertTrue( isinstance( norm[1], LinearOperator ) )
#
#        self.assertEqual( norm[0], Identity( self.dom ) )
#        self.assertEqual( norm[1], self.L.adj() )
#
#        
#    
#    def testminvelconst( self ):
#        """
#        test returns Identity
#        """
#        minvc = self.L.minvelconst()
#        self.assertEqual( minvc, Identity( self.rng ) )
#        


def suite():
    """
    return linearoptester test suite
    """
    return TestLoader().loadTestsFromTestCase( linearoptester )
