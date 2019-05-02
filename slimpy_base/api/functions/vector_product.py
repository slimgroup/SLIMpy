## @package vector_product functions for inner and outer products of vectors 

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


from slimpy_base.api.linearops.MatMult import MatMult
from slimpy_base.api.functions.scalar_functions import real_if_close

## inner product of two vectors
# @ingroup functions
#  @param vec1 a vector
#  @param vec2 a vector
#  @pre vec1 and vec2 are the same length
#  @return: a scalar
def inner_product( vec1, vec2 ):
    """
    inner_product( vec1, vec2 ) -> scalar
    take the inner product of two vectors  
    """
    l1 = len( vec1.space )
    l2 = len( vec2.space )
    
    tmp_vec1 = vec1.reshape( l1, 1 )
    tmp_vec2 = vec2.reshape( l2, 1 )
    
    mat = MatMult(tmp_vec1.space, tmp_vec2)
    
    inner_prod = mat * tmp_vec1
    
#    print 'len',len( inner_prod.space )
    return real_if_close( inner_prod[0] )

## Outer product of two vectors
# @ingroup functions
#  @param vec1 a vector
#  @param vec2 a vector
#  @pre vec1 and vec2 are the same length
#  @warning not implemented
#  @return: a scalar
def outer_product(vec1,vec2):
    """
    inner_product( vec1, vec2 ) -> scalar
    take the inner product of two vectors  
    """
    raise NotImplementedError()
