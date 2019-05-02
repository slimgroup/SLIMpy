""" 
 @package slimpy_base 

 this is the main init file for SLIMpy 
    
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



import info

## major version number 
__version_major__ = 3
## minor version number 
__version_minor__ = 0
## svn revision number 
__revision__ = info.rev

__version__ = "SLIMpy: %(__version_major__)s.%(__version_minor__)s: svn revision %(__revision__)s" % vars()
__date__ = info.date


from slimpy_base.Environment.InstanceManager import InstanceManager

def initialize( ):
    """
    initialize SLIMpy environment
    """
    env = InstanceManager()
    
    from slimpy_base.Environment.hashTable import _HashTable
    from slimpy_base.Environment.GlobalVars import GlobalVars as _GlobalVars
    from slimpy_base.Environment.GraphManager import GraphManager
    from slimpy_base.Environment.KeyStone import KeyStone
    from slimpy_base.Core.MutiProcessUtils.EmploymentCenter import EmploymentCenter
    from slimpy_base.utils.Records import Records
    
    #singleton class any and all instances are the same in the same environment
    env['graphmgr'] = GraphManager
    # order matters fifo for exit funcs 
    env['table'] = _HashTable
    env['record'] = Records
    env['slimvars'] = _GlobalVars
    env['keystone'] = KeyStone
    env['center'] = EmploymentCenter
    
    
    
    env.assure_new_instances(  )
    
initialize( )