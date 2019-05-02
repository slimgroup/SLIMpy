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
Singleton class  that contains all of the global variables  
"""
from unittest import TestCase,defaultTestLoader

class GlobalVarsTester( TestCase ):
    """
    Singleton class used by slimpy to store global 
    variables
    """
#    __shared_state = {}
    
    
    def test__new_instance__( self ):
        raise NotImplementedError("test not implemented")
    
    
    def testget( self ):
        raise NotImplementedError("test not implemented")
        
    
    def testupdate(self):
        raise NotImplementedError("test not implemented")
        
    def testsetglobal( self ):
        raise NotImplementedError("test not implemented")
    
    
    def test__contains__( self ):
        raise NotImplementedError("test not implemented")
    
    def test__getitem__( self ):
        raise NotImplementedError("test not implemented")

    def test__setitem__( self ):
        raise NotImplementedError("test not implemented")
        
    def testset( self ):
        raise NotImplementedError("test not implemented")
        
    def testapplyFunc( self ):
        raise NotImplementedError("test not implemented")
    
    def testsetpath( self ):
        raise NotImplementedError("test not implemented")
                
    def testupdateAbridgeMap( self ):
        raise NotImplementedError("test not implemented")
    
    def testsetworkingdir( self ):
        raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( GlobalVarsTester )
