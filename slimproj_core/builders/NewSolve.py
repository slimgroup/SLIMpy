"""
General solver builder
"""
from slimpy_base.User.adiFactories import VectorFactory as _vf
from slimpy_base.utils.slim_decorators import depends_on,depends_on_functions
from slimpy_base.setup.ParseEnv import parse_env
from slimpy_base.Environment.InstanceManager import InstanceManager
#from slimpy_base import vectorf, parse_env, env as __env__

__author__ = "Sean Ross-Ross"

vector = _vf( )
__env__ = InstanceManager( )

@depends_on( 'solver')
@depends_on_functions('setup_callback')
@depends_on_functions('precondition_callback')
@depends_on_functions('transform_callback')
@depends_on_functions('inv_callback')
@depends_on_functions('solver_callback')
@depends_on_functions('result_callback')
def SolveBuilder( target, source, env ):
    """
    @ingroup sconsint 
    
    Base solve routine with no default values
    env must define the following functions:
    
    @param problem is a package containing default callbacks and documentation.
         see \ref contrib_problems for a list of existing problems in SLIMpy
    
    @param setup_callback defined as setup_callback( target, source, env ): 
            returns the initial vector, useful for
            managing augmented vectors
            
    @param solver_callback defined as solver_callback( target, source, env, A ): 
            returns a solver instance
             
    @param precondition_callback defined as  precondition_callback( target, source, env, space ):
            returns the preconditioner linear operator 'P'
        
    @param transform_callback defined as  transform_callback( target, source, env, space ):
            returns the transform 'A' to pass to the solver 
            'solve' method
            
    @param inv_callback defined as  inv_callback( target, source, env, space ):
            optional, returns the linear operator 'C'
            in not specified uses the \a transform_callback
            
    @param result_callback defined as  result_callback( target, source, env, result )
            returns None
            sets the name of the result, useful for
            managing augmented vectors 
    
    
    @remarks
    Solves The system of equations: 
    @code
    >>> b = P*data
    >>> x = solver.solve(A,  b )
    >>> result = P.adj() * ( C*x )
    @endcode
    where:
     - \a data   is the result of calling setup_callback
     - \a P      is the result of calling precondition_callback
     - \a solver is the result of calling solver_callback
     - \a C      is the result of calling inv_callback
    \par 
    also
     - \a result will be given to result_callback if it was given otherwise 
       SolveBuilder calls result.setName for the fist SCons target passed in.
    
    \par Examle
    The SolveBuilder builder ultimately ends up as a SLIMpy builder.
    Using SolveBuilder in SCons is a bit different. In SCons SolveBulider 
    is just called Solve.
    @code
    from slimproj import *
    from SLIMpy.problems import *
    def transform_callback( target, source, env, space ):
        return Identity( space )
    Solve( target, source, problem=l2_min_problem,
            transform_callback=transform_callback )
    
    @endcode 

    \sa \ref slimpy_contrib.problems "problems"
    """
    parse_env( env )
    
    default_package = env.get( 'problem', env.get( 'default_pack' ,{} ) )
    Get = lambda name : env.get( name, default_package.get(name) )
    #====================================================================
    # Setup Callback Sets up the initial vector    
    vector_setup = Get( 'setup_callback')
    if vector_setup is None:
        data  = vector( str( source[0] ) )
    else:
        data = vector_setup( target,source, env )
    #====================================================================
    
    
    #====================================================================
    # Preconditioner Callback: create a preconditioner P    
    precondition_callback = Get( 'precondition_callback' )
    if precondition_callback is not None:
        P = precondition_callback( target,source, env, data.space )
    else:
        raise Exception( "need to specify precondition_callback")
    #====================================================================
    
    
    #====================================================================
    # Transform Callback: create a transform 'A', for the solver    
    transform_callback = Get( 'transform_callback' )
    if transform_callback is not None:
        A = transform_callback( target, source, env, P.range() )
    else:
        raise Exception( "need to specify transform_callback")
    #====================================================================
    
    
    #====================================================================
    # Inverse Callback: create a transform  'C', to return the result back into the data domain        
    inv_callback = Get( 'inv_callback' )
    if inv_callback is not None:
        C = inv_callback( target, source, env, P.range( ) )
    else:
        C = A
    #====================================================================
    
    
    #====================================================================
    # solver/Solver Callback: get or create a solver 'solver'    
    solver = Get( 'solver' )
    if solver is None:
        solver_callback = Get( 'solver_callback' )
        if solver_callback is not None:
            solver = solver_callback( target, source, env, A )
    if solver is None:
        raise Exception( "need to specify 'solver' or 'solver_callback' ")
    #====================================================================
    
    
    #====================================================================
    # Transform Callback: create a transform 'A', for the solver    
    result_callback = Get( 'result_callback' )
    #====================================================================
    
    
    #====================================================================
    # Main Routine     
    b = P*data
    
    x = solver.solve(A,  b )
    
    result = P.adj() * ( C*x )
    #====================================================================
    
    
    #====================================================================
    # Set the result 
    if result_callback is None:    
        result.setName( str( target[0] ) )
    else:
        result_callback( target, source, env, result )
        
    __env__.Execute( )
    return result

SolveBuilder.__example__ = """
Solve( b, x, transform_callback=operator, solver=my_solver )
"""



