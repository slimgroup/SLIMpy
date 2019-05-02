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
from slimpy_base.Core.User.Structures.VectorSpace import VectorAddition

## representation of addition or subtraction of two operators
# @ingroup linop
class ArithmaticOperator( LinearOperator ):
    """
    ArithmaticOperator( '-', I, T ) * x <-> (I - T) *x
    """
    
    ## Constructor
    # @param arithop one of the strings '+' or '-' 
    # @param oper1 a linear operator 
    # @param oper2 a linear operator 
    def __init__(self, arithop, oper1, oper2):
        self.oper1 = oper1
        self.oper2 = oper2
        self.arithop = arithop
        
        domain = VectorAddition( [self.oper1.domain() ,self.oper2.domain()] )
        range = VectorAddition(  [self.oper1.range() ,self.oper2.range()] )
        LinearOperator.__init__( self, domain, range )

    def __str__(self):
        return "( %(oper1)s %(arithop)s %(oper2)s )" %self.__dict__
    
    ## apply operator to vector
    def applyop(self,other):
        """
        A.applyop(other) -> vector
        """
        res1 = self.oper1 * other
        res2 = self.oper2 * other
        
        if self.arithop == '+':
            res = res1 + res2
            
        elif self.arithop == '-':
            res = res1 - res2
            
        return res
        
