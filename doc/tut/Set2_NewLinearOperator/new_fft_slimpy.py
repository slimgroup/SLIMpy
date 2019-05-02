"""
@package new_fft_slimpy
This is a very straight forward linear operator. fft1X is a subclass of LinearOperatorStruct.

"""
from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct

#===============================================================================
# Linear operator class itself 
#===============================================================================
class fft1X( LinearOperatorStruct ):
    """
    Fourier transfrorm on the first axis.
    Note how fft1X inherits all of its linar operator functionality 
    from LinearOperatorStruct. after the initialization is done of
    fft1X SLIMpy will do the rest of the work.
    """
    name = "fftX"
    
    def __init__( self, domain, sym=True, opt=False ):
        
        kparams = dict( sym=sym, opt=opt, adj=False )

        LinearOperatorStruct.__init__( self, domain, **kparams )
