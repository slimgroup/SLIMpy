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

from slimpy_base.Core.User.linop.linear_operator import LinearOperator
from numpy import ndarray
from slimpy_base.User.AumentedMatrix.AugOperator import AugOperator
from slimpy_base.User.AumentedMatrix.AugVector import AugVector

explicit = lambda oper: isinstance(oper, ndarray)

## @todo 
#  @ingroup linop
class Kronecker( LinearOperator ):
    
    def __init__(self, OperA, OperB):
        self.OperA = OperA
        self.OperB = OperB
    
    ## apply operator to vector
    def applyop(self,other):
        X = other.view( AugOperator )
        
        if self.isadj:
            A = self.OperA.H
            B = self.OperB.H
        else:
            A = self.OperA
            B = self.OperB
            
        C = A * ( X * B.H )
        
        res = C.view( AugVector )
        return res 
