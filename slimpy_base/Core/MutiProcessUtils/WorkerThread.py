"""
Container classes to work on commands on separate threads
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

## 


from slimpy_base.Core.Runners.RunnerBase import Runner
from slimpy_base.Environment.InstanceManager import InstanceManager
from random import randint
from sys import _current_frames
from thread import get_ident
from threading import Thread, Lock
import traceback


printlock = Lock()

## Worker for the multi-core runner
class Worker( Thread , Runner ):
    """
    Worker runs jobs 
    """
    env = InstanceManager()
    
    def __init__( self, name, master_id , processor=0 ):
        
        self.master_id = master_id
        
        self.processor = processor
        self.env['center'].subscribe( name, processor )
        Thread.__init__( self, name=name )
        self.pid = 0
        
        self.thread_state = "init"
    
    def _get_ts(self):
        return self._thread_state
    
    def _set_ts(self,val):
        self._thread_state = val
        return 
#        print self, val
        
    thread_state = property( _get_ts, _set_ts )
    
    ## print status of thread as a traceback
    def status(self):
        """
        print status of thread
        """
        if self.isAlive():
            f = _current_frames()[self._ident]
            traceback.print_stack(f)
        else:
            print "Not Alive"
    
    def run( self ):
        '''
        run method needed by thread class
        calls self.main_loop
        '''
        self.thread_state = "running"
        self._ident = get_ident( )
        self.env.current_env = self.master_id
         
        try:
            self.main_loop()
        except Exception, msg:
#            print "worker calling error"
            self.env['center'].error = True, ( str( self ), str( msg ) )
            self.safe_release_lock()
#            print self,'Thread Terminated'
            self.thread_state = "exit error"
            raise
        
        self.thread_state = "exit"
        
        return  
        
    def safe_release_lock( self ):
        '''
        class will release the all nested locks 
        in the recursive lock 
        '''
        
        rlock = self.env['center'].lock
#        print 'owned',self,rlock._is_owned(),rlock._RLock__owner 
        if rlock._is_owned() and rlock._RLock__owner == self: #IGNORE:E1101
            
#            print 'count',rlock._RLock__count
            for _ in range( rlock._RLock__count ): #IGNORE:E1101
                rlock.release()
            return 
        else:
            return
        
        
#        print 'exit',self
    def getMyPost( self ):
        'get this workers job post'
        return self.env['center'][self.getName(), self.processor]
        
    mypost = property( getMyPost )
    
    def __str__( self ):
#        numtodo = self.mypost.has_todo()
        return "<Worker: node %s, processor %s, %%s jobs todo>" % ( self.getName(), self.processor)
    
    def print_( self, *val ):
        'print using print lock'
        
        log = self.env['record']( 10, 'thread' )
        with printlock:
            print >> log, self, " ".join( map( str, val ) )
        
        
    def main_loop( self ):
        'run until error or until done'
        center = self.env['center']
        self.thread_state = "main loop"
        
        self.thread_state = "got center"
        name = self.getName()
        proc = self.processor
        mypost = center[name, proc]
        mypost.start_timer( )
        
        with center:
                
            
            while 1:
                #wait for the signal to run an event
                self.print_( "waiting for job... " )
    
                if center.done or center.error:
                    self.print_( "Ending work term: done=", center.done, "error=", center.error )
                    mypost.stop_timer( )
                    break
                
                
                if center.has_nothing_todo( name, proc ):
                    self.thread_state = "waiting for job"
                    center.wait_for_job( name, proc )
                    self.thread_state = "finished waiting for job"
                
                
                elif mypost.has_todo():
                    self.print_( " ... working" )
                    
                    job_id = center.get_my_job( name, proc )
                    
                    self.thread_state = "running job"
                    
                    center.release( )
                    self.run_job( job_id )
                    center.acquire( )
                    
                    self.thread_state = "finished running job"
                    
                    center.finished( name, proc, job_id )
                    self.print_( " ... finished" )
                else:
                    center[name, proc].event.clear()
            
    def run_job( self, job_id ):
        '''
        run a job
        '''
        
        name = self.getName()
        proc = self.processor
        ri = randint( 1, 5 )
        
        if not isinstance( job_id, tuple ):
            raise TypeError( "job_id should be a tuple" )
        
        table = self.env['table']                    
        items = [ table[item] for item in job_id]
        # add commands returns a runnable object
        # 'runnable' and a datacontainer 'target'
        job = self.add( items )

        
        # set the data to the result of running the command
        with printlock:
            log = self.env['record']( 1, 'runner' )
            print >> log, '%(name)s-%(proc)d ::' % vars(), job.nice_str()
        
        center = self.env['center']
        if self.env['slimvars']['runtype'] == 'dryrun':
            pass
        else:
            num_proc = job.num_proc
            if num_proc == 'all':
                num_proc = center.semaphore._initial_value
                
            for i in xrange(num_proc): 
                if center.semaphore._Semaphore__value == 0:
                    num = num_proc - i
                    print "waiting for %s more proccesors" %num
                if center.error:
                    return
                center.semaphore.acquire( )
                
            
            job.node_name = self.getName()
            
            for i in xrange(num_proc): 
                center.semaphore.release( )
            job.run()

    
