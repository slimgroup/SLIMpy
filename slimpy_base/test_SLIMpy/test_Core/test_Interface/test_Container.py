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
from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.Core.Interface.PSpace import PSpace
from pdb import set_trace
import unittest

#DataContainer
NI = False

class DataContainerTester( TestCase ):

#    def testgenName( self ):
#        raise NotImplementedError("test not implemented")


#    def test_get_node_names( self ):
#        raise NotImplementedError("test not implemented")


#    def testgetScalar_methods( self ):
#        raise NotImplementedError("test not implemented")


    def test_init( self ):
        '''
        test that the init function in the DataContainer sets the right variables
        '''
        self.failUnlessRaises(TypeError, DataContainer)
        
        dc = DataContainer( "foo.test" )
        self.failIf( dc.istmp(), "DataContainer( 'foo.test' ) should not be tmp data" )
        self.failUnlessEqual( dc.nodenames, set(['localhost']) )

        
        dc = DataContainer( "foo.test", tmp=True )
        self.failUnless( dc.istmp(), "DataContainer( 'foo.test' ) should not be tmp data" )
        
#        set_trace()
        dc = DataContainer( parameters=PSpace('adc') )
        self.failUnless( dc.istmp() )
        self.failUnlessEqual( dc.nodenames, set() )
        
        dc = DataContainer( parameters=PSpace('adc') , tmp=False, 
                            target_node='r' )
        
        self.failIf( dc.istmp() )
        self.failUnlessEqual( dc.target_node, 'r' )

    def testtmp( self ):
        
        dc = DataContainer( "foo.test" )
        
        self.failIf( dc.istmp( ) )
        
        dc.tmp(True)
        
        self.failUnless( dc.istmp() )



    def test_DataContainer__is_local( self ):
        
        dc = DataContainer( "foo.test" )
        
        self.failUnless( dc.is_global )
        self.failIf( dc.is_local )
        
        
        dc = DataContainer( "foo.test" , nodenames=['node1'] )
        
        self.failUnless( dc.is_local )
        self.failIf( dc.is_global )
        
        
    def testadd_node_name( self ):
        dc = DataContainer( parameters=PSpace('adc') )
        
        self.failUnlessEqual(dc.nodenames, set() )
        
        dc.add_node_name('node1')
        
        self.failUnlessEqual(dc.nodenames, set(['node1']) )
        
        if NI: raise NotImplementedError("test not implemented")



    def testisCompatibleWith( self ):
        
        self.failUnless( DataContainer.isCompatibleWith("data.test") )
        self.failIf( DataContainer.isCompatibleWith("data.rsf") )


def suite():
    return defaultTestLoader.loadTestsFromTestCase( DataContainerTester )

if __name__ == '__main__':
    unittest.main()
