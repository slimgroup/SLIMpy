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


import unittest
from slimpy_base.utils.dictSeporator import dictSeporator

class TestdictSeporator(unittest.TestCase):
    
    def testNew(self):
        pass
    
    def testdictSeporator(self):
        
        ds = dictSeporator.dictSeporator
        
        self.assertEqual(ds({}) , [{}] )
        
        self.assertEqual(ds( dict(a=1) ) , [dict(a=1)] )
        
        self.assertEqual(ds( dict(a1=1),fkeys=['a','b'] ) , [dict(a=1,b=None)] )
        
        self.assertEqual(ds( dict(a=1,c=2),fkeys=['a'] ) , [dict(a=1,c=2)] )
        
        self.assertEqual(ds( dict(a=1,a1=2,a2=3),fkeys=['a'] ) , [dict(a=2),dict(a=3)] )
        self.assertEqual(ds( dict(a=1,a1=3,a2=2),fkeys=['a'] ) , [dict(a=3),dict(a=2)] )        
        
        self.assertEqual(ds( dict(b=1,a1=2,a2=3),fkeys=['a'] ) , [dict(a=2,b=1),dict(a=3,b=1)] )        
        

        
     
    def testgetNonNumberedKeys(self):
         
        gnnk = dictSeporator.getNonNumberedKeys
        self.assertEqual(gnnk(dict( )) , {}  )
        
                 
        self.assertEqual(gnnk(dict(a=1,b2=2)) , {'a':1 }  )
        self.assertEqual(gnnk(dict(a=1,a1=2)) , {'a':1 }  )
        self.assertEqual(gnnk(dict(a2=1,a1=2)) , { }  )
        
        self.assertEqual(gnnk(dict(a2=1,a1=2),fkeys=['a','b']) , { 'a': None, 'b': None }  )
        self.assertEqual(gnnk(dict(a=1,a1=2),fkeys=['a','b']) , { 'a': 1, 'b': None }  )
        
        
        
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestdictSeporator)

