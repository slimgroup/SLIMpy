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
#from slimpy_base.utils.GlobalVars import GlobalVars

from slimpy_base.Environment.InstanceManager import InstanceManager
from itertools import starmap
from os import sep

def gethostname():
    import os
    return os.uname()[1]
    
def is_localhost( nodename ):
    if nodename is None:
        return True
    if isinstance(nodename, str):
        if nodename == 'localhost':
            return True
        if nodename == gethostname():
            return True
    else:
        return False
    
class Unix_Pipes( object ):
#    slimvars = GlobalVars()
    env = InstanceManager()
    JOIN_PIPE  = " | ".join

    
    @classmethod
    def prepend_datapath(cls, is_loc, is_tmp , com):
        '''
        choose a datapath from one of the global variables localtmpdir, 
        globaltmpdir or datapath.
        return com augmented by "DATAPATH=%(dp)s %(com)s" 
        '''
        local_dp  = "DATAPATH=%s" % cls.env['slimvars']['localtmpdir'] + sep
        tmp_global_dp = "DATAPATH=%s" % cls.env['slimvars']['globaltmpdir'] + sep
        global_dp = "DATAPATH=%s" % cls.env['slimvars']['datapath'] + sep

        if is_tmp:
            if is_loc:
                dp = local_dp
            elif is_loc is False:
                dp = tmp_global_dp
            else:
                dp = False
        elif is_tmp is False: # not tmp
            dp = global_dp
        else:
            dp = None
#                print dp
        if dp:
            return "%s %s" %( dp, com )
        else:
            return com

    @classmethod
    def pipe_join( cls, cmd_list, is_local=None,is_tmp=None ):
        """
        join cmand 
        """

        if is_tmp is None: is_tmp = [None] * len(cmd_list)
        if is_local is None: is_local = [None] * len(cmd_list)
        assert len(is_tmp) == len(is_local) == len(cmd_list), "not a user error. should not get here"
        
        loc_tmp_cmd = zip(is_local,is_tmp, cmd_list)
        
        star = starmap( cls.prepend_datapath, loc_tmp_cmd )
        
        ret = cls.JOIN_PIPE( star )
        return ret
          
    @classmethod
    def stdout_join(cls, cmd, outfile):
        return " 1> ".join([cmd,outfile])
    
    @classmethod
    def stderr_join( cls, cmd, outfile):
        return " 2> ".join([cmd,outfile])

    @classmethod
    def sub( cls, targ, **kargs):
        '''
        Unix_Pipes.sub( targ, **kargs )
        creates a string.Template from targ and sub in kargs
        ''' 
        return Template( targ ).substitute( **kargs )

    
    @classmethod
    def stdin_join( cls, infile, cmd):
        return "< %s %s" %(infile,cmd)
    
    file_in_out = "< ${STD_IN} ${COMMAND} > ${STD_OUT}"
    file_out    = "${COMMAND} > ${STD_OUT}"
    file_in     = "< ${STD_IN} ${COMMAND}"
    file_       = "${COMMAND}"
    rsh         = '${RSH} ${NODE} "${COMMAND}"'
    
#    @classmethod
#    def remote_command(cls, node, command):
#        cls.sub( cls.rsh, RSH=cls.slimvars['rsh'], NODE=node, COMMAND=command )
    
    @classmethod
    def replace_quotes(cls,cmd):
        cmd = cmd.replace('\\"','\\\\"')
        return cmd.replace('"','\\"')
    
    @classmethod
    def CreateComand( cls, cmdlist, node_name=None , 
                      source=None, target=None, 
                      is_local=None,is_tmp=None, err=None, ssh_localhost=False):
        
        cmd = cls.pipe_join( cmdlist, is_local, is_tmp)
        
#        sub = lambda targ, **kargs: Template( targ ).substitute( **kargs )
        
        if source:
            if target:
                # IN and OUT
                cmd = cls.sub( cls.file_in_out, STD_IN=source, COMMAND=cmd, STD_OUT=target ) 
            else:
                cmd = cls.sub( cls.file_in, STD_IN=source, COMMAND=cmd )
        elif target:
            cmd = cls.sub( cls.file_out, COMMAND=cmd, STD_OUT=target )
        else:
            cmd = cls.sub( cls.file_, COMMAND=cmd )
        
        if err:
            cmd = cls.stderr_join( cmd, err )
        
        if ssh_localhost or not is_localhost(node_name) :
            
            if is_localhost(node_name):
                node_name = gethostname() 
#            print node_name
            cmd = cls.replace_quotes(cmd)
            cmd = cls.sub( cls.rsh, 
                       RSH=cls.env['slimvars']['rsh'],  
                       NODE=node_name, 
                       COMMAND=cmd )
        return cmd

