#!/usr/bin/env python
# encoding: utf-8
"""
@package configure_slimpy
Generate a script SLIMpy can use to update defaults on import
script must be python and contain: 
    a dict object named 'DEFAULTS'
    an integer RC_VERSION

configure_slimpy takes two optional arguments dest and rc_name
the values are a path and a filename respectively.

On import SLIMpy looks for an environment variable SLIMPY_RC,
a file named .slimpy_rc in the current directory or a file
named .slimpy_rc in the users $HOME directory in that order.
The first file that it finds it will use.

An example of generating a script
 
@code
[bash]$ python configure_slimpy.py [dest=] [rc_name=] [slimpy options]
Wrote file: '/Users/sean/.slimpy_rc'

<edit your script>
@code 
 
@param dest destination of the .slimpy_rc file may be \a global \a local or a path name.
@param rc_name the name of the .slimpy_rc file defaults to ".slimpy_rc"
"""

__copyright__ = """
Copyright 2008 Sean Ross-Ross
"""
__license__ =  """
This file is part of SLIMpy.

SLIMpy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SLIMpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SLIMpy. If not, see <http://www.gnu.org/licenses/>.
"""


RC_VERSION = 1

from SLIMpy.setup import *

from SLIMpy import env
from os.path import join, split, isdir,exists
from string import Template
import os


def get_rc_filename(dest,rc_name):
    """
    @param dest destination of the .slimpy_rc file may be \a global \a local or a path name.
    @param rc_name the name of the .slimpy_rc file defaults to ".slimpy_rc"
    @return a fully formed path name 
    """
    if dest == 'global':
        HOME = os.environ.get('HOME',None)
        if not HOME:
            option_parser.error('coultd not find home enironment')
        slim_rcfile = join(HOME,rc_name)
    elif dest == 'local':
        slim_rcfile = rc_name
    else:
        assert isdir(dest)
        slim_rcfile = join(dest,rc_name)
        
    return slim_rcfile


def check_exists( slim_rcfile ):
    """
    checks if the rc file already exists and if so 
    prompt the user if they truly want to over write it
    """
    if exists( slim_rcfile ):
        while 1:
            ans = raw_input( "file '%s' exists.\n"
                             "Are yout sure you want to overwrite? [Y|n]: " %slim_rcfile)
            ans = ans.lower()
            if ans in ['no','n']:
                raise SystemExit( 'goodbye' )
            elif ans in ['yes','y','']:
                return 
            else:
                print "sorry need 'y' or 'n' answer"

def create_dict_lines( key ,slimpy_rc):
    """
    Write the current defaults to the SLIMpy rc file with documentation
    """
    from SLIMpy.setup.DEFAULTS import SYS_DEFAULTS
    
    slimvars = env[ 'slimvars' ]
    
    djoin = lambda key,value: "%s : %s" %( repr(key), repr(value) )
    doc = "# " + slimvars.slimdoc.get(key,"No Doc")
    doc = doc.replace('\n','\n# ')
    value = slimvars[key]
    val2 = SYS_DEFAULTS.get(key,"No Default value")
    
    l1 = djoin(key, val2)
    l2 = djoin(key, value)
    
    print >> slimpy_rc
    print >> slimpy_rc, doc
    print >> slimpy_rc, "#"+"="*79
    print >> slimpy_rc, '#',l1,','
    
    if SYS_DEFAULTS.get(key, None) == value:
        pass
    else:
        print >> slimpy_rc, l2,','
        
    print >> slimpy_rc, "#"+"="*79

def write_header( slimpy_rc ):
    """
    Write the preamble to the rc file 
    """
    import SLIMpy,time
    print >> slimpy_rc, "'''"
    print >> slimpy_rc, "slimpy_rc file:"
    print >> slimpy_rc, "Created on",time.strftime( "%a, %b %d, %Y" )
    print >> slimpy_rc
    print >> slimpy_rc, SLIMpy.__version__,"-",SLIMpy.__date__
    print >> slimpy_rc
    print >> slimpy_rc, SLIMpy.__license__
    print >> slimpy_rc, "'''"
    print >> slimpy_rc
    print >> slimpy_rc, "RC_VERSION =", RC_VERSION
    print >> slimpy_rc

if __name__ == '__main__':
    
    Parameters( 'dest', 'rc_name')
    Defaults( dest='global',rc_name='.slimpy_rc' )
#    check_required( 'dest' )
    
    
    pars = parse_args( )
    
    dest = pars['dest']
    rc_name = pars['rc_name']
    
    slim_rcfile = get_rc_filename( dest, rc_name )
    
    check_exists( slim_rcfile )
                
    slimpy_rc = open( slim_rcfile, 'w' )
    
    write_header( slimpy_rc )
    
    
    print >> slimpy_rc, "DEFAULTS = {"
    for key in DEFAULTS.DEFAULTS:
        create_dict_lines( key,  slimpy_rc) 
    
    print >> slimpy_rc
    print >> slimpy_rc, "}"
    
    print "Wrote file: '%s'" %slim_rcfile
    
