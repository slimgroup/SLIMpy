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

from unittest import  TestCase,TestLoader
import unittest

TestLoader.loadTestsFromModule

from slimpy_base.Environment.Singleton import Singleton

class TestSingleton( TestCase ):
    
    def setUp(self):
        self.s1 = Singleton( 's1')
        self.s2 = Singleton( 's2')
    
    def tearDown(self):
        Singleton.__del_instance__('s1')
        Singleton.__del_instance__('s2')
        
        self.assertEquals(Singleton._num_instances(),0)
        
    
    def testcreate_singleton(self):
        
        s1 = self.s1
        s2 = self.s2
        s1.foo = 1
        s2.foo = 2
        
        s3 = Singleton( 's1' )
        
        self.assertNotEqual( s1.foo, s2.foo)
        self.assertEqual( s1.foo, s3.foo)
        
        s3.__del_instance__( 's1' )
        
        s4 = Singleton( 's1' )
        
        self.assertRaises( AttributeError, getattr, s4, 'foo' )
        
        error_singleton = type('newsingleton',(Singleton,) , {'__init__':lambda self:None})
        
        self.assertRaises(TypeError, error_singleton, 's1')
        
        newsingleton = type('newsingleton',(Singleton,) , {} )
        
        ns = newsingleton('s2')
        
        self.assertEquals( ns._instance_name, 's2' )
        self.assertRaises( AttributeError, getattr, ns, 'foo' )
        
    def test__clean__(self):
        pass # raiseNotImplementedError("test not implemented")
        
    
    def test_num_instances( self ):
        
        self.assertEquals( Singleton._num_instances(), 2)
        
        Singleton.__del_instance__( 's1' )
        
        self.assertEquals( Singleton._num_instances(), 1)

        
def suite():
    return TestLoader().loadTestsFromTestCase(TestSingleton)

if __name__ == '__main__':
    unittest.main()

