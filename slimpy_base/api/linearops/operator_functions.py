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
from slimpy_base.Core.User.linop.linear_operator import Identity
from slimpy_base.Core.User.linop.linear_operator import CompoundOperator


## test if object implements LinearOperatorType 
# @ingroup linop 
@LinearOperatorType
def is_linear_op( oper ):
    '''
    is_linear_op( oper ) -> bool
    returns true if type( type(oper) ) == LinearOperatorType
    '''
    bll = type( type(oper) ) == LinearOperatorType
    return bll


## normalizes the rows or coloums of an operator
# @ingroup linop 
@LinearOperatorType
def Norm( oper, col=True, default=None ):
    """
    Norm( oper, col=True, error=False ) -> Weights
    normalizes the operator
    if error is True then the linear operator must have the appropriate
    __norm_col__ or 
    """
    if not is_linear_op(oper):
        raise TypeError( "first argument of norm must be a linear operator" )
    # 
    if oper.isadj:
        coll = not col
    else:
        coll = col
#    coll = oper.isadj and not col or col
    
    if coll:
        name = "__norm_col__"
    else:
        name = "__norm_row__"
    
    
    if not hasattr(oper , name):
        raise AttributeError( "linear operator %(oper)s "
                              "has no method %(name)s " %vars() )
        
    normmethod = getattr(oper, name)
    weight = normmethod( )
    
    if weight == NotImplemented:
        if default is None:
            raise Exception( "operator %s can not be normalized" %(oper) )
        elif default == 'Identity':
            if col:
                space = oper.range( )
            else:
                space = oper.domain( )
                
            return Identity( space )
        elif is_linear_op(default):
            
            return default
        else:
            raise TypeError( 'argument "default" must be None, '
                             '"Identity" or a LinearOperatorType, got "%s"' %type(default) )
    else:
        return weight 
    
## normalizes the rows or coloums of an operator
# @ingroup linop 
@LinearOperatorType
def Normalize( oper , col=True, default=None ):
    """
    Normalize( oper , col=True, error=False )
    
    """
    weights = Norm( oper, col=col, default=default )
    if col:
        oper_list = [ weights ,oper]
    else:
        oper_list = [ oper, weights] 
    
    return CompoundOperator(  oper_list )
    
    
## @ingroup linop 
@LinearOperatorType
def MinVelConst( oper , ang_weights, default=None ):
    """
    weight = MinVelConst(oper, ang_weights, default=None)
    returns a weighting operator for the min 
    """
    assert is_linear_op( oper )
    
    name = "__min_vel_const__"
    
    if not hasattr(oper, name):
        if default is None:
            raise AttributeError( "oper does not have attribute '__min_vel_const__' " )
        elif default == "Identity":
            space = oper.domain( )
            return Identity(space)
        else:
            return default
    
    min_vel_const = getattr(oper, name)
    
    const = min_vel_const( ang_weights )
    
    if const == NotImplemented:
        if default is None:
            raise AttributeError( "oper attribute '__min_vel_const__' returned 'NotImplemented' " )
        elif default == "Identity":
            space = oper.domain( )
        else:
            return default 
    else:
        return const


