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

from slimpy_base.Core.Interface.ContainerBase import DataContainer
from os.path import isfile
from slimpy_base.api.Plugins.slim2su.SU_ScalarMethods import SU_ScalarMethods

class SU_DataContainer( DataContainer ):
    
    _scalar_methods = SU_ScalarMethods
    @staticmethod
    def isCompatibleWith( obj ):
        '''
        statict method to determine if 'obj' is an su file
        @param obj:
        @type obj: any object that would be 
            contained in a datacontainer class
        '''
        
        obj = str(obj)
        
        if obj.endswith( ".su" ):
            if not isfile( obj ):
                raise Exception, "the file %s can not be found" %( obj )
            return True
        if isfile( obj+".su" ):
            return True
        
        return False 

    def getConverter( self , command ):
        '''
        return converter class
        
        command must have attribute 'function'  
        '''
        
        raise NotImplementedError
    
    
    def setName( self, newname ):
        'set the name of the data, perform a move command if neccisary'
        raise NotImplementedError
    
    def isempty( self ):
        'is the data on disk'
        raise NotImplementedError
    
    
    
    
        

    
