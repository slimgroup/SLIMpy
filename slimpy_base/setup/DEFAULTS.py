"""
Defaults for GlobalVars class

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

import os
from os.path import curdir, join, sep, isfile, devnull, abspath
NULLOUT = open( devnull, 'w' )


DEFAULTS = {
            "verbose": 0, 
            "debug" : ['cmd','err','stat'] , 
            "check_path" : False, 
            "strict_check" : 2, 
            "memsize":500 , 
#            "tmpdir": abspath( curdir ),              
#            "ispipe":True, 
            "runtype":'normal' , 
            "globaltmpdir": abspath( curdir ), 
            "localtmpdir": join( sep, 'var', 'tmp' ), 
            'datapath': abspath( os.environ.get( 'DATAPATH', abspath( curdir ) ) ), 

            "mpi": False, 
            "MPIFLAGS": "${MPIRUN} -np ${np} -hostfile ${NODEFILE}", 
            "NODEFILE" : None, 
            "NODELIST" : [],
            "nodemap_type":'lin' , 

            "MPIRUN" :  "mpirun_ssh", 
            "np" :  1 , 
            "rsh":  'ssh', 
            "eps":0, 
            "nwin": 0, 
            "abridge":True, 
            "test_devel":False, 
            'abridgeMap' : {abspath( curdir ):'.'}, 
            'walltime':30, 
            'no_del':False, 
            'logfile':None, 
            
            'keep_tb_info': True, 
            'show_std_err': False, 
            'use_scalar_obj': True,
            
            'sync_disk_om_rm': True,
            'SYNC_CMD': 'sync',
            
            'run_again':False,
            
            
            }



tmpPath = join( sep, 'var', 'tmp' )
PBS_JOBID = os.environ.get( 'PBS_JOBID', '' )

PBS_JOBID = join( tmpPath, PBS_JOBID )

if os.access( PBS_JOBID, os.W_OK | os.R_OK ):
    DEFAULTS['tmpdatapath'] = abspath( PBS_JOBID )
else:
    DEFAULTS['tmpdatapath'] = abspath( curdir )

SYS_DEFAULTS = DEFAULTS.copy() 

def rc_update_defaults():
    """
    try and get the defaults from the SLIMpy rcfile
    """
    
    SLIMPY_RC = os.environ.get( 'SLIMPY_RC', None )
    HOME = os.environ.get( 'HOME', None )
    
    if SLIMPY_RC is None:
        if isfile( '.slimpy_rc' ):
            SLIMPY_RC = '.slimpy_rc'
        elif isfile( join( HOME, '.slimpy_rc' ) ):
            SLIMPY_RC = join( HOME, '.slimpy_rc' )
        
    if SLIMPY_RC is not None:
        rc_globals = {}
        execfile( SLIMPY_RC, rc_globals )
            
        try:
            DEFAULTS.update( rc_globals['DEFAULTS'] )
        except KeyError:
            raise KeyError( "slimpy rcfile must contain 'DEFAULTS' attribute" )
        

rc_update_defaults()

