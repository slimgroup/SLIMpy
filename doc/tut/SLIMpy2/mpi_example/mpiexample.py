__author__ = "Sean Ross-Ross"
__version__ = "Simple mpi example v(1.0)"

"""
simple example of how to create a vector and run 
commands
"""
from slimpy_base import Space, Execute,vector

from slimpy_base.setup import *

from slimpy_base.utils.slim_decorators import depends_on  
from pdb import set_trace




defaults = { 'thr':0.1 }


@depends_on('thr')
def PerformSimleOpBldr( target, source, env ):
    'create a 10 by 10 image of zeros and add 3 to it'
    
    # parse a dictionary into SLIMpy global variables
    env = parse_env( env ,defaults)
    
    #Setting the defaults 
    vec = vector( source[0] )
    
    P = env['precondition_callback']( vec.space )
    C = env['transform_callback']( P.range() )
    
    
    augvec = P*vec
    
    coeffs = C * augvec
    
    tmp3 = coeffs.thr( env['thr'] )
    
    augres = C.adj() * tmp3
    
    result = P.adj() *  augres
    
    result.setName( target[0] )
    
    Execute()
    

    

# Add integration with scons 
__all__ = ['PerformSimleOp']

# add Simple function to SCons environment
from slimproj_core.builders.CreateBuilders import add_to_slim_env

PerformSimleOp = add_to_slim_env("PerformSimleOp", PerformSimleOpBldr )

