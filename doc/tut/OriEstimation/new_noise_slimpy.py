##@package new_noise_slimpy
# This is a very straight forward linear operator which adds Gaussian noise to an image. 
# noiseX is a subclass of LinearOperatorStruct.
# @code
# from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
# 
# #===============================================================================
# # Linear operator class itself 
# #===============================================================================
# class noiseX( LinearOperatorStruct ):
#     \"""
#     Adds Gaussian Noise to image
#     Note how noiseX inherits all of its linear operator functionality 
#     from LinearOperatorStruct. after the initialization is done of
#     noiseX SLIMpy will do the rest of the work.
#     \"""
#     name = "noise"
#     
#     def __init__( self, domain):
#         
#         kparams = dict( adj=False )
# 
#         LinearOperatorStruct.__init__( self, domain, **kparams )
# @endcode

from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct

#===============================================================================
# Linear operator class itself 
#===============================================================================
class noiseX( LinearOperatorStruct ):
    """
    Adds Gaussian Noise to image
    Note how noiseX inherits all of its linear operator functionality 
    from LinearOperatorStruct. after the initialization is done of
    noiseX SLIMpy will do the rest of the work.
    """
    name = "noise"
    
    def __init__( self, domain, sigma = 0.08):
        
        kparams = dict( sigma = 0.08, adj=False )

        LinearOperatorStruct.__init__( self, domain, **kparams )
