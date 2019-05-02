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
Test CompoundOperator class
"""
from slimpy_base.Core.User.linop.linear_operator import CompoundOperator, Identity, LinearOperator
from slimpy_base.Core.User.Structures.VectorSpace import VectorSpace as Space 
from  unittest import TestCase, TestLoader



class compTester( TestCase ):
    """
    Test CompoundOperator class
    """
    
    def setUp( self ):
        
        self.dom = Space( "adc", n1=10, n2=10  )
        self.inter = Space("adc", n1=15, n2=15 )
        self.rng = Space( "adc", n1=22, n2=22 )
        
        self.L1 = LinearOperator( self.dom, self.inter, adj=False )
        self.L2 = LinearOperator( self.inter, self.rng, adj=False )
        
        self.C = CompoundOperator( [ self.L1 , self.L2 ] )
        
    
    def test__init__( self ):
        
        self.assertRaises ( TypeError, CompoundOperator , self.L1 )
        
#        self.assertRaises(TypeError, comp, [ self.L2 ,self.L1 ] )
        
        
    def test__getitem__( self ):
        C = self.C 
        
        self.assertEqual( C[0] , self.L1 )
        self.assertEqual( C[1] , self.L2 )
        
        
    def testdomain( self ):
        
        self.assertEqual( self.C.domain() , self.L2.domain() )
        self.assertEqual( self.C.range() , self.L1.range() )
        
        CH = self.C.adj()
        
        self.assertEqual( CH.domain() , self.L1.range() )
        self.assertEqual( CH.range() , self.L2.domain() )
        

def suite():
    return TestLoader().loadTestsFromTestCase( compTester )


