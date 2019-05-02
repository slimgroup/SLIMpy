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

from slimpy_base.User.AumentedMatrix.AugmentedBase import AugmentBase
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.Core.Interface.PSpace import PSpace
from numpy import all, ndarray
from slimpy_base.Core.Interface.Structure import Structure

## A space containing many spaces is used with AugOperator and AugVector 
# @ingroup userclasses
class MetaSpace( AugmentBase ):
    """
    """
    _contained_type = PSpace
    
    
    def _get_meta(self):
        if not hasattr(self, '_meta_space' ):
            self._meta_space = None
        return self._meta_space
    
    def _set_meta(self,val):
        self._meta_space = val
    
    meta = property(_get_meta, _set_meta )
    
    def has_key( self, k ):
        raise NotImplementedError
    
    def __contains__( self, obj ):
        """
        Test if a vector is in this space
        """
        pkw_obj = self.__pk_expannder__( obj )
        boo_array = self.__attr_func__( "__contains__", pkw_obj )
        return all(boo_array)
        
        
    def getParameters( self ):
        """
        Get parameter instance contained within class
        """
        raise NotImplementedError
    
    def makeContaner(self, command=None, tmp=None):
        
        pkw_obj = self.__pk_expannder__( command=command,tmp=tmp )
        container_array = self.__attr_func__("makeContaner", pkw_obj)
        return container_array.view( ndarray )
    
        
    def testCommand( self, cmd_tag, *args, **kargs ):
        """
        returns the reulting space from applying the command 
        but does not add the command to the graph
        """
        
        """
        returns the reulting space from applying the command 
        but does not add the command to the graph
        """
        new_space = Structure.testCommand( self, cmd_tag, *args, **kargs )
        assert new_space is not None
        
        return new_space
    
    def newSpace( self, *d, **keys ):
        """
        Returns a new space with changed keys
        """
        raise NotImplementedError
    
      
    # CREATE
    #TODO move away from the vector class
    def create( self, out=0, istmp=True ):
        """
        Create a vector within this vectorspace
        """
        pkw_obj = self.__pk_expannder__( out=out, istmp=istmp )
        container_array = self.__attr_func__("create", pkw_obj)
        augvec = container_array.view( AugVector )
        augvec.meta = self.meta
        return augvec

    def noise( self ):
        """
        Create a vector within this vectorspace
        """
        pkw_obj = self.__pk_expannder__( )
        container_array = self.__attr_func__("noise", pkw_obj)
        augvec = container_array.view( AugVector )
        augvec.meta = self.meta
        return augvec
        

    def zeros( self ):
        """
        Create a vector of zeros within this vectorspace
        """
        return self.create()
    
    def ones( self ):
        """
        Create a vector of ones within this vectorspace
        """
        return self.create( out=1 )  
        
    def isReal( self ):
        pkw_obj = self.__pk_expannder__(  )
        bool_array = self.__attr_func__("isReal", pkw_obj)
        
        return all(bool_array)
#        raise NotImplementedError
    
    def isComplex( self ):
        pkw_obj = self.__pk_expannder__(  )
        bool_array = self.__attr_func__("isComplex", pkw_obj)
        
        return all(bool_array)
    
    def isInt( self ):
        pkw_obj = self.__pk_expannder__(  )
        bool_array = self.__attr_func__("isInt", pkw_obj)
        
        return all(bool_array)
    
    def get_local_sizes( self ):
        
        pkw_obj = self.__pk_expannder__(  )
        size_array = self.__attr_func__("get_size", pkw_obj)
        size_array = size_array.view( ndarray ).astype( int )
        
        return size_array
        
    def get_size( self ):
        """
        retuns the total number of elements in the augmented vector
        """
        size = self.get_local_sizes( )
        
        return size.sum()
    
    def coalesce(self):
        slist = self.ravel().tolist()
        return PSpace.union( *slist )
    
    def _get_plugin(self):
        return self[0].plugin
    
    plugin = property( _get_plugin )
    
    def copy(self):
        pkw_obj = self.__pk_expannder__(  )
        copy_array = self.__attr_func__("copy", pkw_obj )
        if self.meta is not None:        
            copy_array.meta = self.meta.copy()
            
        return copy_array
        
    
