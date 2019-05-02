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


from slimpy_base.Core.Interface.node import Source
from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct


## Matrix-vector multiplication 
# @note The adj flag gives the transpose for RSF
# @ingroup linop
class MatMult(LinearOperatorStruct):
    """
    M = MatMult(vecSpace, matrix)
    
    Matrix-vector multiplication. n1 of input must match n1 of matrix.
    In other words, n1 corresponds to row index and n2 corresponds to column index when RSF file is 2D.
    Paradoxiolly, A vector RSF file with values in the n1 direction is a column vector.
    
    NOTE: The adj flag gives the transpose
    
    Matrix is a file name of an rsf file of the matrix we wish to apply.
    
    Designed to work with SLIMpy2
    
    Written by Tim Lin
    July 2007
    """
    
    name = "matrixmult"
    ## Constructor
    # @param space domain of operator 
    # @param matrix vector object to look at as a matrix 
    def __init__(self, space, matrix, adj=False):
        
        from slimpy_base.Core.User.Structures.serial_vector import Vector
        if isinstance(matrix, str):
            from slimpy_base import vector
            matrix = vector( matrix )
        elif not isinstance(matrix, Vector):
            raise TypeError( "argument 'matrix' must be a 'Vector' or a 'str' instance got '%s'" %type(matrix) )
        
        self.inSpace = space
        kparams = dict(mat=Source(matrix.container), adj=adj)
        
        LinearOperatorStruct.__init__( self, self.inSpace, **kparams )

    
