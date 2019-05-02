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

from slimpy_base.utils.Interface import InterfaceType

from inspect import isroutine
from inspect import isdatadescriptor

class VectorType( InterfaceType ):
    
    interface_methods = dict(
#                            is_transp = isdatadescriptor,
                            space = isdatadescriptor,
                            setName =isroutine,
                            sort=isroutine, 
                            orderstat=isroutine,

#                            __radd__,
#                            __neg__  ,
#                            __sub__ ,  
#                            __rsub__ ,  
#                            __div__ ,  
#                            __rdiv__ ,  
#                            __mul__ ,  
#                            __rmul__ ,  
#                            __pow__ ,  
#                            __abs__  
#                            __or__, 
#                            __and__,
#                            __lt__,
#                            __gt__,
#                            __le__,
#                            __ge__,
#                            __eq__,
#                            __ne__,
#                            rms  
#                            max=isroutine,
#                            min  =isroutine,
#                            mean  =isroutine,
##                            var  
##                            sdt  
#                            norm=isroutine,
#                            real=isroutine, 
#                            imag=isroutine,
#                            conj=isroutine,
#                            grad=isroutine,
#                            thr=isroutine, 
#                            sort=isroutine, 
#                            orderstat=isroutine,
#                            T=isdatadescriptor, 
                            )


is_vector = lambda obj: type(type( obj ) ) == VectorType

