"""
Some more Linear operators 
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


from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.Core.Interface.node import Source
from slimpy_base.Core.User.Structures.VectorType import is_vector
from slimpy_base.Core.User.linop.linear_operator import LinearOperator


## Zero a portion of a dataset based on a header mask
# @ingroup linop 
class pickingoper( LinearOperatorStruct ):
    """
    Zero a portion of a dataset based on a header mask
    """
    name = 'pick'
    __block_diagonal__ = True
    def __init__( self, inSpace, mask, axis=2 ):
        self.axis = axis
        kparams = dict( mask = Source( mask.container ) )
        
        LinearOperatorStruct.__init__( self, inSpace , **kparams )
        
    def applyop( self, other ):
        """
        Apply self to a vector other
        """            
        # must transpose the vector image to apply the transform to the proper axis
        # if a1 is equal to a2 then nothing is done
        othertransp = other.transp( a1=2, a2=self.axis )

        picadj = LinearOperatorStruct.applyop( self, othertransp )
        
        picdata = picadj.transp( a1=2, a2=self.axis )
        
        return picdata

# Create a diagonal weight from a vector or a scalar
## @ingroup linop 
class DiagonalWeight( LinearOperator ):
    """
    DiagonalWeight( domain, weight ) -> D
    diagonal weighting operator
    for D*other, if other is not a vector
    returns new DiagonalWeight instance
    """
    name = 'DiagonalWeight'
    def __init__( self, domain, weight ):
        self.weight = weight
        range = domain
        LinearOperator.__init__( self, domain, range )
        
    def applyop(self,other):
        ret = self.weight * other
        if is_vector( other ):
            return ret 
        else:
            return DiagonalWeight( self.range(), ret )
    
    
 
class weightoper( LinearOperatorStruct ):
    """
    the Input parameter must be a vecor
    """
    cmnd = 'mul'
    def __init__( self, wvec, inSpace ):
        """
        The param wvec must be able to be applied to another vector. Or is it is out of core, can be a string
        TODO if wvec is None, it is the Identity operator.
        TODO - error trap that if wvec is same type as other when applying. 
        """

        msg = "weightoper:Dont use this class!!! use DiagonalWeight"
        import warnings; warnings.warn( msg, DeprecationWarning )
        
        self.wvec = wvec
        if is_vector( wvec):
            par = Source( wvec.container )
            LinearOperatorStruct.__init__( self, inSpace, vec=par )
        if isinstance( wvec, DataContainer ):
            par = Source( wvec )
            LinearOperatorStruct.__init__( self, inSpace, vec=par )
        else:
            LinearOperatorStruct.__init__( self, inSpace, wvec )
        
    def applyop( self, other ):
        """
        apply this operator to a vector
        """
        
        return self.wvec * other

##
# @ingroup linop 
class restrictoper( LinearOperatorStruct ):
    """
    The restriction operator takes mask
    """
    name = 'restrict'
    def __init__( self, inSpace, mask):
        
        from slimpy_base.Core.User.Structures.serial_vector import Vector
        if isinstance(mask, str):
            from slimpy_base import vector
            mask = vector(mask)
        elif not isinstance(mask, Vector):
            raise TypeError( "argument 'mask' must be a 'Vector' or a 'str' instance got '%s'" %type(mask) )
        
        LinearOperatorStruct.__init__( self, inSpace, mask=Source(mask.container) )

## @ingroup linop 
class conjoper( weightoper ):
    """
    This will apply the conj operator to the input.
    """
    cmnd = 'conj'
    def __init__( self, inspace ):
        """
        Just call the superclass weight operator, that will apply the conj op.
        """
        LinearOperatorStruct.__init__( self, inspace )
        
    def applyop( self, other ):
        return other.conj()
    
## @ingroup linop 
class transpoper( LinearOperatorStruct ):
    """
    This will apply the transp operator to the input.
    """
    name = 'transp'
    def __init__( self, inspace, plane=[1,2], **kparams ):

        LinearOperatorStruct.__init__( self, inspace, plane=plane, **kparams )


class Cosine( LinearOperatorStruct ):
    """
    Cosine transform
    """
    name = 'cosinetrans'
    def __init__( self, domain , adj=False ):

        
        LinearOperatorStruct.__init__( self, domain, adj=False )
        
    






