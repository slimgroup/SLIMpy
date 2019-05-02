"""
contains the curvelet transforms in 2d and 3d.
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
#from slimpy_base.api.linearops.transforms import weightoper
from slimpy_base.api.functions.functions import clnorm
#from slimpy_base.api.functions.functions import curveletNorm
import warnings

#_fdct2__weightoper = __weightoper


## curvelet transform in three dimensions.
# @ingroup linop
class fdct3( LinearOperatorStruct ):
    """
    The fast discrete curvelet transform in three dimensions.
    """
    name = "fdct3"
    __block_diagonal__ = True
    def __init__( self, inSpace, nbs, nbd, ac, cpxIn=False, adj=False ):
        
        LinearOperatorStruct.__init__( self, inSpace, nbs=nbs, nbd=nbd, ac=ac, adj=adj, cpxIn = cpxIn )

    def applyop( self, other ):
        """
        overload the applyop to take into account the sizes file.
        sets a breakpoint in the graph to build the data at 
        this point.
        """
        new = LinearOperatorStruct.applyop( self, other )
        new.addBreakPoint( )
        return new
        

## curvelet transform in two dimensions
# @ingroup linop
class fdct2( LinearOperatorStruct ):
    """
    The fast discrete curvelet transform in two dimensions.
    """
    name = 'fdct2'
    __block_diagonal__ = True
    def __init__( self, inSpace, nbs, nba, ac, cpxIn=False, adj=False ):
        LinearOperatorStruct.__init__( self, inSpace, nba=nba, nbs=nbs, ac=ac, adj=adj, cpxIn = cpxIn)
    
    ## 
    # @depricated use slimpy_base.api.linearops.operator_functions.Norm
    def norm( self ):
        """
        depricated function
        overload our norm operator to use the sffdct2vects rsf function.
        """
        warnings.warn("please use SLIMpy.Norm function", DeprecationWarning , 2)
        return self.__norm_col__( ) 
    
    def __norm_col__(self):
        """
        A.__norm_col__() <-> Norm( A ) 
        """
        
        return clnorm( self )
    
    def __min_vel_const__(self, ang_weights ):
        """
        A.__min_vel_const__(ang_weights) <-> MinVelConst( A ) 
        """

        return clnorm( self, mode='zang', angconstr=ang_weights )
    
    
## @ingroup linop
class fdct( LinearOperatorStruct ):
    """
    The fast discrete curvelet transform in-core with PYCT (sffdct)
    """
    name = 'fdct'
    def __init__( self, inSpace, curveSpace=None, nbs=4, nba=8, ac=1, adj=False ):
        LinearOperatorStruct.__init__( self, inSpace, curveSpace=curveSpace, nbs=nbs, nba=nba, ac=ac, adj=adj)
        
        
