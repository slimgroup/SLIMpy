"""
Sub classes of LinearOperator that use Structures as base classes
aswell
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
from slimpy_base.Core.Interface.AbstractDataInterface import ADI 
from slimpy_base.Core.User.linop.linear_operator import LinearOperator


class linearop_r( Structure, LinearOperator ):
    """
    The base linear operator object should not be called by itself.
    """
    name = "linearop_r"
    def __init__( self, inspace, *params, **kparams ):
        # init Structure not necissary but to conserve consistancy
        Structure.__init__( self )
        outspace = inspace.testCommand( self.name, *params, **kparams )
        
        LinearOperator.__init__( self, inspace, outspace, *params, **kparams )

    
    def applyop( self, other ):
#        assert other.space in self.domain() 
        return self.generateNew( other, self.name , *self.params, **self.kparams )
    

class linearop_c( LinearOperator, ADI ):
    """
    The base linear operator object should not be called by itself.
    """
    name = "linearop_c"
    def __init__( self, data, inSpace, outSpace, *params, **kparams ):
        
        ADI.__init__( self, data )
        LinearOperator.__init__( self, inSpace, outSpace, *params, **kparams )
    
    def applyop( self, other ):
        """
        apply
        """
        return other.generateNew( self.name, *self.params, **self.kparams )

    def __mul__( self, other ):
        return LinearOperator.__mul__( self, other )
    
    
