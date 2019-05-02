
"""
Aumented operator class
"""

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

from slimpy_base.Core.User.Structures.VectorSpace import VectorAddition
from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType,is_oper
from slimpy_base.Core.User.linop.linear_operator import LinearOperator, CompoundOperator
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.User.AumentedMatrix.AugmentedBase import AugmentBase
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
from slimpy_base.api.linearops.ScatterOperator import apply_along_axis

from numpy import mat, diag, ndarray, asarray #IGNORE:E0611
from pdb import set_trace
from slimpy_base.api.linearops.transforms import DiagonalWeight

from slimpy_base.Core.User.Structures.Scalar import is_scalar_obj
from slimpy_base.Core.User.Structures.Scalar import is_number

is_array = lambda item: isinstance( item , ndarray )


## @ingroup linop
class AugOperator( AugmentBase ):
    """
    augmented operator is a matrix of Linear Operators
    ie.
    Aug = AugOperator( meta_space, [ [A,0], 
                                     [0,A] ] )
    new_vec = Aug * aug_vec
    """
    def __new__(cls, *pars, **kw ):
        from slimpy_base.Core.Interface.PSpace import PSpace
        if pars:
            meta = pars[0]
            if len(pars) < 2 or not isinstance( meta, PSpace ):
                meta = None
            else:
                pars = pars[1:]
            
            new_aug_oper = AugmentBase.__new__( cls, *pars, **kw )
            new_aug_oper.meta = meta
             
        else:
            new_aug_oper = AugmentBase.__new__( cls, *pars, **kw )
            
        ndim = new_aug_oper.ndim
        if ndim != 2:
            raise TypeError("AugOperator should have dim 2, got only dim %s matrix" %(ndim) )
        
        return new_aug_oper
        
        
    _contained_type = LinearOperator
    __metaclass__ = LinearOperatorType

    def _get_meta_rng(self):
        if not hasattr(self, '_meta_space_rng' ):
            self._meta_space_rng = None
        return self._meta_space_rng
    
    def _set_meta_rng(self,val):
        self._meta_space_rng = val

    def _get_meta_dom(self):
        if not hasattr(self, '_meta_space_dom' ):
            self._meta_space_dom = None
        return self._meta_space_dom
    
    def _set_meta_dom(self,val):
        self._meta_space_dom = val
        
    def _set_meta(self,val):
        self._meta_space_dom = val
        self._meta_space_rng = val
        
    meta = property( fset=_set_meta )
    meta_domain = property( _get_meta_dom, _set_meta_dom )
    meta_range = property( _get_meta_rng, _set_meta_rng )
    
    def copy( self ):
        new = AugmentBase.copy( self )
        
        new.meta_domain = self.meta_domain
        new.meta_range = self.meta_range
        return new 
    
    def domain( self ):
        """
        return inSpace
        """
        
        pkw_obj = self.__pk_expannder__()
        dom = self.__attr_func__( "domain", pkw_obj )
        
        colspace = apply_along_axis( lambda axis:VectorAddition( axis.tolist() ) ,0, dom )
        
        if colspace.size == 1:
            return colspace.item()
        
        colspace = colspace.view( MetaSpace )
        colspace.meta = self.meta_domain
        
        return colspace
#        return diag( dom ).reshape( -1, 1 ).view( MetaSpace )
    
    def range( self ):
        """
        return outSpace
        """
        pkw_obj = self.__pk_expannder__()
        rng = self.__attr_func__( "range", pkw_obj )
#        rng = rng.view( MetaSpace )
#        rng.meta = self.meta_range

        rowspace = apply_along_axis( lambda axis:VectorAddition( axis.tolist() ) ,1, rng )

        if rowspace.size == 1:
            return rowspace.item()
        
        rowspace = rowspace.view( MetaSpace )
        rowspace.meta = self.meta_domain

        return rowspace
            
    def adj( self ):
        """
        The adjoint flips the operator_dict key transp. and updates the domain and range.
        """
        
        adj = self.transpose( ) #IGNORE:E1101
        
        pkw_obj = self.__pk_expannder__()
        SH = adj.__attr_func__( 'adj', pkw_obj )
        
        SH.meta_range = self.meta_range
        SH.meta_domain = self.meta_domain
        
        return SH
    
    H = property( adj )
    
    def _getadj( self ):
        "get the adj key in the kparams"
        raise NotImplementedError

    def _setadj( self, val ):
        "set the adj key in the kparams"
        raise NotImplementedError
    
    isadj = property( _getadj , _setadj )
    
    def __mul__( self, other ):
        """
        Not defined in this class
        """
        return self.applyop( other )
    
    def __call__( self, other ):
        """
        Not defined in this class
        """
        return self.applyop( other )
            
    def applyop( self, other ):
        
        if is_oper( other ):
            return CompoundOperator( [self, other] )
        import pdb
        if is_number( other ):
            new = self.copy( )
            for i, oper in enumerate(new.flat):
                if is_oper( oper ):
                    D = DiagonalWeight( oper.range(), other )
                    C = CompoundOperator( [oper, D] )
                elif oper is 0:
                    C = 0
                else:
                    C = oper * other
                    
                new.flat[i] = C
                
            return new
        
        n = self.shape[1]
        m = 1
        if is_array( other ): m = other.size
        
        assert m == n, "AugOperator expected an Augment Vector of length %s, got length %s" %(n,m) 
        
        
        if is_array( other ):
            other_long_vector = other.reshape( [-1, 1] )
            new = mat( self ) * other_long_vector
            
        else: # other is not a augmented vector
            new = asarray( self ) * other
        
        if is_array( new ):
            other_cls = AugVector
            if new.size == 1:
                ret = new.item()
            else:
                ret = new.view( other_cls )
        else: ## assume 1x1 aug oper
            ret = new
        
        if is_array( ret ):
            ret.meta = self.meta_range
            
        return ret
         
         
    def getdim( self ):
        """
        Returns the dimensions of the operator. Usually not defined.
        """
        raise NotImplementedError
        return [ len( self.domain( ) ), len( self.range( ) )]
        
    def norm( self ):
        """
        returns Identity
        """
        raise NotImplementedError
    
    def normalize( self ):
        """
        returns comp( [self.norm(), self] )
        """
        raise NotImplementedError
    
    def minvelconst( self, *args, **kargs ):
        """
        returns Identity
        """
        raise NotImplementedError
 
