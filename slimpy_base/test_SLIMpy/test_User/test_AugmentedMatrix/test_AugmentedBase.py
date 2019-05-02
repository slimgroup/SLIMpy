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
from slimpy_base.User.AumentedMatrix.AugmentedBase import AugmentBase
from numpy import ndarray,all,array
import unittest

class AugmentBaseTester( TestCase ):
    
    def setUp(self):
        self.ab = AugmentBase( [['one',2],[3,'four']] )
        self.ab._contained_type = str
        
        self.ba = AugmentBase( [['foo'],['bar'] ] )
        self.ba._contained_type = int
    def tearDown(self):
        self.ab = None
        
    def test__pk_helper__( self ):
        """
        
        """
        ab = self.ab
        itm = ['one',2,3,4]
        itm_copy = itm[:]
        _iter = enumerate(itm)
        
        ab.__pk_helper__(_iter, itm)
        
        msg1 = "item returned by pk_helper is not 'ndarray' instance"
        self.assertEqual( len(itm_copy), len(itm) )
        for i,item in enumerate(itm):
            self.assert_( isinstance(item, ndarray) , msg1)
            self.assertEqual( ab.size, item.size )
            self.assert_( all( item == itm_copy[i] ) )
            
        
        itm = [['one']]
        _iter = enumerate(itm)

        self.assertRaises( ValueError, ab.__pk_helper__, _iter, itm )
        
        itm    = [['one','two','three',4]]
        itm_cp = [['one','two','three',4]]
        _iter = enumerate(itm)
        
        ab.__pk_helper__( _iter, itm )
        
        for val1,val2 in zip(itm,itm_cp):
            self.assert_( all(val1 == val2) )

    def test__pk_expannder__( self ):
        'test that the pk expander works'
        
        ba = self.ba
        
        pkw_obj = ba.__pk_expannder__( 1 )
        
        for p,kw in pkw_obj:
            self.assertEquals( len(p) , 1 )
            self.assertEquals( p[0] , 1 )
            
            kw_is_dict = isinstance(kw, dict)
            self.assertTrue( kw_is_dict )
            self.assertFalse( kw )
            
        pkw_obj = ba.__pk_expannder__( [1,2] )

        for i,(p,kw) in enumerate(pkw_obj):
            self.assertEquals( len(p) , 1 )
            self.assertEquals( p[0] , i+1 )
            
            kw_is_dict = isinstance(kw, dict)
            self.assertTrue( kw_is_dict )
            self.assertFalse( kw )

        pkw_obj = ba.__pk_expannder__( 1,2 , qq='rae' )

        for i,(p,kw) in enumerate(pkw_obj):
            self.assertEquals( len(p) , 2 )
            self.assertEquals( p[0] , 1 )
            self.assertEquals( p[1] , 2 )
            
            kw_is_dict = isinstance(kw, dict)
            self.assertTrue( kw_is_dict )
            self.assertEquals( len(kw), 1)
            self.assertTrue( kw.has_key('qq') )
            self.assertEqual( kw['qq'] ,'rae' )
    


    def test__obj_or_array__( self ):
        pass#raise NotImplementedError("test not implemented")
    
    
    def test__attr_func__( self ):
        ba = self.ba
        ab = self.ab
            
        pkw_obj = ba.__pk_expannder__( 1,2 )
        res = ba.__attr_func__( 'attr_not_defined', pkw_obj)
        self.assertTrue( all(res == ba) )

        pkw_obj = ab.__pk_expannder__( 1,2 )
        self.assertRaises(AttributeError,ab.__attr_func__,'attr_not_defined', pkw_obj)

        pkw_obj = ab.__pk_expannder__( 'teen' )
        res = ab.__attr_func__( '__add__', pkw_obj )
        expected_res = array([['oneteen',2],[3,'fourteen']] )
        
        self.assertTrue( all( res == expected_res) )

        pkw_obj = ab.__pk_expannder__( ['-two',0,0,'teen'] )
        res = ab.__attr_func__( '__add__', pkw_obj )
        expected_res = array([['one-two',2],[3,'fourteen']] )
        
        self.assertTrue( all( res == expected_res) )
        
def suite():
    return defaultTestLoader.loadTestsFromTestCase( AugmentBaseTester )


if __name__ == '__main__':
    unittest.main()
    
