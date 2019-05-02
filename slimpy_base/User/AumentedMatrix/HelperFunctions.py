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

from slimpy_base.User.AumentedMatrix.AugOperator import AugOperator
from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType
from itertools import izip
from numpy import diag

## create a block diagonal operator
# @param A linear operator or a list of linear operators 
# @param length if A is not a list then  Diag will retrurn a operator of size length*length
# @return Diagonal slimpy_base.User.AumentedMatrix.AugOperator.AugOperator instance 
#  @ingroup linop
@LinearOperatorType
def Diag( A, length=0 ):
    """
    D = Diag( A [, length] )
    create a diagonal operator from A if length is non zero a must be a list, 
    and will return a len(A) x len(A) matrix otherwize will return a length x 
    length size operator with copies of A along the diagonal.   
    """
        
    if length:
        A_list = [A]*length
    else:
        A_list = A
        
    return diag( A_list ).view( AugOperator )

## create a diagonal Operator from a class and a meta space
## @ingroup linop
@LinearOperatorType
def From_sapce( cls , inspace, *params, **kparams):
    """
    D = From_sapce( oper_class, meta_space, ... )
    create a diagonal Operator from meta (in/out) spaces
    """    
#    msg1 = "'%(cls)s' is not block_diagonal. Got 'Metaspace' as inspace" %vars()
#    msg2 = "inspace and outspace must both be MetaSpace instances"
#    msg3 = "inspace and outspace must both be the same size"
    
#    assert hasattr(cls, "__block_diagonal__") and getattr(cls, "__block_diagonal__") , msg1
#    assert isinstance(inspace, MetaSpace) and isinstance(outspace, MetaSpace) , msg2
#    assert inspace.size == outspace.size, msg3

    pkw_obj = inspace.__pk_expannder__( *params, **kparams )
    zipper = izip( inspace.ravel(), pkw_obj)
    
    oper_list = [ cls( ispc,  *p, **wk) for ispc,(p,wk) in zipper ]
    
    OP = Diag( oper_list )
    OP.meta = inspace.meta
    return OP 

