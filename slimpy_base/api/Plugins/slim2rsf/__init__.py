"""
Definitions of RSF package
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
from os import environ as _env
from os.path import join
from rsfContainer import rsf_data_container #IGNORE:W0403
from rsf_mpi_contianer import rsf_mpidata_container
from sfcommands import element, linear_ops, boolcmp, mpi_commands
#from slimpy_base.utils.GlobalVars import GlobalVars


 
env = InstanceManager()

#from rsfCommands import addAll as __addAll
def get_containers():
    """
    returns the rsf plugin data container
    """
    
    if not _env.get( "RSFROOT", None ):
        raise NotImplementedError( "Environment Variable 'RSFROOT'"
                                  " needed for slim2rsf plugin, was not found" )
    slimvars = env['slimvars']
    
    slimvars['RSFROOT'] = _env.get( "RSFROOT", "" ),'main rsf path'
    slimvars['RSFBIN'] = join( slimvars['RSFROOT'], "bin" ),'rsf binary path'
    slimvars['SEPROOT'] = _env.get( "RSFROOT", slimvars['RSFROOT'] ),'sep path set to RSFROOT if no sep environment'
    slimvars['SEPBIN'] = join( slimvars['SEPROOT'], "bin" ),'sep binary path'
    
    slimvars['abridgeMap'][ slimvars['RSFBIN'] +'/'] = ''
    slimvars['abridgeMap'][ slimvars['SEPBIN'] +'/'] = ''
#    base_name = rsf_data_container.base_name( )/
#    slimvars['abridgeMap'][base_name] = '$tmp/'
    
    rsf_plugins = {}
    rsf_plugins[rsf_data_container.name] = rsf_data_container
    rsf_plugins['slim2rsf'] = rsf_data_container 
    rsf_plugins["rsfmpi"] = rsf_mpidata_container
     
    return rsf_plugins
