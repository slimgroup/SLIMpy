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

from slimpy_base.Core.User.Structures.VectorType import VectorType
from slimpy_base.Core.User.Structures.serial_vector import Vector
from slimpy_base.User.AumentedMatrix.AugmentedBase import AugmentBase
from slimpy_base.api.functions.scalar_functions import scalar_max,scalar_mean,scalar_min
from numpy import average, sum as npsum
from numpy import inner,outer

## Augmented vector containing vectors 
# @ingroup userclasses
# @section Example 
# Look at this example
# @code 
# >>> AugVector( [[v1,v2]])
# @endcode
# @page foo
# this is foo
class AugVector( AugmentBase ):
    """
    class containing vectors
    used in an augmented system of equations
    \see slimpy_base.Core.User.Structures.serial_vector.Vector
    """
    
    _contained_type = Vector
    __metaclass__ = VectorType

    __transpose_flag = False
    
    def _get_meta(self):
        if not hasattr(self, '_meta_space' ):
            self._meta_space = None
        return self._meta_space
    
    def _set_meta(self,val):
        self._meta_space = val
    
    meta = property(_get_meta, _set_meta )
    
    def _get_meta_vec(self):
        if hasattr(self, "_meta_vector" ):
            return self._meta_vector
        else:
            return None
        
    def _set_meta_vec( self, val ):
        
        self._meta_vector = val
    
    meta_vector = property( _get_meta_vec, _set_meta_vec )
    
    def _get_params(self):
        return self.space 
    
    params = property( _get_params )
    
    def _get_transp_flag(self):
        return self.__transpose_flag
    def _set_transp_flag(self,val):
        self.__transpose_flag = bool(val)
    
    
    def _conj_transp(self):
        pkw_obj = self.__pk_expannder__( )
        aug_vec =  self.__attr_func__( '_conj_transp' ,pkw_obj )
        aug_vec.is_transp = not self.is_transp
        return aug_vec
        
    H = property( _conj_transp )
    
    
    def __mul__( self, other ):
        isvec =  (type(type(other) ) == VectorType)
        if isvec and (self.is_transp ^ other.is_transp):
            if self.is_transp:
                return inner( self.flat, other.flat )
            else:
                return outer( self, other )
        else:
            return AugmentBase.__mul__(self, other)
        
    is_transp = property( _get_transp_flag, _set_transp_flag ) 
 
    def thr( self, obj, mode='soft' ):
        pkw_obj = self.__pk_expannder__( obj, mode=mode )
        return self.__attr_func__( 'thr', pkw_obj )
    
    def flush( self ):
        pkw_obj = self.__pk_expannder__( )
        self.__attr_func__('flush', pkw_obj)
     
    def setName(self,name):
        pkw_obj = self.__pk_expannder__( name )
        self.__attr_func__('setName', pkw_obj)

    def noise(self,mean=0):
        pkw_obj = self.__pk_expannder__( mean=mean )
        return self.__attr_func__('noise', pkw_obj)
        
    def __real__(self):
        pkw_obj = self.__pk_expannder__(  )
        return self.__attr_func__('real', pkw_obj)

    def __imag__(self):
        pkw_obj = self.__pk_expannder__(  )
        return self.__attr_func__('imag', pkw_obj)
        
    real = __real__
    imag = __imag__
    
    def getSpace(self):
        "getSpace"
        from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
        
        pkw_obj = self.__pk_expannder__(  )
        new = self.__attr_func__('getSpace', pkw_obj)
        
        new_meta =  new.view( MetaSpace )
        new_meta._contained_type = MetaSpace._contained_type
        
        new_meta = new_meta.ravel( )
        new_meta.meta = self.meta 
        return new_meta
    
    def orderstat(self , ind):
        """
        gets the ind-th element of the sorted self
        
        returns an average of the ind-th element in all vectors 
        """
        glo = self.space.get_size( )
        loc = self.space.get_local_sizes( )
        
        perc = loc * float(ind) / glo
        
        
        pkw_obj = self.__pk_expannder__( perc.astype(int) )
        ostat =  self.__attr_func__( 'orderstat', pkw_obj )
        
        return average( ostat.reshape(-1) ) 

    def rms( self ):
        """    Returns the root mean square"""
        raise NotImplementedError
    
    def max( self ):
        "Returns the maximum value contained in the vector"
        pkw_obj = self.__pk_expannder__( )
        mmax =  self.__attr_func__('max', pkw_obj)
        mmax = mmax.reshape(-1).tolist()
        return scalar_max( mmax )
    
    def min( self ):
        """    Returns the minimum value"""
        pkw_obj = self.__pk_expannder__( )
        mmin =  self.__attr_func__('min', pkw_obj)
        mmin = mmin.reshape(-1).tolist()
        return scalar_min( mmin )

    def mean( self ):
        "Returns the mean value"
        pkw_obj = self.__pk_expannder__( )
        means =  self.__attr_func__( 'mean', pkw_obj )
        means = means.reshape(-1).tolist()

        return scalar_mean( means )

    
    def var( self ):
        "Returns the variance"
        raise NotImplementedError
    def sdt( self ):
        "Returns the std deviation"
        raise NotImplementedError
    
    def norm( self, lval=2 ):
        "Returns the lval norm of the vector"
        pkw_obj = self.__pk_expannder__( lval=lval )
        mnorm =  self.__attr_func__( 'norm', pkw_obj )
        
        if lval == 0: 
            root = 0
        else:
            root = 1./lval
            
        vec = mnorm ** lval
        nrm = npsum( vec ) ** root
        
        return nrm 

    space = property( getSpace )        
