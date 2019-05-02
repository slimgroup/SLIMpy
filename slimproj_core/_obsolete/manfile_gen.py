'''
genorate man file for slimproj
'''


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

from string import Template
import sys

man_template = Template("""
.TH SLIMPROJ 1 "${date}"
.SH NAME
slimproj \- SLIMpy tool for scons

.SH SYNOPSIS
${projec_doc}
To include slinproj in a SCons file use

.ES
from slimproj import *
.EE

.B slimproj
provides the following builder methods:

'\"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
'\" BEGIN GENERATED BUILDER DESCRIPTIONS
'\"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

${BUILDERS}

.SS Construction Variables

A number of useful construction variables are automatically defined by
scons for each supported platform, and additional construction variables
can be defined by the user. The following is a list of the automatically
defined construction variables:
'\"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
'\" BEGIN GENERATED CONSTRUCTION VARIABLE DESCRIPTIONS
'\"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
${VARIABLES}
""")
    
func_template = Template("""
.IP ${name}()
.IP env.${name}()
${doc}
${params}
${example}${author}
"""
)

example_tem = Template("""
.B Example:

.ES
${example}
.EE
""" )

authorstr = "\n.B Author:\n%s"
params_tem = Template("\n\n.B PARAMETERS:\n${params}\n\n")

def genorate_man():
    '''
    genorate_man() -> str
    '''
    import slimproj
    from slimproj_core.builders.CreateBuilders import Default_SLIM_Builders

    from slimpy_base import env
    
    
    
    
    slimvars = env['slimvars']
    
    keys = slimvars.slimGlobals.keys()
    keys.sort()
    
    manafie = lambda  key,doc: """\n.IP %s\n%s""" %(key,doc)
    
    VARIABLES =[]
    push = VARIABLES.append
    for key in keys:
        doc = slimvars.slimdoc.get( key, "No documentation")
        item = manafie( key, doc )
        push(item)
    
    
    
    BUILDERS = []
    push = BUILDERS.append
    esub = lambda ex: example_tem.substitute( example=ex.replace('\n    ','\n').replace('\n','\n ') )
#    print Default_SLIM_Builders
    bldr_keys = Default_SLIM_Builders.keys()
    bldr_keys.sort()
#    print bldr_keys
    for key in bldr_keys:
        builder = Default_SLIM_Builders[key]
        execfunc = builder.action.execfunction
        
        doc = hasattr(execfunc,"__doc__") and execfunc.__doc__ and execfunc.__doc__.strip() or "No Doc\n"
        doc = doc.replace('\n    ','\n')
        doc = doc.replace('\n','\n ')
        
        example = hasattr(execfunc,"__example__") and esub( execfunc.__example__ ) or ""
#        example = example.replace('\n    ','\n').replace('\n','\n ')
#        example = example.replace('\n','\n ')
        if hasattr(execfunc, '__additional_dependancies__'):
            params = getattr(execfunc, '__additional_dependancies__')
            params = ",\n".join(params)
            params = params_tem.substitute(params=params)
        else:
            params= ""
        
        emod = sys.modules[execfunc.__module__]
        if hasattr(emod, '__author__'):
            author = authorstr %emod.__author__
        else:
            author = ""
            
        func =func_template.substitute(name=key,example=example,
                                 doc=doc,
                                 author=author,
                                 params=params)
        
        push(func)
        
        
    mmm = dict()
    import time
    
    mmm['date'] = time.strftime( "%m/%y") 
    mmm['projec_doc'] = slimproj.__doc__
    mmm['BUILDERS'] = "\n".join(BUILDERS)
    mmm['VARIABLES'] = "\n".join(VARIABLES)
    
    return  man_template.substitute( **mmm)
    
