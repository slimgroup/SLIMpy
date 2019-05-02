"""
function to gudie the user to useful things
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


from inspect import ismodule, isclass, isroutine
from itertools import count

## interactive help for SLIMpy 
# @ingroup functions
# @param names get help for objects 
def shelp( *names ):
    """
    some other useful helper functions:
    listLinop() -> prints a list of all the linear operator classes 
    listPlugins() -> print the plugins available ( ie. rsf )
    printglobal() -> prints all global variables in 'slimvars'
    """
    if not names:
        print "available help commands:" 
        for item in globals():
            
            if item.startswith( '_help_' ):
                print "   ", repr( item[6:].replace( "_", " " ) )
        print
        print shelp.__doc__
         
    
    for name in names:
        try:
            name = str( name ).lower()
            name = name.replace( " ", "_" )
            _help_func = eval( '_help_%s' %name )
        except Exception:
            print
            print "No help for item,", repr( name ), 
            print ". call _help() to see all available help commands." 
        else:
            _help_func()
        
        
is_slimpy = lambda value: value.__name__.startswith( 'SLIMpy' )
no_ = lambda key: not key.startswith( '_' )

from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType
opers  = LinearOperatorType.LinearOperators.keys()

notoper = lambda key: key not in opers

def _help_whats_new():
    print
    print "This is new"
    print

def _help_modules():
    
    print 'SLIMpy modules'
    print

    key_func = lambda key, value: ismodule( value ) and is_slimpy( value ) and no_( key )
    
    keydo = dict( _helphelper( key_func ) )
    
    _format_keydo( keydo )

def _help_classes():
    print "SLIMpy classes:"
    print "for linear operator classes please use: listLinop( ) function"
    print 
    
    
    key_func = lambda key, val: notoper( key ) and isclass( val ) and no_( key )
    
    keydo = dict( _helphelper( key_func ) )
    
    _format_keydo( keydo )
    
def _help_functions():
    print "list of slimpy functions"
    
    
    
    key_func1 = lambda key, val: isroutine( val ) or ( not isclass( val ) and not ismodule( val ) )
    key_func = lambda key, val: notoper( key ) and key_func1( key, val ) and no_( key ) 
    
    keydo = dict( _helphelper( key_func ) )
    
    _format_keydo( keydo )

def _help_other():
    pass
    
def _format_keydo( keydo ):
    
    longest = lambda a, b: len( a ) > len( b ) and a or b  
    lnst = len( reduce( longest, keydo.keys() , "" ) )
    print
    for key, doc in keydo.iteritems():
        print key +" "+ "." *( lnst-len( key ) ) , "-", 
        print doc

def _helphelper( key_func ):
    
    import slimpy_base
    
    for key, value in vars( SLIMpy ).iteritems():
        if key_func( key, value ):
            if value.__doc__ and value.__doc__.strip( "\n \t" ):
                doc = value.__doc__.strip( "\n \t" )
                ds = doc.splitlines()
                if ds > 1:
                    
                    for i in count():
                        if ds[i]:
                            doc = ds[0] + " ..."
                            break
            else:
                doc = ""
                
            yield key, doc
    
