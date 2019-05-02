"""
Helper functions to create SCons builders out of ???
"""
from slimproj_core.builders.CreateBuilders import CreateSLIMpyBuilder
from SCons.Script.SConscript import SConsEnvironment
from slimproj_core.builders.my_de_call import DefaultBuilderCall
import inspect

class slim_builder( object ):
    """
    @ingroup sconsint
    This function is for SCons integration with SLIMpy inline inside the SConstruct file.
    This is a python decorator function.
    \param func must be a function with signature func( target, source, env )
    
    \par Example:
    @code
    from slimproj import *
    
    @slim_builder
    def MyBuilder( target, source, env ):
        parse_env( env )
        
        ...function body ...
        
        Execute( )
    
    MyBuilder( 'foo.rsf', 'bar.rsf' )
    @endcode
    \sa \ref slimpy_base.Environment.InstanceManager.InstanceManager.Execute "Execute" 
    \sa \ref slimpy_base.setup.ParseEnv.parse_env "parse_env"
    \sa \ref slimpy_base.utils.slim_decorators.depends_on "depends_on"
    \sa \ref slimproj_core.builders.funtion_decorators.slim_builder_simple "slim_builder_simple"
    """
    def __new__( cls , func ):
        
        if isinstance(func, SConsEnvironment ):
            return object.__new__( cls, func )
        else:
            return cls.create(func)
    
    def __init__( self, env ):
        self.env = env
    
    def __call__( self, func ):
        self.create( func, self.env )
    
    @classmethod
    def create(cls, func , env=None ):
        new_slimpy_builder = CreateSLIMpyBuilder( func.__name__ , func )
    
        if env:
            env['BUILDERS'][func.__name__] = new_slimpy_builder
            
        return DefaultBuilderCall( new_slimpy_builder )



hassuffix = lambda src: hasattr(src, 'suffix') and (src.suffix == '.rsf' )
class slim_builder_simple( object ):
    """
    @ingroup sconsint
    This function is for SCons integration with SLIMpy inline inside the SConstruct file.
    This is a python decorator function.
    \param func must be a function with signature func( vectors, [keywords=...] )
    \post the function slim_builder_simple is similar to slim_builder except that the preamble is handled 
    automatically. 
     - all of the sources in the SCons call are converted to vectors
     - the keyword arguments are tracked as dependencies
     - the return value of func may be a vector or a sequence of vectors that are automatically 
       set as SLIMpy targets
       
    \return a Scons Default Environment Call
    
    \par Example:
    @code
    from slimproj import *
    
    @slim_builder_simple
    def MyBuilder( vectors, [keyword arguments] ):
        
        ...function body ...
        
        return results
    
    MyBuilder( 'foo.rsf', 'bar.rsf'  )
    @endcode
    
    \sa \ref slimpy_base.utils.slim_decorators.depends_on "depends_on"
    \sa \ref slimproj_core.builders.funtion_decorators.slim_builder "slim_builder"
    """
    def __new__( cls , func ):
        
        if isinstance(func, SConsEnvironment ):
            return object.__new__( cls, func )
        else:
            return cls.create(func)
    
    def __init__( self, env ):
        self.env = env
    
    def __call__( self, func ):
        self.create( func, self.env )
    
    @classmethod
    def create(cls, func , env=None ):
        
        args, varargs, varkw, defaults = inspect.getargspec(func)
        
        if defaults is None:
            kwargs = []
        else:    
            kwargs =  args[-len(defaults):]
        
        newbuild = new_builder( kwargs,varkw, func )
        new_slimpy_builder = CreateSLIMpyBuilder( func.__name__ , newbuild, depends_on=kwargs )

        if env:
            env['BUILDERS'][func.__name__] = new_slimpy_builder
        
        return DefaultBuilderCall( new_slimpy_builder )

class new_builder( object ):
    
    def __init__(self, kwargs,varkw, func ):
        self.kwargs =kwargs
        self.varkw = varkw
        self.func = func
        
    def __call__( self, target, source, env ):
        
        from SLIMpy.setup import parse_env
        from SLIMpy import vector,Execute
        
        env = parse_env( env  )
        
        kwdict = {}
        for karg in self.kwargs:
            if karg in env:
                kwdict[karg] = env[karg]
        
        vectors = [vector(src) for src in source if hassuffix(src)]
        
        if self.varkw:
            result = self.func( vectors, **env )
        else:
            result = self.func( vectors, **kwdict )
        
        if isinstance(result, (list,tuple) ):
            if not len(result) <= len(target):
                raise Exception("The number of results returned from function '%s' "
                                "must be less than or equal to the number of SCons targets given:\n"
                                "results = %s\n"
                                "targets = %s" %( self.func.__name__, result, [str(tgt) for tgt in target]) )
                
            for i,res in enumerate(result):
                res.setName( target[i] )
        elif result is None:
            pass
        else:
            result.setName( target[0] )
    
        Execute( )
        
        return 

