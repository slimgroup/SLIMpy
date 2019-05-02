"""
simple example of how to create a vector and run 
commands
"""
from slimpy_base.utils.slim_decorators import depends_on

usage = "python simple.py [options]"

from slimpy_base import Execute, vector, fft1,parse_env, env
from slimpy_base.setup import *
from slimpy_base import Scatter

@depends_on( 'blocksize', 'numblocks' )
def scatter_bldr(target,source,env):
    
    parse_env( env )
    
    blocksize = env.get('blocksize',None)
    numblocks = env.get('numblocks',None)
    assert blocksize is not None or numblocks is not None, "must set blocksize or numblocks"
    x = vector( source[0] )
    
    S = Scatter( x.space, blocksize=blocksize, numblocks=numblocks )

    r = S *x
    
    r.thr(0.02) * 2
    
    gathered = S.adj() * r
    
    gathered.setName( target[0] )
    
    Execute()

Parameters( 'blocksize', 'numblocks' ,'tgt','src' )
Types( blocksize=eval, numblocks=eval )

if __name__ == '__main__':
    
    # format the ouput that goes to stdout
    check_required( 'blocksize','numblocks' )
    check_required( 'tgt' )
    check_required( 'src' )
    # parse the command line arguments
    
    env = parse_args()
    target = [ env.pop('tgt') ]
    source = [ env.pop('src') ]
         
    scatter_bldr(target, source, env)

else:
    __all__ = ['MyScatter']
        
    from slimproj_core.builders.CreateBuilders import add_to_slim_env
    
    MyScatter = add_to_slim_env( "MyScatter", scatter_bldr )
    

