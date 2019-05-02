"""
runner for many processors on the same CPU
"""
from __future__ import with_statement

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


from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.Core.MutiProcessUtils.WorkerThread import Worker
from slimpy_base.Core.Runners.PresidenceStack import presStack
from slimpy_base.Environment.InstanceManager import InstanceManager
from threading import ThreadError
from threading import currentThread
import pdb

class MultiCoreRunner( presStack ):
    """
    Runs commands from the graph. uses two stacks to keep 
    track of dependencies and perhaps run several commands 
    at the same time.
    """
    env = InstanceManager()
    
    
    def __init__( self ):
        
        self.created_nodes = set()
        self.nodes = None
        presStack.__init__( self )
        
    def set_graph(self, graph):
        """
        runner.set_graph( graph )
        sets the graph to graph 
        """
        presStack.set_graph( self, graph )
        center = self.env['center']
        center.reset()
        
        self.nodes = { }
        
        if len( center.node_names ) == 0:
            raise Exception("No nodes to work on")
            
        for nodename in center.node_names:
            
            proc_list = self.nodes.setdefault(nodename,[])
            ppn = len(proc_list)
            
            worker = Worker( nodename, self.env.current_env, processor=ppn )
            proc_list.append( worker )
            
        center.set_event( )
                
        assert not center.done

    def run(self):
        """
        required by Thread
        """
        center = self.env['center']
        
        try:
            self.main_loop()
        except Exception, msg:
            center.error = True, msg
            
            self.safe_release_lock()
            center.abort_all( )
            
            self.join_all()
            raise
        
        self.join_all( )
        center.reset()
    
    def join_all(self):
        """
        Wait for all to finish
        """
        
        
        for node in self.nodes.values():
            for processor in node:
                if processor.isAlive():
                    processor.join()
        return 
                    
    def check_if_job_is_cmd( self, job_id ):
        """
        The job is a command or data 
        """
        if isinstance( job_id, tuple ):
            return job_id
        else:
            self.created_nodes.add( job_id )
            self.pop( job_id )
            self.env['center'].set_event()
            return None
    
    def safe_release_lock(self):
        
        this = currentThread()
        rlock = self.env['center'].lock
        
        while rlock._is_owned() and rlock._RLock__owner == this: #IGNORE:E1101
            rlock.release( )

    
    def __str__(self):
        num_nodes = len(self.nodes)
        num_proc  = sum( map( len, self.nodes.values()) )
        ready = self.has_ready()
        working = self.num_working()
        return ( "<MutiCoreRunner %s nodes, "
                                 "%s processors, "
                                 "%s ready, "
                                 "%s working>" 
                 % (num_nodes, num_proc,ready,working ) )
    
    def has_work_and_worker(self):
        rdy = self.has_ready()
        idle = self.env['center'].has_idle()
        return  ( rdy and idle )
    
    def have_no_work_or_workers(self):
        nothing_to_do  = not self.has_ready()
        nothing_to_do |= not self.env['center'].has_idle()
        return nothing_to_do
    
    
    def main_loop(self):
        

        log = self.env['record']
        logt = log(10,'thread')
        
        for node in self.nodes.values():
            
            for processor in node:
                print >> logt,"starting",node,processor
                processor.start()
    
        
        with self.env['center'] as center:
            
            while self.has_more_jobs():
                
                print >> logt ,self, "has more jobs and is waiting"

                if self.have_no_work_or_workers():
                    center.wait_for_avail( )
                
                if center.error:
                    raise ThreadError( "Another thread signaled error" )
                
                for job_id in center.dump_finished():
                    self.pop( job_id )
    
                
                # while there are jobs to do and workers to do them
                # assign a worker some work 
                while self.has_work_and_worker():
                    
                    job_id, (node, proc) = self.choose( )
                    
                    
                    if job_id:
                        
                        self.pull( job_id )
                        # posting a job also calls "notify" on the thread waiting for 
                        # a job to do
                        print >> log(10,'thread') ,self, "posting job"
                        center.post(node, proc, job_id)
                        
                # Finished Posting jobs
            # End with center
                
            print >> log(10,'thread') ,self, "is done!!!!!"
            # Tell all that no more jobs are being posted
            center.done = True
#            pdb.set_trace()
#            self.nodes['localhost'][0].status
        return 
    
    @classmethod
    def get_src_from_id(cls,job_id):
        jlist = [ cls.env['table'][jid] for jid in job_id]
        
        srcs = []
        if isinstance( jlist[0], DataContainer ):
            srcs.append( jlist[0] )
        
        sc = lambda job: job.source_containers
        hc = lambda job: hasattr( job, 'source_containers' )
        slist = [ sc(job) for job in jlist if hc(job) and sc(job) ]
        
        map( srcs.extend , slist )
        
        return srcs
        
        
    def choose(self):
        
        while self.has_ready_data():
            data_id = self.pull_data()
            self.created_nodes.add( data_id )
            self.pop( data_id )
            
            
        cmds = [ key for key in self.ready.keys() if isinstance( key, tuple) ]
        
        if cmds:
            center = self.env['center']
            idle = center.idle
            nodelist = [ node for node,_ in idle ]
            jid, node = self._choose_node_command( cmds, nodelist )
            proc = None
            for n,p in idle:
                if n == node:
                    proc = p
                    break
        else:
            jid, (node, proc) = None,(None,None)
        
        self.env['center'].set_event( )
        
        
        return jid, (node, proc)
            
    @classmethod
    def _choose_node_command(cls, job_ids, nodelist ):
        res = []
        for job_id in job_ids:
            datalist = cls.get_src_from_id(job_id)
            r2 = []
            for p in nodelist:
                hits = len([ 1 for data in datalist if p in data.nodenames])
                miss = len( datalist ) - hits
                r2.append( (job_id,p,(hits,miss)) )
            r2.sort( mycmp )
            res.append( r2[0] )
            
        res.sort( mycmp )
        return res[0][:2]

    

def mycmp(x,y):
    ( _,_, ( hits1, miss1 ) ) = x
    ( _,_, ( hits2, miss2 ) ) = y
    cmp_miss = cmp( miss1, miss2 )
    if cmp_miss == 0:
        return  cmp(  hits2, hits1 )
    else:
        return cmp_miss 

