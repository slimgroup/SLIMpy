## functions that work on SLIMpy scalars
# @package slimpy_base.api.functions.scalar_functions 
"""
general scalar functions that work on SLIMpy scalar objects or 
python numbers
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

from slimpy_base.Core.User.Structures.Scalar import *
from numpy import real_if_close as numpy_real_if_close

from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.utils.RegisterType import register_slimpy_func

## The SLIMpy global environment
__env__ = InstanceManager( )

## for * import 
__all__ = [ "scalar_max",
           "scalar_min",
           "real_if_close",
           "scalar_value",
           "scalar_mean" ]

def generate_new_scalar( one, other, func):
    """
    generate_new_scalar( one, other, func) -> scalar
    """
    scalar = Scalar( )
    trg_scal = Target( scalar )
    src_self = Source( one )
    
    other_obj = one._num_src( other )
    
#        new_func = scalar_helper(func,func_name=func_name)
    tag = str(func)
    command = general_command( tag, None, src_self,other_obj,trg_scal )
    command.func = func
    
    if one.env['slimvars']['keep_tb_info']:
        stack = traceback.extract_stack( )
        st_list  = traceback.format_list( stack[:-3] )
        command.tb_info = "".join(st_list)
        
    compack = CommandPack([command], None, None)
    
    __env__['graphmgr'].graphAppend( compack )

    return scalar

def scalar_operation( one, other, func ):
    
    if has_num(one) and has_num(other):
        return func( get_num(one), get_num(other) )
        
    if is_number(other) or other is None:
        return one.gen_new_scal(other, func )
    else:
        return NotImplemented

class scalar_proxies( object ):
    '''
    class to help scalar 
    used to prevent error on pickle function
    used instead of defineing functions in the module namespace
    '''
    def __init__( self, value ):
        self.method_name = value
        
    def __call__(self , src_self,other_obj,trg_scal=None ):
            
        method = getattr(self, self.method_name)
        
        val = method( get_num(src_self), get_num(other_obj) )
        if trg_scal is None:
            return val
        else:
            trg_scal.set(val)
            return

    def max( self, one, other ):
        return max( one, other )

    def min( self, one, other ):
        return min( one, other )

    def real_if_close(self,one,other):
        return numpy_real_if_close( one ).item( )

def _scalar_max( scal1, scal2 ):

    return scalar_operation(  scal1, scal2, scalar_proxies("max") )

## return max element
# @ingroup functions
#  @param sequence a sequence of scalars
#  @return: a scalar object
@register_slimpy_func
def scalar_max( *sequence ):
    '''
    scalar_max(sequence) -> value
    scalar_max(a, b, c, ...) -> value
    
    With a single sequence argument, return its largest item.
    With two or more arguments, return the largest argument.
    '''

    assert len(sequence)
    if len(sequence) == 1:
        sequence = sequence[0] 
    
    max2 = lambda scal1, scal2: _scalar_max(scal1, scal2)
    return reduce( max2 , sequence)
    

def _scalar_min( scal1, scal2 ):

    return scalar_operation(  scal1, scal2, scalar_proxies("min") )

## return min element
# @ingroup functions
#  @param sequence a sequence of scalars
#  @return: a scalar object
@register_slimpy_func
def scalar_min( *sequence ):
    '''
    scalar_min(sequence) -> value
    scalar_min(a, b, c, ...) -> value
    
    With a single sequence argument, return its smallest item.
    With two or more arguments, return the smallest argument.
    '''

    assert len(sequence)
    if len(sequence) == 1:
        sequence = sequence[0] 
    
    min2 = lambda scal1, scal2: _scalar_min(scal1, scal2)
    return reduce( min2 , sequence)

## returns a real valued scalar if imaginary part of scal is close to 0
#  @ingroup functions
#  @param scal a saclar object
#  @return: a scalar object
@register_slimpy_func
def real_if_close( scal ):
    """
    returns a real valued scalar if imaginary part of scal is close to 0 
     real_if_close( scal ) -> value  
    """
    return scalar_operation(  scal, None, scalar_proxies("real_if_close") )

## mean value of a sequence of scalars
#  @ingroup functions
#  @param sequence a sequence of numbers
#  @return: a scalar object
@register_slimpy_func
def scalar_mean( sequence ):
    """
    scalar_mean( sequence ) -> value
    returns the mean value of sequence
    """
    length = len( sequence )
    
    ssum = sum( sequence ) / length
    
    return ssum

# retuns a python number from a scalar object
#  @ingroup functions
#  @param scal a scalar object or a python number
#  @post forces a build of the AST if scal is a sclar object
#  @return: a python number
@register_slimpy_func
def scalar_value( scal ):
    """
    retuns a number if scal is either a number of a SLIMpy scalar object
    """
    if is_scalar_obj( scal ):
        return scal.item()
    else:
        return scal 
    
    
    
