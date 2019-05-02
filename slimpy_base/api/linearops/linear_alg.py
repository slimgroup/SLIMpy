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

from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType
from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
from slimpy_base.Core.User.linop.linear_operator import CompoundOperator


## Half Order Deriviative
#  @ingroup linop
class halfderiv( LinearOperatorStruct ):
    """
    HD = halfderiv( dom, inv=True ) 
    Half Order Deriviative
    """
    name = "halfderiv"
    def __init__(self,inSpace,inv=True,**kparams):
        """
        Initialize the operator.
        """
        LinearOperatorStruct.__init__(self,inSpace,inv=inv,**kparams)

## Full Derivative operator
# @ingroup linop
@LinearOperatorType
def deriv(inSpace):
    """
    D = deriv( dom )
    A Full Derivative
    """
    hd = halfderiv(inSpace)
    
    return CompoundOperator( [hd, hd] )

## gradient 
# @return compound operator of ??? 
# @ingroup linop
@LinearOperatorType
def grad(inSpace):
    """
    G = grad( dom )
    Grad with respect to hd/d compounding
    """
    d = deriv(inSpace)
    
    return CompoundOperator( [d] )

## @ingroup linop
@LinearOperatorType
def curl(inSpace, sym=True, opt=False ):
    """
    C = curl( inSpace ) 
    Curl with respect to hd/d compounding
    """
    d = deriv(inSpace)
    
    return CompoundOperator( [d] )
