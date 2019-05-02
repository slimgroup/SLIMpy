
"""
A SLIMpy linear operator consists of a dictionary of 
values operator_dict and an undefined pipeobject to 
be defined upon application to a vector.
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
from slimpy_base.Core.User.linop.linear_operator import  CompoundOperator
from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType
from slimpy_base.Core.Interface.node import Source


## @ingroup linop 
class mdwt1( LinearOperatorStruct ):
    """
    Rice Wavelet Toolboxes' Wavelet transform
    """
    name = "mdwt1"
    def __init__( self, inSpace, h=None, L=2, adj=False, **kparams ):
        """
        Takes h, L as paramaters. h as source so it creates it.
        """
        assert h is not None
        kparams.update( h=Source(h.getContainer()), L=L, adj=adj )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )
        
## @ingroup linop 
class mdwt2( LinearOperatorStruct ):
    """
    Rice Wavelet Toolboxes' Wavelet transform
    """
    name = "mdwt1"
    def __init__( self, inSpace, h=None, L=2, adj=False, **kparams ):
        """
        Takes h, L as paramaters. h as source so it creates it.
        """
        assert h is not None
        kparams.update( h=Source(h.getContainer()), L=L, adj=adj )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )
        

## @ingroup linop
class mrdwt1( LinearOperatorStruct ):
    """
    Rice Wavelet Toolboxes' Redundant Wavelet transform
    """
    name = "mrdwt1"
    def __init__( self, inSpace, h=None, L=2, adj=False, **kparams ):
        """
        Takes h, L as paramaters. h as source so it creates it.
        """
        assert h is not None
        kparams.update( h=Source(h.getContainer()), L=L, adj=adj )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )
          
## @ingroup linop       
class mrdwt2( LinearOperatorStruct ):
    """
    Rice Wavelet Toolboxes' Redundant Wavelet transform
    """
    name = "mrdwt1"
    def __init__( self, inSpace, h=None, L=2, adj=False, **kparams ):
        """
        Takes h, L as paramaters. h as source so it creates it.
        """
        assert h is not None
        kparams.update( h=Source(h.getContainer()), L=L, adj=adj )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )


## Wavelet transform on any axis
# @ingroup linop  
class dwt( LinearOperatorStruct ):
    """
    Wavelet transform on any axis
    """
    name = "dwt"
    
    def __init__( self, inSpace, axis= 1, type = 'linear', unit=True ):
        """
        @param unit unitary scaling
        @param type wavelet type
        """
        self.axis = axis
        kparams = dict( type = type , adj=False, unit=unit )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )

        
    def applyop( self, other ):
        """
        Apply self to a vector other
        """            
        # must transpose the vector image to apply the transform to the proper axis
        # if a1 is equal to a2 then nothing is done
        othertransp = other.transp( a1=1, a2=self.axis )

        dwttransp = LinearOperatorStruct.applyop( self, othertransp )
        
        dwtdata = dwttransp.transp( a1=1, a2=self.axis )
        
        return dwtdata
    
## Wavelet transform in two dimensions
# @ingroup linop 
@LinearOperatorType
def dwt2( inSpace, type='linear' ):
    """
    The Wavelet transform in two dimensions
    """
    return CompoundOperator( [ dwt( inSpace, type=type ), 
                              dwt( inSpace, axis=2, type=type ) ] )
    
## Wavelet transform in three dimensions    
# @ingroup linop 
@LinearOperatorType
def dwt3( inSpace, type='linear' ):
    """
    The Wavelet transform in three dimensions
    """
    return CompoundOperator( [dwt( inSpace, type=type ), 
                             dwt( inSpace, axis=2, type=type ), 
                             dwt( inSpace, axis=3, type=type )] )


