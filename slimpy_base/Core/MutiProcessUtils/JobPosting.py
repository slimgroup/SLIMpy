'''
posting class for worker threads to get info about new jobs
'''


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

from threading import RLock,Event
from slimpy_base.Core.MutiProcessUtils.JobRecord import JobRecord
from slimpy_base.Environment.InstanceManager import InstanceManager
import time

class JobPosting( object ):
    '''
    posting class for worker threads to get info about new jobs
    Like a message board.
    '''
    env = InstanceManager()
    
    def __init__( self, name, processor ):
        
        self.lock = RLock()
        self.event = Event()
        self.lock.acquire()
        
        self.name = name
        self.processor = processor
        self.finished_jobs = set()
        self.current = set()
        self.todo = set()
        self._is_waiting = False
        
        self._first_wait = True
        self.start_time = 0
        self.stop_time = 0
        self.current_rec = None
        self.finished_rec = set()
        
        self.lock.release() 
    
    def _get_waiting(self):
        'true if worker is waiting for a job'
        return self._is_waiting
    
    def _set_waiting(self,val):
        self._is_waiting = val
        
    waiting = property( _get_waiting, _set_waiting )
    
    def get_time_since_start(self):
        'get the time from the start of the job'
        if self.current_rec is None:
            return 0
        else:
            return time.time() - self.current_rec.created
    
    time_passed = property( get_time_since_start )
    
    def notify(self):
        'notify the listening worker'
        self.event.set()
        
    def new_todo( self, job ):
        'add a job to the message board'
        self.lock.acquire()
        self.todo.add( job )
        self.lock.release()
        
    def get( self ):
        'get a job from the todo pile'
        self.lock.acquire()
        job = self.todo.pop()
        self.current.add( job )
        self.current_rec = JobRecord( job ,self.name, self.processor)
        self.current_rec.start()
        
        self.env['record'].add_job( self.current_rec )
        
        self.lock.release()
        return job
    
    def finished( self, job ):
        '''
        adds current job to the finished pile
         
        '''
        self.lock.acquire()
        self.current.remove( job )
        self.finished_jobs.add( str(job) )
        
        rec = self.current_rec
        rec.stop()
        self.finished_rec.add( rec )
        print >> self.env['record'](10,'time'), "Command execution time: %0.4f seconds" %(rec.finished-rec.created) 
        self.current_rec = None
        
        self.lock.release()
    
    def is_working( self ):
        'true if the worker is working on a job'
        return len( self.current )
    
    def has_todo( self ):
        'returns the len of the todo pile'
        return len( self.todo )
    
    def busy( self ):
        'true if job is working or has stuff todo'
        self.lock.acquire()
        ret = self.is_working() or self.has_todo()
        self.lock.release()
        return ret
    
    def post(self,job):
        'post a job to the todo'
        self.lock.acquire()
        
        self.todo.add( job )
        self.event.set()
        
        self.lock.release()
        
    def start_timer(self):
        'starts timer '
        self.start_time = time.time()

    def stop_timer(self):
        'stops timer '
        self.stop_time = time.time()

    def wait_for_job(self):
        "wait for slef.notify to be called"
        self.event.wait()
        self.event.clear()
        return
    
    def acquire(self):
        self.lock.acquire()
        
    def release(self):
        self.lock.release()
        
    def total_time(self):
        "total time between start and stop"
        return self.stop_time - self.start_time
    
    def time_idol(self):
        'total time spent idle'
        tot = self.total_time()
        for jobrecord in self.finished_rec:
            tot -= jobrecord.total_time()
        return tot
    
