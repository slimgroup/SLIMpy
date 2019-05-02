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

#from slimpy_base.utils.Logger import Log
#from popen2 import Popen3,popen2
from subprocess import Popen, PIPE as __PIPE__
from slimpy_base.Core.Command.Drivers.Unix_Pipes import Unix_Pipes
from os.path import join
from pdb import set_trace
import re

#from slimpy_base.utils.GlobalVars import GlobalVars
#from slimpy_base.utils.hashTable import HashTable

from slimpy_base.Environment.InstanceManager import InstanceManager

SCALAR = re.compile( r'(\$\{SCALAR\[\d*\]\})' ).findall

class RemoteDriver( object ):
    """
    used to chain ooc_driver commands together
    """
    env = InstanceManager()
    _stderr_logfile = "stderr_logfile.log"
    
    def _get_stderr_logfile(self):
        return join( self.env['slimvars']['localtmpdir'], self._stderr_logfile )
    
    stderr_logfile = property( _get_stderr_logfile )
    
    def __init__( self ):
        self.__cmnd = []
        self.__Target = None
        self.__Source = None
        self._node_name = None
        return
    
    def get_num_proc( self ):
        
        numbers = [com.get_nub_proc() for com in self.getCmnd() ]
        
        return max(numbers)

    
    def getCmnd( self ):
        return self.__cmnd
    
    def get_command_list(self):
        return self.__cmnd
    
    def addCommand( self, command ):
        self.setTarget( None )
        return self.__cmnd.append( command )

    def is_muti_proc(self):
        for cmd in self.get_command_list():
            if cmd.command_type == 'multi_process':
                return True
        return False
            
    def setSource( self, src ):
        assert not self.getCmnd(), "command already has attributes to it, cannot add a source"
        self.__Source = src
        return
    
    def getSource( self ):
        return self.__Source
    
    
    def setTarget( self, tgt ):
        self.__Target = tgt
        return
    def getTarget( self ):
        return self.__Target
    
    def get_node_name(self):
        return self._node_name
    
    def set_node_name(self, val):
        self._node_name = val
        for cmd in self.get_command_list():
            cmd.node_name = val
    
    source = property(getSource, setSource )
    target = property(getTarget, setTarget )
    node_name = property(get_node_name,set_node_name )
    
    def get_targets(self):
        tgts = set()
        if self.target:
            tgts.add(self.target)
            
        for com in self.__cmnd:
            tgts.update( com._get_target_cont() )
        return tgts
    
    def make_locals_list(self):
        lst = []
        push = lst.append
        
        for com in self.get_command_list():
            push(None)
            for target in com._get_target_cont():
                if target.is_global:
                    lst[-1] = False
                    break
                else:
                    lst[-1] = True

        if lst[-1] is False:
            pass # do nothing target is already global
        elif self.target:
            # set it to the location of the stdout target
            is_local = bool( self.node_name != 'localhost' ) 
            lst[-1] = is_local

        return lst
    
    def make_tmp_list(self):
        
        lst = []
        push = lst.append
        
        for com in self.__cmnd:
            push(None)
            for target in com._get_target_cont():
                if target.istmp():
                    lst[-1] = True
                    break
                else:
                    lst[-1] = False
                    
        if self.target:
            lst[-1] = self.target.istmp()

        return lst

    def get_sources(self):
        srcs = set()
        if self.source:
            srcs.add(self.source)
        for com in self.__cmnd:
            srcs.update( com._get_source_cont() )
        return srcs

    
    def __str__( self ):
        
        format = [com.func.format( self.node_name,com.params, com.kparams ) for com in self.getCmnd()]
        
        command = " | ".join( format )
        if self.source:
            command = "< %s %s" %(self.source, command)
        if self.target:
            command = "%s > %s" %(command, self.target)
            
        return command
#        return "< %s %s > %s" %( self.getSource(), command , self.getTarget() )
      
    def __call__( self, *params, **kparams ):
        """
        runs driver with pipe. uses the list of 
        """
        return self.run()
    
    def run(self):
        
        if self.node_name is None:
            raise Exception( "job host not set" )
        
        log = self.env['record'](5,'cmd','err')
