"""
parse a dict or SCons.Environment object and update the slimvars
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

from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.setup.DEFAULTS import DEFAULTS

__env__ = InstanceManager()



def parse_env( env, *E, **kw ):
    """
    updates 'slimvars' class with values from 
    env that are also in 'DEFAULTS' retuns
    a dict with values from *E, **kw and updated 
    with the values from env that are not in 
    'DEFAULTS' 

    @param env:
    @type env: dict or SCons.Environment
    """
    
    log = __env__['record'](1, 'stat' )
    
    print >> log, "SLIMpy: Building AST"
     
    __env__.assure_new_instances( )
    
    if hasattr(env, "Dictionary" ): # assume scons base instance 
        e_dict = env.Dictionary()
    else: # assume dict
        e_dict = dict( env )
    
#    if e_dict.has_key( 'logfile' ) and e_dict['logfile']:
#        __log__.setLogFile( e_dict['logfile'] )
    ret_env = dict(*E, **kw)
    
    n_dict= {}
    
    for key in DEFAULTS.iterkeys():
        if key in e_dict:
            n_dict[key] = e_dict[key]
    
    __env__['slimvars'].setglobal( **n_dict )
    
    callbacks = e_dict.pop( 'callbacks' ,[])
    
    
    for func in callbacks:
        if isinstance(func, str):
            import function_callbacks
            func = getattr( function_callbacks, func )
        
        func( )
    
    ret_env.update( e_dict )
    
    return ret_env
