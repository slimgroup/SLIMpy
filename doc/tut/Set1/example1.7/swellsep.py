"""
@page es1step7 Step 7
"""

from SLIMpy.linear_operators import *
from SLIMpy import vector
from slimpy_contrib.ana.problems.l1_minimization_problem import l1_min


#Global Operators
PC = None
W = None

def transform_callback( target, source, env, space ):
    """
    create a transfrom
    [[ PC ],
     [ W  ]]
    Where PC is the weighted cosine transfrom and W is 
    the wavelt transfrom. 
    """
    global PC, W
    
    weight = vector( source[1] )
    
    C = Cosine( space )
    P = DiagonalWeight( space, weight )
    
    PC = CompoundOperator( [P,C] )
    W = dwt( space )
     
    AH = AugOperator( [[PC],
                      [W]] )
    
    D = DiagonalWeight( AH.domain(), .49 )
    
    AD = CompoundOperator( [AH,D] )
    
    A = AD.H
    return A

def recovery_callback( target, source, env, space ):
    """
    do the weighted cosine transfrom and wavelet transform
    as a block diagonal so they are not summed together. 
    """
    AH = AugOperator( [[PC.H, 0  ],
                      [ 0,   W.H ]] )
    
    D = DiagonalWeight( AH.range(), .49 )
    DA = CompoundOperator( [D,AH] )
    return DA

def result_callback( target, source, env, result ):
    """
    sets the first and second targets estimated swell 
    noise and and the signal respectivley 
    """
    result.flat[0].setName( str(target[0] ) ) 
    result.flat[1].setName( str(target[1] ) )

## @var dict l1swell_sep
# this is the l1swell_sep problem. It is a python dictionary copied from the 
# l1_min problem with the added transform_callback recovery_callback and result_callback.
# Also has extra default solver parameters.
l1swell_sep = l1_min.copy()
l1swell_sep['doc'] = l1swell_sep['doc'].copy()

l1swell_sep['transform_callback'] = transform_callback
l1swell_sep['inv_callback'] = recovery_callback
l1swell_sep['result_callback'] = result_callback

l1swell_sep['nouter'] = 10
l1swell_sep['nouter'] = 10
l1swell_sep['lmax'] = 0.001 
l1swell_sep['lmin'] = 0.99



