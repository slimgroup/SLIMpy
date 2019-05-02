#!/usr/bin/env python
# encoding: utf-8
"""

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

from optparse import Option,OptionParser
from pickle import load
import SLIMpy
from slimpy_base.Core.Runners.dotRunner import dotRunner
from slimpy_base.utils.Filters import DebugFilter,VerbosityFilter
import re


parser = OptionParser(usage="%prog [options] logfile")


v_opt = Option( '-v' ,
            type=int,
            default=0,
            dest='verb' )

#filt_opt = Option('-f' ,'--filt',
#                  action='store_true')

allow_opt = Option('-a' ,
                  dest='debug',
                  action='append',
                  )

node_opt = Option('-n' ,
                  dest='node',
                  action='append',
                  )

proc_opt = Option('-p' ,
                  dest='proc',
                  type=int,
                  action='append',
                  )

dot_opt = Option( '--dot',
                  action='store_true' 
                  )

list_opt = Option( '-l','--list',
                  action='store_true' 
                  )

abr_opt = Option( '-b','--abridge',
                  action='store_true', 
                  dest='abridge',
                  default=False,
                  )

time_opt = Option('-t','--time',
                  action='store_true',
                  )

cmd_opt = Option('--cmd',
                 action='store_true',)

parser.add_option( v_opt )
#parser.add_option( filt_opt )
parser.add_option( list_opt )
parser.add_option( allow_opt )
parser.add_option( node_opt )
parser.add_option( proc_opt )
parser.add_option( dot_opt )
parser.add_option( abr_opt )

_re_kw = re.compile('(.*?)=(.*)')
def split_args(args):
    p = []
    kw = {}
    for arg in args:
        items = _re_kw.findall(arg)
        if items:
            kw.update( items )
        else:
            p.append(arg)
    
    return p,kw
    

if __name__ == '__main__':
    
    options, args = parser.parse_args()
    
    p,kw = split_args(args)
    
    if not p:
        parser.error("need file")
    file = p[0] 
        
    record = load( open(file) )
    
    if options.list:
        record.print_filter_list()
    
    elif options.dot:
        record._init_env()
        runner = dotRunner(record.command_records)
        runner.set_graph( record.graph )
        print runner.printDot( )
    else:
        vfilt = VerbosityFilter( options.verb )
        dfilt = DebugFilter( options.debug or set( ) )
#        node = options.node,options.proc
        
        record.set_abridge( options.abridge )
        
        record.add_filter( vfilt )
        record.add_filter( dfilt )
        
        record.set_filter_type( 'any' )
        
        record.print_log( )
    # 
    




