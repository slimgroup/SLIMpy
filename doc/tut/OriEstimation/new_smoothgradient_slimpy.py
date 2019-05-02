##@package new_smoothgradient_slimpy
# This is a very straight forward linear operator which computes the derivatives of the input function with a special
# 3x3 filter which is more resistant to noise than the usual Sobel filter. smoothgradientX is a subclass of LinearOperatorStruct.
# 
# @code
# from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
# import os, sys, re, string, glob, shutil 
# 
# #===============================================================================
# # Linear operator class itself 
# #===============================================================================
# class smoothgradientX( LinearOperatorStruct ):
#     \"""  
#     Calculates a relatively robust gradient operator on its input
#     Note how smoothgradientX inherits all of its linear operator functionality 
#     from LinearOperatorStruct. after the initialization is done of
#     smoothgradientX SLIMpy will do the rest of the work.
#     \"""
#     name = "smoothgradientX"
#     
#     def __init__( self, domain ):
#         
#         kparams = dict( adj=False )
# 
#         LinearOperatorStruct.__init__( self, domain, **kparams )
# @endcode

from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
import os, sys, re, string, glob, shutil 

#===============================================================================
# Linear operator class itself 
#===============================================================================
class smoothgradientX( LinearOperatorStruct ):
    """  
    Calculates a relatively robust gradient operator on its input
    Note how smoothgradientX inherits all of its linear operator functionality 
    from LinearOperatorStruct. after the initialization is done of
    smoothgradientX SLIMpy will do the rest of the work.
    """
    name = "smoothgradientX"
    
    def __init__( self, domain ):
        
        kparams = dict( adj=False )

        LinearOperatorStruct.__init__( self, domain, **kparams )
