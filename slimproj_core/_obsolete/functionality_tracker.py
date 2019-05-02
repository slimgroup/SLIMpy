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

from slimproj_core.builders.BuilderFunctions import DEFAULT_PROFILES

def tracker_emitter( target, source, env):
    
    source.extend(DEFAULT_PROFILES)
    
    return target, source

    

from hotshot.stats import load
from sys import modules
from os.path import split, splitext  
from inspect import ismodule, isclass,isroutine
import pickle

def catigorize( table, obj_name,obj, stats, optional_doc ):
    
    if isclass(obj):
        type = 'Class'
        mod = modules[obj.__module__]
    elif ismodule(obj):
        type = 'Module'
        mod = obj
    
    dir,file = split( mod.__file__ )
    name,ext = splitext( file )
    
#    print 'Section name:', obj_name
    
    
    method_tuples, msg = stats.eval_print_amount(name, stats.fcn_list[:], '')
#    num, method_tuples = stats.get_print_list((name,))
    
    tested_methods = set([ name for file,line,name in method_tuples])
    
    
    all_methods = set([ key for key,val in obj.__dict__.iteritems() if isroutine(val) ])
    tested_methods.intersection_update( all_methods )
#    print "all_methods:",all_methods
#    
#    print
#    print "tested methods:", all_methods.intersection(tested_methods)
#    print
#    print "untested methods:", all_methods.difference(tested_methods)
    
    section = table.setdefault("%(obj_name)s" %vars() ,{})
    section['all_methods'] = all_methods
    section['tested_methods'] = tested_methods
    section[ 'doc' ] = optional_doc
    
    return  

def tracker_builder( target, source, env ):

#    flist = env['funcmod']
    str_src = [str(src) for src in source ]
    
    table = {}
    f = open(str(target[0]), 'w')
    
    if str_src:
#        raise Exception( 'calling tracker_builder when no profiles have been performed' )
        
        
        stat = load( str_src[0] )
        for src in str_src[1:]:
            stat.add( load( src ) )
        
        stat.strip_dirs( )
        stat.sort_stats( 'module' )
        
        
#        from slimpy_base.utils.Profileable import Profileable
#        profile_classes = Profileable.Profiles
        from inspect import isfunction,isclass,ismethod
        from sys import modules
        import slimpy_base
        
        is_slim_mod = lambda mod : mod.startswith("SLIMpy")
        
        slim_mods = [ mod for key,mod in modules.iteritems() if is_slim_mod(key) ]
        profile_classes = { }
        class_set = set() 
        
        for mod in slim_mods:
            for item in dir(mod):
                atr = getattr(mod, item)
                if isclass(atr) and is_slim_mod(atr.__module__):     
                    class_set.add( atr )
        
        for klass in class_set:
            (klass, doc) = profile_classes.setdefault(klass.__name__, (klass, {}) )
            for method in klass.__dict__.values():
                if hasattr(method, "__note__"):
                    note = getattr(method, "__note__")
#                    print note 
                    doc[method.__name__] = note
        
#        print profile_classes
        
        for name, (klass, doc) in profile_classes.iteritems():
    #        print name,doc
            catigorize( table,name, klass, stat, doc )
    #        print table[name]['doc']
        
        
    else:
        pass
        
    pickle.dump( table, f )

    
    return

