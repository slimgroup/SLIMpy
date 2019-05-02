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
from slimpy_base.Core.Interface.PSpace import PSpace
from slimpy_base.Core.Command.Converter import ConstraintFunctions as cf

import unittest

NI = False
class ConstraintFunctionsTester( TestCase ):

    def testeqType( self ):
        
        space1 = PSpace('adc', data_type='complex' )
        space2 = space1.copy( )
        space3 = space1.copy( )
        
        cf.eqType( None, [space1,space2,space3] )
        
        space3['data_type'] = 'float'

        self.failUnlessRaises(TypeError, cf.eqType, None, [space1,space2,space3] )
        
        space1 = PSpace('adc' )
        self.failUnlessRaises(TypeError, cf.eqType, None, [space1] )
        
    def testeqShape( self ):
        
        space1 = PSpace('adc', n1=12, n2=12 )
        space2 = space1.copy( )
        space3 = space1.copy( )
        
        cf.eqShape( None, [space1,space2,space3] )
        
        del space3['n2']

        self.failUnlessRaises(TypeError, cf.eqType, None, [space1,space2,space3] )

        space1 = PSpace('adc', n1=12, n2=1 )
        space2 = space1.copy( )

        del space2['n2']
        
        cf.eqShape( None, [space1,space2] )
        

    def testmatch( self ):
        
        space = PSpace('adc', n1=12  )
        
        
        cf.match(space,'n1')
        cf.match(space, n1=12)
        
        self.failUnlessRaises( TypeError, cf.match,space,'n2')
        self.failUnlessRaises( TypeError, cf.match,space, n2=1)

def suite():
    return defaultTestLoader.loadTestsFromTestCase( ConstraintFunctionsTester )

if __name__ == '__main__':
    unittest.main()
