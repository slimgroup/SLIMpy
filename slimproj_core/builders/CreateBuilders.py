"""
Create SLIMpy default builders
"""
from SCons.Defaults import ConstructionEnvironment as _ConstructionEnvironment
from SCons.Script import Builder,Action
#from SCons.Tool import LaTeXScanner
from slimproj_core.builders.BuilderFunctions import dottest_emitter_wrapper
from slimproj_core.builders.BuilderFunctions import function_parameters
from slimproj_core.builders.BuilderFunctions import help_emitter
from slimproj_core.builders.BuilderFunctions import logfile_emitter,rsf_binary_emitter,slimpy_variable_emitter,additional_parameters
from slimproj_core.builders.BuilderFunctions import profile_emitter_wrapper,slimpy_file
#from slimproj_core.builders.SLIMdoc import how_to_gen,term_builder,term_emitter,tutorial_index,index_emitter
#from slimproj_core.builders.SLIMdoc import index_emitter_demo,howto_emitter
#from slimproj_core.builders.build_tests import slim_test_builder,slim_test_emitter
#from slimproj_core.builders.functionality_tracker import tracker_emitter, tracker_builder
#from slimproj_core.builders.list_class_profiles import func_builder
from slimproj_core.builders.my_de_call import DefaultEnvCall
#import inspect
import re
import sys

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



Default_SLIM_Builders = {}



def default_str_closure(name):
    'functional closure on default string function for slimpy actions'
    
    def default_str(target, source, env):
        'default string function for a slimpy action'
        targets = ', '.join( [repr(t.name) for t in target if hasattr(t,'suffix') and t.suffix == '.rsf' ])
        sources = ', '.join( [repr(t.name) for t in source if hasattr(t,'suffix') and t.suffix == '.rsf' ])
        
        cond = lambda val : hasattr(val,'read') and isinstance( val.read(), tuple ) and len(val.read()) == 2  
        
        xvals = [ val.read() for val in source if cond(val) ]
        
        vals = []
        for key,val in xvals:
            if isinstance(val, str):
                newvals = val.split('\n')
                i = 0
                lnv = len(newvals)
                while i < lnv and newvals[i].startswith('@'):
                    i+=1
                newval = newvals[i]
                allre = re.findall("def (.*)\(.*\):", newval)
                if allre:
                    newval =  "<function %s>" %allre[0] 
                else:
                    allre = re.findall(" lambda.*:", newval)
                    if allre:
                        newval =  "<function <lambda>>" 
                
                vals.append( (key,newval) )
            else:
                vals.append( (key,val) )
        
        values = ",\n    ".join([ "%s=%s"%( key,repr(item) ) for key,item in vals ])
        
#        print dir(val)
        sources = sources and ", [ %s ]" %sources or ", None"
        targets = targets and "[ %s ]" %targets or "None"
        values = values and ",\n    %s" %values or ""
        
        return "\n"+name + "( %(targets)s%(sources)s%(values)s )\n" %vars()
     
    return default_str

def post_mortem_closure( act ):
    """
    adds post mortem pdb stack trace 
    """
    def pm_action( target, source, env ):
        import bdb
        try:
            act( target, source, env )
        except bdb.BdbQuit:
            pass
        except:
            if env.get('post_mortem'):
                type, val, tb = sys.exc_info()
                import pdb 
                print
                print type, val
                print "launching post mortem"
                pdb.post_mortem( tb )
                
            raise

    return pm_action

def add_function_emitter( act ,slim_emitters):
    
    if hasattr(act, '__function_dependancies__'):
        funcnames = getattr(act, '__function_dependancies__')
        slim_emitters.append( function_parameters( funcnames) )
    else:
        pass
    
    return
    

def CreateSLIMpyBuilder( name, act , file_name=None, str_func=None , emitters=None, depends_on=None ):
    '''
    ???
    '''
    
    if str_func is None:
        str_func = default_str_closure( name )
    
    pm_act = post_mortem_closure( act )
    slimpy_action  = Action( pm_act, str_func )
    
    if file_name is None:
        mod = sys.modules[act.__module__]
        file_name = mod.__file__
    
    if depends_on is None:
        depends_on = []

    if hasattr(act, "__additional_dependancies__" ):
        additional_deps = getattr(act, "__additional_dependancies__" )
        depends_on.extend( additional_deps )
        
    slim_emitters = [
            rsf_binary_emitter,
            logfile_emitter,
            slimpy_variable_emitter,
            slimpy_file(file_name),
            additional_parameters(depends_on),
            profile_emitter_wrapper(act),
            dottest_emitter_wrapper(act),
            help_emitter
        ]
    
    add_function_emitter(act, slim_emitters)
    
    if emitters is None:
        emitters = []
        
    slim_emitters.extend( emitters )
    
    slimpy_builder = Builder( action = slimpy_action,
                                    emitter=slim_emitters,
                                    suffix = '.rsf',
                                    src_suffix = '.rsf')
    
    return slimpy_builder

def add_to_slim_env( name, act , file_name=None, str_func=None , emitters=None, depends_on=None):
    '''
    add default emitters and string functions and dependencies
    '''
    
    global Default_SLIM_Builders
    
    slimpy_builder = CreateSLIMpyBuilder( name, act , file_name, str_func , emitters, depends_on )
    
    Default_SLIM_Builders[name] = slimpy_builder
    
    
    def new_slim_tool(env):
        'auto '
        env['BUILDERS'][name] = slimpy_builder
        
    from SCons.Script import _SConscript
    if _SConscript._DefaultEnvironmentProxy:
        _SConscript._DefaultEnvironmentProxy['BUILDERS'][name] = slimpy_builder

    if 'TOOLS' in _ConstructionEnvironment:
        _ConstructionEnvironment[ 'TOOLS' ].append( new_slim_tool )
    else:
        _ConstructionEnvironment[ 'TOOLS' ] = ['default',new_slim_tool]
        
    dec = DefaultEnvCall( name, None, act.__doc__ )
    
    return dec

    

