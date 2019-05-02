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
from slimpy_base.Core.Interface.node import Node
from slimpy_base.Environment.InstanceManager import InstanceManager
import unittest

_env = InstanceManager(  )

class NodeTester( TestCase ):
    
    def setUp(self):
        _env.End()
        _env['table'].clear( )

    def test_init( self ):
        
        e = Node( 'e' )
                
        self.failUnlessEqual( len( _env['table'] ), 1 )
        
        self.failUnless( _env['table'].has_key( e.id ) )
        
        
    def testget( self ):
        
        e = Node( 'a' )
        
        a= e.get()
        
        self.failUnlessEqual( a, 'a' )

    def testgetID( self ):
        
        e = Node( 'a' )
        
        a= e.get()
        
        self.failUnlessEqual( a, 'a' )


    def test_getattr( self ):
        
        str_b = 'b'
        
        b = Node( str_b )
        
#        b='b'
        self.failUnlessEqual(b.upper, str_b.upper) 


def suite():
    return defaultTestLoader.loadTestsFromTestCase( NodeTester )


if __name__ == '__main__':
    unittest.main()
