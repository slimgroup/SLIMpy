"""
A set of geneal out of core functions
to work on Vectors.
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


from slimpy_base.Core.Interface.Structure import Structure
from slimpy_base.Core.Interface.node import Source

from slimpy_base.api.functions import slimpy_function_register
from numpy import array, any
from math import floor
from slimpy_base.Core.User.linop.linear_operator import Identity
from slimpy_base.api.linearops.transforms import DiagonalWeight


## create a complex vector from real and imaginary parts
#  @ingroup functions
#  @param real a  vector that contains real numers        
#  @param imag a vector that contains real numers        
#  @return: a complex vector that is composed of real numbers for param real
#     and imaginary numbers from param imag
@slimpy_function_register
def cmplx( real, imag ):
    """
    cmplx( real, imag ) -> complex vector
    create a complex vector from real and imaginary parts 
    """
    struct = Structure( )
    
    cmnd = "cmplx"
    return struct.generateNew( real, cmnd, Source, Source( imag.container ) )



## Concatenate datasets
# @ingroup functions
#  @param catlist a list that contains the vectors to be concatonated        
#  @param axis Axis being merged        
#  @return: a vector
@slimpy_function_register
def cat( catlist , axis ):
    """
    Concatenate datasets catlist in the axis dinention.
    cat( axis, catlist ) -> vector
    """
    struct = Structure( )
    
    cat_array = array(catlist)
    if not cat_array.shape: 
        return catlist
    elif cat_array.size == 1:
        return catlist.item()
    else:
        catlist = cat_array.ravel().tolist()
        cat1,catlist = catlist[0],catlist[1:]         
        sourcelist = [ Source(catitem.container) for catitem in catlist ]
        cmnd = "cat"
        return struct.generateNew( cat1, cmnd, *sourcelist, **{'axis':axis} )
    

## norm of coloums of fdct2 
# @ingroup functions
#  @param A the fdct2 linear operator        
#  @param mode todo        
#  @param angconstr todo        
#  @return: a diagonal weight linear operator
@slimpy_function_register
def clnorm( A ,mode="norm" , angconstr=[0,0] ):
    """
    clnorm( A ,mode="norm" , angconstr=[0,0] ) -> DiagonalWeight
    retruns a diagonal weight operator with domain and range in the vector space of
    the domain of A 
    The weight coresponds to the norms of the coloums of A
    """
    struct = Structure( )
    cmnd =  'fdct2vects'
    
    if A.isadj:
        cInSpace = A.range( )
    else:
        cInSpace = A.domain( )
#        A[]

    angconstr
    angperwed = 360./ A.kparams['nba']
    
    wedgconstr=[0,0]
    for i in range(2):
        wedgconstr[i] = floor((90-angconstr[i])/angperwed)
    
    
    if mode == "zang" and not any(wedgconstr) :
        return Identity( A.range() )
        
    
    command = struct.generate_command( cmnd ,
                                     cInSpace=cInSpace,
                                     mode=mode,
                                     wedgconstr=wedgconstr,
                                     nbs= A.kparams['nbs'], 
                                     nba= A.kparams['nba'], 
                                     ac = A.kparams['ac'] )
    
    # empty data container 
    data_container = cInSpace.makeContaner( cmnd )
    converter = data_container.get_converter( command )
    commpack = converter.convert( None, command )
    
    commpack.target = data_container
    commpack.source = None
    
    struct.env['graphmgr'].graphAppend( commpack )
    
    from slimpy_base.Core.User.Structures.serial_vector import Vector
    wvec = Vector(data_container)
    return DiagonalWeight(wvec.space, wvec) 


