"""
Linear Operators relating to fft
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


from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
from slimpy_base.Core.User.linop.linear_operator import CompoundOperator
from slimpy_base.Core.User.linop.linear_operator import LinearOperatorType



## Fourier transfrorm on the first axis
# @ingroup linop
class fft1( LinearOperatorStruct ):
    """
    F = fft1( domain, sym=True, opt=False, adj=False ) 
    Fourier transfrorm on the first axis
    """
    name = "fft1"
    __block_diagonal__ = True
    def __init__( self, inSpace, sym=True, opt=False, adj=False ):
        
        kparams = dict( sym=sym, opt=opt, adj=adj )

        LinearOperatorStruct.__init__( self, inSpace, **kparams )

## Fourier Fourier transform on any axis
# @ingroup linop
class fft( LinearOperatorStruct ):
    """
    F = fft( inSpace, sym=True, opt=False, pad=1, axis=2, adj=False )
    Fourier transform on any axis
    """
    name = "fft"
    __block_diagonal__ = True
    
    ## Constructor 
    # @param inSpace a VectorSpace
    # @param sym apply symmetric scaling to make the FFT operator Hermitian
    # @param opt determine optimal size for efficiency
    # @param pad  padding factor
    # @param axis Axis to transform
    # @param adj create inverse transform
    def __init__( self, inSpace, sym=True, opt=False, pad=1, axis=2, adj=False ):
        
        kparams = dict( sym=sym, opt=opt, pad=pad, axis=axis, adj=adj )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )

## fourier transform in two dimensions
# @ingroup linop
# @param  sym  apply symmetric scaling to make the FFT operator Hermitian
# @param  opt determine optimal size for efficiency
# @return Compound operator of fft1 and fft with axis=2
@LinearOperatorType
def fft2( inSpace, sym=True, opt=False ):
    """
    F = fft2( dom, sym=True, opt=False ) 
    The fourier transform in two dimensions
    """
    f1 = fft1( inSpace, sym=sym, opt=opt )
    f2 = fft( f1.range(), sym=sym, opt=opt, axis=2 )
    
    return CompoundOperator( [f2, f1] )

## fourier transform in three dimensions
# @ingroup linop
# @param  sym  apply symmetric scaling to make the FFT operator Hermitian
# @param  opt determine optimal size for efficiency
# @return Compound operator of fft1, fft with axis=2 and fft with axis=3
@LinearOperatorType
def fft3( inSpace, sym=True, opt=False ):
    """
    F = fft3( dom, sym=True, opt=False ) 
    The fourier transform in three dimensions
    """
    f1 = fft1( inSpace, sym=sym, opt=opt )
    f2 = fft( f1.outSpace, sym=sym, opt=opt, axis=2 )
    f3 = fft( f2.outSpace, sym=sym, opt=opt, axis=3 )
    
    return CompoundOperator( [f3, f2, f1] )