#        print >> log
#        print >> log, "command failed, running diagnostic"
#        print >> log
        try:
            self._run()
        except IOError:
            
            print >> log, "command failed, running diagnostic"
            if self.env['slimvars']['run_again']:
                if self.diagnose():
                    print >> log, "All diagnostics passed: running command again"
                    self._run()
                else:
                    print >> log, "diagnostic failed: raising exception"
                    raise
            else:
                raise
        return
            
    def diagnose(self):
        
        for source in self.get_sources():
            if not source.diagnostic(  ):
                
                return False
        
        return True
        
    def add_node_name_to_targets( self ):
        
        if self.target:
            if self.target.is_local:
                self.target.add_node_name( self.node_name )
            else:
                self.target.add_node_name( 'localhost' )
            
        for cmd in self.get_command_list():
            cmd.add_node_name_to_targets( )
        
        return

    def copy_sources(self):
        """
        recursively copy source nodes if necessary
        """

        if self.source and self.source.is_local:
            if self.is_muti_proc():
                self.source.node_copy( 'localhost' )
            else:
                self.source.node_copy( self.node_name )
            
        for cmd in self.get_command_list():
            cmd.copy_sources( )

    
    def _run(self):
        center = self.env['center']
        
        self.copy_sources( )
        
        center.acquire()
        cmd = self.pipe_format()
        
        log = self.env['record']
        print >> log(5,'cmd'), cmd
        p3 = Popen(cmd , stderr=__PIPE__ ,shell=True)
        pid = p3.pid
        center.add_pid( pid )
#        p3.tochild.close()
        center.release()
        
        try:
            err = p3.wait()
            print >> log(5), "finished::", self.node_name
            
        except OSError, e:
            if e.errno is 10:
                err = p3.returncode
            else:
                raise
        
        center.acquire()
        
        self.add_node_name_to_targets()
            
        center.remove_pid(pid)
        lines = p3.stderr.readlines()
        last_line = "".join(lines) #@UnusedVariable
        
        if err:
#            last_line = self.get_last_line_of_err_log()
            node = self.node_name #@UnusedVariable
            center.release()
            raise IOError( err, "process %(pid)s on node %(node)s, returned %(err)s: \n%(last_line)s\nCommand:%(cmd)s" % vars() ) 
        else:
            center.release()
            
            if last_line:    
                print >> log(5,'cmd','err'), last_line
                
            p3.stderr.close()
            return
        
    def pipe_format(self):
        
        #
#        clist= []
        clist = self.format()
        
        # If any target is non temp then send it to global storage      
        is_local = self.make_locals_list()
        is_tmp = self.make_tmp_list()
        
        if self.source is None:
            clist.insert(0,'true')
            is_local.insert( 0 , None )
            is_tmp.insert( 0 , None )
        
        if self.is_muti_proc():
            nodename = 'localhost'
        else:
            nodename = self.node_name
        
        source = self.source
        if source:
            source = source.get_data( self.node_name )

        target = self.target
        if target:
            target = target.get_data( self.node_name )

        pipecommand = Unix_Pipes.CreateComand( clist,
                                 node_name = nodename, 
                                 source = source, 
                                 target = target,
                                 is_local=is_local,
                                 is_tmp=is_tmp,
                                  )
        
        all_scalars = SCALAR( pipecommand )
        scalars_map = self.env['table'].scalars_map
        for scal in all_scalars:
            scalar_value = str(scalars_map[scal])
            pipecommand = pipecommand.replace(scal, scalar_value )
        
        return pipecommand
    
    
    def set_work_node(self , node_name ):
        self.node_name = node_name
        
    def format( self ):
        """
        creates a dictionary with the key "cmnd" 
        which is a string of all the 
        """
        
        cmnd = [com.func.format( self.node_name, *com.do_runtime_map() ) for com in self.getCmnd()]
        
        return cmnd
