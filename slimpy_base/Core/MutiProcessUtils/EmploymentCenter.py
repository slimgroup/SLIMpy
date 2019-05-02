"""
Central thread scheduler info center a common ground for 
Worker nodes and main scheduler node to sync 
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



from slimpy_base.Core.MutiProcessUtils.JobPosting import JobPosting
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Environment.Singleton import Singleton
from os import kill
from os.path import isfile
from signal import SIGALRM, alarm, signal, SIGKILL
from threading import RLock, Event, BoundedSemaphore
from time import sleep
from pdb import set_trace
from threading import currentThread
import pdb
import sys


def action( signum, stack_frame ):
    '''
    action to catch alarm
    '''
    print
    print "WallTime exceded"
    print
    env = InstanceManager()
    env['center'].error = True

# set alarm to signal EmploymentCenter().error
signal( SIGALRM, action )

class EmploymentCenter( Singleton ):
    """
    Singleton class to store the state of the multi core runner
    communicates with the workers and scheduler
    """
    
    def __new_instance__( self, name ):
        '''
        create a new instance
        '''
        Singleton.__new_instance__( self, name )
        
        self.lock             = RLock()
        
        with self:
            self._jobs_posted = 0
            self._jobs_finished = 0
            self._done = False
            self._error = False
            self._error_message = None
            self._pids            = set()
            self._aborted_pids    = set()
            self._waiting_list    = set()
            self._event           = Event()
            self.__node_names     = [ ]
            self.nodes            = {}
            self._idle            = set()
            self._fin             = set()
            self._head_node       = ( "__main__", "__main__" )
            
            self.env              = InstanceManager()
        
        self._semaphore = None
        
    def _get_semaphore(self):
        if self._semaphore is None:
            self._semaphore = BoundedSemaphore( len(self.node_names) )
        return self._semaphore
    
    semaphore = property( _get_semaphore )
           
    def reset( self ):
        '''
        set self.done and self.error to false
        '''
        self.done = False
        self.error = False
    
    def set_alarm( self ):
        '''
        set the alarm for the amount of time 
        walltime given minus the time of the
        longest running job 
        '''
        with self:
            if self._jobs_posted == self._jobs_finished:
                aval = 0
            else:
                max_time = 0
                walltime = self.env['slimvars']['walltime']
                for procs in self.nodes.itervalues():
                    for proc in procs.itervalues():
                        time_passed = proc.time_passed
                        if time_passed > max_time:
                            
                            max_time = int( time_passed )
                    aval = walltime - max_time 
            
            log = self.env['record']
            print >> log( 2, 'alarm' ), "alarm set for", aval 
            alarm( aval )
        return 
             
    def add_to_waiting_list( self, name, proc ):
        """
        add a worker to wait for a job from the 
        scheduler
        """
#        self.acquire()
#        print "adding ",name,proc,"to waiting list"
        self._waiting_list.add( ( name, proc ) )
#        print "wl",self._waiting_list
        if self._head_node in self._waiting_list:
            all = set( [self._head_node] )
            for name, val in self.nodes.iteritems():
                for proc in val.iterkeys():
                    all.add( ( name, proc ) )
            assert all.issuperset( self._waiting_list )
            if all == self._waiting_list:
                pass
#                raise ThreadError( "all threads locked %s == %s" %( all, self._waiting_list ) )
        else:
            pass
#        self.release()
        return  
        
    def remove_from_waiting_list( self, name, proc ):
        """
        remove a worker from the waiting_list 
        """
#        print "removing ",name,proc,"from waiting list" 
        self._waiting_list.remove( ( name, proc ) ) 
#        print "wl",self._waiting_list

    def add_pid( self, pid ):
        """
        add the pid of a running job to the 
        set of pids so they may be killed upon
        error  
        """
        with self:        
            self._pids.add( pid )
    
    def remove_pid( self, pid ):
        """
        remove a pid from set
        """
        with self:
#            pdb.set_trace()
            self._pids.remove( pid )
    
    def abort_all( self, kill_signal=SIGKILL ):
        """
        abort all of the pids of working jobs by the 
        kill command 
        """
        log = self.env['record']( 1, 'thread' )
        print >> log , "Abort All:"
        with self.lock:
            print >> log, 'killing', self._pids
            for pid in self._pids.copy():
                try:
                    kill( pid, kill_signal )
                except OSError:
                    pass
                else:
    #                print "no such process"
    #                print "abbort successful"
                    print >> log , "removing" , pid 
                self.remove_pid( pid )
                
        return
        
    def _set_error( self, val ):
        """
        set the error value
        if true then all listeners will be notified
        """
        log = self.env['record'](2,'err')
        with self:
            if isinstance( val, tuple ):
                msg = val[1]
                val = val[0]
            else:
                msg = None
                
            self._error_message = msg
            
            if val and not self._error: #IGNORE:E0203 access to _error befor defined: defined in __shared_state 
                print >> log, "Fatal Error Occured, Waiting for all nodes to finish", str( msg )
                self.set_event()
                self.notify()
                
    #        elif not val:
    #            print >> sys.stderr, "Resetting Thread error"
            self._error = val
        
        
    def _get_error( self ):
        """
        True if error occurred
        """
        return self._error    
    
#    def _set_nodenames(self,val):
#        self.__class__.__node_names = val
    
    def _get_nodenames( self ):
        """
        retuns a list of nodenames from
        slimvars['NODELIST'] or slimvars['NODEFILE'] 
        """

        if 'NODELIST' in self.env['slimvars']:
            node_list =self.env['slimvars']['NODELIST']
        else:
            node_list = None
            
        if node_list:
            assert isinstance( node_list, ( list, tuple ) )
            return self.env['slimvars']['NODELIST']
        
        elif self.env['slimvars']['NODEFILE']:
            PBS_NODEFILE = self.env['slimvars']['NODEFILE']
            if isfile( PBS_NODEFILE ):
                
                lines = open( PBS_NODEFILE , 'r' ).read()
                nodes = str.split( lines ) 
#                num_nodes = len( nodes ) 
                self.env['slimvars']['NODELIST'] = nodes
                return nodes
            else:
                raise EnvironmentError( "nodefile '%s' does not exist" %PBS_NODEFILE )
#                self.env['slimvars']["np"] =  num_nodes
        else:
            raise Exception( "no nodefile or nodelist" )

        
#        return self.__node_names
    
    def idle_add( self, name, proc ):
        """
        add idle worker
        """
        self._idle.add( ( name, proc ) )
        
    def idle_discard( self, name, proc ):
        "discard worker from idle"
        
        self._idle.discard( ( name, proc ) )
    
    def set_event( self ):
        "notify schedular"
#        print "event is set"
        self._event.set()
        
    node_names = property( _get_nodenames )
    error = property( _get_error, _set_error ) 
        
    def wait_for_avail( self ):
        """
        wait for  center.set_event()
        """
        self.release( )
        
        self.add_to_waiting_list( "__main__", "__main__" )
        while not self._event.isSet():
            sleep( 0.01 )
            
        self.remove_from_waiting_list( "__main__", "__main__" )
        self._event.clear()
        
        self.acquire( )
        
        return
        
    
    def wait_for_job( self, name, proc ):
        """
        non synchronous: worker node  wait for job to be posted or error 
        """
        self.release( )
        
        mypost = self[name, proc]
        if mypost.event.isSet():
            pass
        else:
            self.add_to_waiting_list( name, proc )
            mypost.wait_for_job( )
            self.remove_from_waiting_list( name, proc )
            
        self.acquire( )
        
        return
            
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__( self, t, v, tb ):
        
        if self.lock._RLock__owner != currentThread( ):
            pass
        else:
            self.release( )
        return
    
    def subscribe( self, name, processor ):
        """
        subscribe worker to the jobs list
        """
        with self:
        
            procs = self.nodes.setdefault( name , {} )
            procs[processor] = JobPosting( name, processor )
            self.idle_add( name, processor )
                
    def _set_done( self, val ):
        """
        notify all that all jobs are done
        """
        self._done = val
        self.notify()
    
    def _get_done( self ):
        """
        returns True if scheduler is done 
        """
        return self._done
    
    done = property( _get_done , _set_done )
    
    def notify( self, nodename=None, processor=None ):
        """
        if nodename and processor are not None set then notify that 
        worker, otherwise notify all
        """
        
        with self:
        
            if nodename is None:
                for node in self.nodes.values():
                    for processor in node.values():
                        processor.notify()
            else:
                node = self[nodename, processor]
                node.notify()
            
        return
    
    def finished( self, name, processor, job ):
        """
        add a job to the finished list and
        add a worker to the idle set 
        notify the scheduler
        """
        with self:
            self._fin.add( job )
            self[name, processor].finished( job )
            self.idle_add( name, processor )
            self.set_event()
            self._jobs_finished += 1 #IGNORE:E1101
            
            self.set_alarm()
    
    def dump_finished( self ):
        """
        return all finished jobs
        """
        with self:
            ret = self._fin
            self.__class__._fin = set()

        return ret
    
#    def add_node( self, name ):
#        self.lock.acquire()
#        self.nodes.setdefault( name, WorkNode )
#        self.lock.release()
        
    def __getitem__( self, ( name, processor ) ):
        """
        return a worker's job posting from name,processor
        """
        with self:
        
            node = self.nodes[name][processor]
        
        return node
    
    def post( self, name, processor, job ):
        """
        post a job to the job posting for the  
         (name, processor) worker node
        """
        
        with self:
        
            self[name, processor].post( job )
            self.idle_discard( name, processor )
            self._jobs_posted += 1 #IGNORE:E1101
            self.set_alarm()
        
    
    def has_idle( self ):
        """
        returns true if the idle set is
        non empty
        """
        with self:
            ret = len( self._idle )
        return ret
    
    def pop( self ):
        '''
        pop a (name, proc) pair from the idle list
        '''
        with self:
        
            name, proc = list( self._idle.__iter__().next() )
        
        return name, proc
    
    def _get_idle(self):
        
        return self._idle
    
    idle = property( _get_idle )
    
    def acquire( self ):
        """
        acquire self.lock
        """
        self.lock.acquire()
        
    def release( self ):
        'release self.lock'
        if self.lock._RLock__owner != currentThread( ):
            raise Exception("cannot wait: this thread does not own lock")
        self.lock.release()
        
        
    def prettyprint( self ):
        """
        print info to screen
        """
        d_spacer = "+".join( ['-'*20]*5 )
        eqspacer = "+".join( ['='*20]*5 )
        
        print "*"*22
        print "<Current Job Postings>"
        print len( self._idle ) , "processors are idle"
        print eqspacer
        
        catagories = ['*Name*', '*Event*', '*doing*', '*todo*', '*finished*']
        title = "|".join( [ s.center( 20 ) for s in catagories] )
        print title
        print d_spacer
        
        
        for node in self.nodes.values():
            for proc in node.values():
                print self.format_poc( proc )
                print d_spacer
        print eqspacer
               
    def format_poc( self, proc ):
        l = []
        
        push = l.append
        push( proc.name )
        push( proc.event.isSet() )
        doing = map( str, list( proc.current ) )
        if proc.current:
            push( str( list( proc.current )[0] ) )
        else:
            push( 'None' )
            
        num_todo = len( proc.todo ) 
        if num_todo > 0:
            tdstr = list( proc.todo )[0]
            if num_todo > 1:
                tdstr = tdstr+' ...'
            push( tdstr )
        else:
            push( 'None' )

        push( len( proc.finished_jobs ) )
        return "|".join( [ str( s ).center( 20 ) for s in l] )
    
    def display_stats( self ):
        '''
        display stats of finish scheduler
        '''
        col_space = 20
        d_spacer = "+".join( ['-'*col_space]*5 )
        eqspacer = "+".join( ['='*col_space]*5 )
        catagories = ['*Node Name*', '*Num Jobs*', '*Total Time*', '*Time Idle*', '*Utility*']
        title = "|".join( [ s.center( col_space ) for s in catagories] )
        
        print "*"*col_space
        print "Job Post Stats"
        print eqspacer
        print title
        num_jobs = 0
        totaltime = 0
        totalidol = 0
        
        for node in self.nodes.values():
            for proc in node.values():
                print d_spacer
                nj, tt, ti, out = self.pocstat( proc )
                num_jobs += nj
                totaltime += tt
                totalidol += ti
                print out
        print d_spacer
        
        print "|".join( [ str( s ).center( col_space ) for s in
                             ['Total', 
                              "%d" % num_jobs, 
                              "%.2f" % totaltime, 
                              "%.2f" % totalidol, 
                              "%.2f %%" % ( ( 1 - totalidol/totaltime )*100 ) ]] )
        print eqspacer
               
    def pocstat( self, proc ):
        ls = []
        push = ls.append
        
        push( proc.name +":" +str( proc.processor ) )
        nj = len( proc.finished_rec )
        push( nj )
        tt = proc.total_time()
        push( "%.2f sec" %  tt )
        ti = proc.time_idol()
        push( "%.2f sec" % ti )
        push( "%.2f %%" %( 100 - proc.time_idol() / proc.total_time() *100 ) )
        
        return nj, tt, ti, "|".join( [ str( s ).center( 20 ) for s in ls] )
    
    def get_my_job( self, name, proc ):
        'returns the job of a worker'
        with self:
            job_id = self[name, proc].get()
        return job_id
    
    def has_todo( self, name, proc ):
        """
        true if there is a job waiting for the (name,proc) worker
        """
        with self:
            val = self[name, proc].has_todo()
        return val
    
    def has_nothing_todo( self, name, proc ):
        '''
        returns 'not has_todo'
        '''
        return not self.has_todo( name, proc )
    
    
    
