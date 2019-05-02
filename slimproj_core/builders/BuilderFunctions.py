"""
List of helpful SCons builders to work with SLIMpy
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


from slimpy_base import __version__ as slimpy_version
from inspect import isroutine,getsource,getsourcefile,getsourcelines
from itertools import chain
from os import environ
from os.path import isfile
from re import compile
from SCons.Script import Help


def rsf_binary_emitter( target, source, env):
    'add binary file as a side effect and call Clean '
    rsf_headers = [ tgt for tgt in target if hasattr(tgt, "suffix") and tgt.suffix == '.rsf']
    in_eq = compile("^\W*in=(.*)$")
    for node in rsf_headers:
#        contents =  node.get_contents()
        contents =  None
        if contents:
            lines = contents.split('\n')
            lines.reverse()
            for line in lines:
                all = in_eq.findall( line )
                if all:
                    data = all[0].replace("@","\@")
                    break
        else:
            data_path = environ.get("DATAPATH", "")
            data =  data_path +node.name + "@" 
        
        env.SideEffect( data, node )
        env.Clean( node, data )
#        target.append( data )
        
    return target, source

def logfile_emitter(target,source,env):
    'append a log file target if logfile in env'
    logfile =  env.get('logfile', None)
    if logfile is not None:
        target.append( logfile )
        if not env.has_key('verbose'):  
            env['verbose'] = 0
            
    return target, source


DEFAULT_PROFILES = []
def profile_emitter_wrapper(act):
    """
    profile 'act' 
    Uses functional closure to return an emitter func
    that calls the profile builder
    """
    def profile_emitter(target, source, env):
        ''
        profiler = env.get( 'profile', None )
        
        if profiler is not None:
            profiler.set_action(act)
            profiler.set_env(target,source,env)
            profiler.profile( )
            
        return target, source
    
    return profile_emitter

def dottest_emitter_wrapper(act):
    """
    profile 'act' 
    Uses functional closure to return an emitter func
    that calls the profile builder
    """
    def dottest_emitter(target, source, env):
        ''
        dottester = env.get( 'dottest', None )
        
        if dottester is not None:
            dottester.set_action(act)
            dottester.set_env(target,source,env)
            dottester.dot_test( )
            
        return target, source
    
    return dottest_emitter


def slimpy_file(mod_file):
    """
    ??
    """
    if mod_file.endswith('.pyc') and isfile(mod_file[:-1]):
        mod_file = mod_file[:-1]
    def slimpy_file_emitter( target, source, env):
        
        coutput = env.get('coutput',None)
        
        val = env.Value( slimpy_version )
        source.append( val )
        
        if coutput is not None:
            target.append(coutput)
        
        source.append( mod_file )
        
        if mod_file != __file__:
            source.append( __file__ )
      
        
        return target, source
    return slimpy_file_emitter



def slimpy_variable_emitter( target ,source, env):
    """
    add dependencies on SLIMpy global variables
    if a variable defined in slimvars and specified in
    env, then slimpy adds it as a Value source 
    """
    from slimpy_base.Environment.InstanceManager import InstanceManager
    slimvars = InstanceManager()['slimvars']
    
    for key in slimvars.keys():
        if env.has_key(key):
            par =env[key]
            val = env.Value( (key,par) )
            source.append( val )
    
    return target ,source
    

def additional_parameters( additional_pars ):
    """
    Add dependencies on functions as environment parameters
    """
    
    def additional_parameter_emitter( target ,source, env):
        default_package = env.get( 'default_pack' ,{} )
        Get = lambda name : env.get( name, default_package.get(name) )
        has_key = lambda key: env.has_key(key) or default_package.has_key(key)
        
        parameters = chain( additional_pars, default_package.get('additional_parameters',[]) )
        for key in parameters:
            Get(key)
            if has_key(key):
                par = Get(key)
                val = env.Value( (key,par) )
                source.append( val )
        
        return target ,source
    return additional_parameter_emitter

def function_parameters( funcnames ):
    """
    Add dependencies on functions passed in to env
    """
    def additional_parameter_emitter( target ,source, env ):
        default_pack = env.get( 'problem', env.get('default_pack') )
        Get = lambda name : env.get( name, default_pack.get(name) )
        has_key = lambda key: env.has_key(key) or default_pack.has_key(key)
        
        new_pars = set()
        for key in funcnames:
            if has_key(key):
                func =Get(key)
                
                if isroutine(func):
                    try:
                        source_code = getsource(func)
                    except IOError:
                        source_code = None
                        
                    if source_code is None:
                        continue
                    
                    sha = hash(source_code)
                    rr ="<function %s hash=%s>" %(func.__name__,sha)
                    val = env.Value( (key,rr) )
                    
                    source.append( val )
                    
                pars = getattr( func, '__additional_dependancies__' , [] )
                
                new_pars.update( pars )
                
        if new_pars:
            additional_parameters(new_pars)(target,source,env)
        
        return target ,source
    return additional_parameter_emitter
            
help_names = set()
def help_emitter( target, source, env ):
    if env.has_key('default_pack') or env.has_key('problem'):
        default_pack = env.get( 'problem', env.get('default_pack') )
        help_name = default_pack['name']
        if  help_name in help_names:
            return target,source
        else:
            help_names.add( help_name )
            
        Help("Help for %(help_name)s\n" %vars())
        Help("eg.\n" %vars())
        Help("Solve( target, source, problem=%(help_name)s,\n" %vars() )
        Help("                       ...params... ,\n" %vars() )
        Help("     )\n\n" %vars() )
        
        
        keys = default_pack.keys()
        keys.sort()
        for item in keys:
            val= default_pack[item]
            if item in ['doc','name']:
                continue
            doc = default_pack['doc'].get(item)
            if doc is None:
                if isroutine(val):
                    doc = val.__doc__
                if doc is None:
                    doc = "No doc for %(item)s" %vars()
                else:
                    pars = getattr( val, '__additional_dependancies__' , [] )
                    doc = "Depends on %s\n" %pars + doc  
            
            doc = doc.strip()
            doc = "\n\t".join([ line.strip() for line in doc.split('\n') ]) 
            if isroutine(val):
                name = (val.__name__)
                try:
                    stuff = ( val.__name__,repr(getsourcefile(val)),getsourcelines(val)[-1])
                except IOError:
                    val = "<function %s in ???>" %name
                else:
                    val = "<function %s in %s at line %s>" %stuff
                    
            Help("  %(item)s: default=%(val)s" %vars() )
            Help("\n\n\t%(doc)s\n\n" %vars() )
        
    return target ,source
