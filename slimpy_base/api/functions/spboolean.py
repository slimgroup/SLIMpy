## @package scalar_functions Boolean vector functions
"""
Boolean vector functions
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

from slimpy_base.api.functions import slimpy_function_register
from slimpy_base.Core.Interface.Structure import Structure

## Test if two vectors are equal per element
#  @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def equal( vec1 , vec2 , eps=0 ):
    """
    equal( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are equal within eps precision  
    """
    
    cmd = "eq"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if two vectors are not equal per element
#  @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def not_equal( vec1 , vec2 , eps=0 ):
    """
    not_equal( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are not equal within eps precision  
    """
    
    cmd = "ne"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of vec1 are less than vec2
# @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def less_than( vec1 , vec2 , eps=0 ):
    """
    less_than( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are less than vec2
    """
    cmd = "lt"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of vec1 are less than or equal to vec2
# @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def less_than_eq( vec1 , vec2 , eps=0 ):
    """
    less_than_eq( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are less than or equal to vec2  
    
    """
    cmd = "le"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of vec1 are greater than vec2
# @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def greater_than( vec1 , vec2 , eps=0 ):
    """
    greater_than( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are greater than vec2 
    
    """
    cmd = "gt"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of vec1 are greater than or equal to vec2
# @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def greater_than_eq( vec1 , vec2 , eps=0 ):
    """
    greater_than_eq( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if two vectors elemnts are greater than or equal to vec2 
    """
    cmd = "ge"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of either vec1 or vec2 are non-zero
#  @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def or_( vec1 , vec2 , eps=0 ):
    """
    or_( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if elements of either vec1 or vec2 are non-zero 
    """
    cmd = "or_"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )

## Test if elements of both vec1 or vec2 are non-zero
#  @ingroup functions
#  @param vec1 a vector        
#  @param vec2 a vector        
#  @param eps a number
#  @pre vec1 and vec2 are the same length
#  @return: a vector of integers the same length as input.
@slimpy_function_register
def and_( vec1 , vec2 , eps=0 ):
    """
    and_( vec1 , vec2 , eps=0 ) -> vec3
    
    Test if elements of either vec1 or vec2 are non-zero 
    """
    cmd = "and_"
    struct = Structure( )
    right = struct.source_or_num( vec2 )
    return struct.generateNew( vec1, cmd, eps=eps, right=right )
