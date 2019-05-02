##@package new_smoothgradient_rsf_integration
# This is the second step in creating a linear operator. There are two substeps to this module.
#  - create a \ref slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter "sfConverter" 
#    subclass that defines how to use a SLIMpy operator with rsf commands.
#  - register the converter with the rsf plugin. 
# 
# @code
# from numpy import ceil
# from slimpy_base.api.Plugins.slim2rsf.sfCommandFactory import rsfCommandFactory
# from slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter import sfConverter
# 
# ########################################################################
# # Define how smoothgradientx behaves
# ########################################################################
# 
# # create a Converter class
# class smoothgradientX_Converter( sfConverter ):
#     \"""
#     This is a mapping instance that maps a SLIMpy command into an object that 
#     can be run.
#     There are three types of function this class should have.
#       - map
#       - trans 
#       - constr
#     Each of these functions can have an optional '_adj' at the end of the name 
#     if the operator's adjoint is different than the forward.
#     
#     \par map should change the arguments of the operator such that it can run as 
#     an rsf command line.
#     \par trans defines how this operator affects the domain of the input. 
#      this is also to calculate the range of the operator at initialization.
#     \par constr defines any run time error messages if the vector is not in the domain of 
#     the operator.
#       
#      
#     \"""
#     # always use classmethod or static method
#     @classmethod
#     def map( cls, source, command ):
#         \"""
#         map a SLIMpy command to a rsf command
#         \"""
#         # the RSF bin and 'sf' will be automaticaly prepended to smoothgradient executable
#         command = cls.default_function( command, "./Msmoothgradient.py" ) 
#         #change all python True/False objects to 'y'/'n' strings
#         command = cls.truefalseHelper( command )
#         #map the adj flage to inv
#         command = cls.keywordmap( command, {'adj':'inv'} )
#         #always must return a CommandPack instance
#         return cls.pack( command )
#     
# 
#     @classmethod
#     def trans( cls, command, space, *spaces ):
#         'define how this operator affect the space'
#         n1 = spaces[0]['n1']
#         space['n1_smoothgradient']= n1
#         space["n1"] = int( ceil( n1/2. )+1 )
#         space['data_type']='float' 
#         return space
#     
#     @classmethod
#     def trans_adj( cls, command, space, *spaces ):
#         \"""
#         trans_adj will automatically be called in the case
#         where the command has an adj keyword that is true
#         \"""
#         n1 = spaces[0]['n1_smoothgradient']
#         space['data_type']='float'
#         space['n1']= n1
#         return space
#     
#     @classmethod
#     def constr( cls, command, space ):
#         'make sure the data on the forward command is float'
#         cls.match( space, data_type='float' )
#         
#     
#     @classmethod
#     def constr_adj( cls, command, space ):
#         'make sure the data on the adjoint command is float'
#         cls.match( space, data_type='float' )
# 
# 
# #===============================================================================
# # Add it to the list of existing rsf commands by
# # by registering the converter with the rsf plugin. 
# #===============================================================================
# 
# factory = rsfCommandFactory()
# # add the converter class to the factory
# # now converter will be invoked when 
# # a linear operator with the 'name' attribute
# # of smoothgradient
# factory['smoothgradientX'] = smoothgradientX_Converter
# @endcode

from numpy import ceil
from slimpy_base.api.Plugins.slim2rsf.sfCommandFactory import rsfCommandFactory
from slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter import sfConverter

########################################################################
# Define how smoothgradientx behaves
########################################################################

# create a Converter class
class smoothgradientX_Converter( sfConverter ):
    """
    This is a mapping instance that maps a SLIMpy command into an object that 
    can be run.
    There are three types of function this class should have.
      - map
      - trans 
      - constr
    Each of these functions can have an optional '_adj' at the end of the name 
    if the operator's adjoint is different than the forward.
    
    \par map should change the arguments of the operator such that it can run as 
    an rsf command line.
    \par trans defines how this operator affects the domain of the input. 
     this is also to calculate the range of the operator at initialization.
    \par constr defines any run time error messages if the vector is not in the domain of 
    the operator.
      
     
    """
    # alwas use classmethod or static method
    @classmethod
    def map( cls, source, command ):
        """
        map a SLIMpy command to a rsf command
        """
        # the RSF bin and 'sf' will be automaticaly prepended to smoothgradient executable
        command = cls.default_function( command, "./Msmoothgradient.py" ) 
        #change all python True/False objects to 'y'/'n' strings
        command = cls.truefalseHelper( command )
        #map the adj flage to inv
        command = cls.keywordmap( command, {'adj':'inv'} )
        #alwas must return a CommandPack instance
        return cls.pack( command )
    

    @classmethod
    def trans( cls, command, space, *spaces ):
        'define how this operator affect the space'
        n1 = spaces[0]['n1']
        space['n1_smoothgradient']= n1
        space["n1"] = int( ceil( n1/2. )+1 )
        space['data_type']='float' 
        return space
    
    @classmethod
    def trans_adj( cls, command, space, *spaces ):
        """
        trans_adj will automatically be called in the case
        where the command has an adj keyword that is true
        """
        n1 = spaces[0]['n1_smoothgradient']
        space['data_type']='float'
        space['n1']= n1
        return space
    
    @classmethod
    def constr( cls, command, space ):
        'make sure the data on the forward command is float'
        cls.match( space, data_type='float' )
        
    
    @classmethod
    def constr_adj( cls, command, space ):
        'make sure the data on the adjoint command is float'
        cls.match( space, data_type='float' )



#===============================================================================
# Add it to the list of existing rsf commands by
# by registering the converter with the rsf plugin. 
#===============================================================================

factory = rsfCommandFactory()
# add the converter class to the factory
# now converter will be invoked when 
# a linear operator with the 'name' attribute
# of smoothgradient
factory['smoothgradientX'] = smoothgradientX_Converter
