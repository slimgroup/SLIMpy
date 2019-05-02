"""
record jobs done 
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

import time

class JobRecord( object ):
    """
    tracks time spent working on a job which node
    etc.
    """
    
    def __init__( self, job_id, node_name, node_num ):
        
        self.node_info = ( node_name, node_num )
        
        self.name = job_id
        
        self.created = 0 
        self.finished = 0
        self._crashed = False
    
    def start( self ):
        self.created = time.time()
    
    def stop_crash( self ):
        self._crashed = True
        self.stop()
    
    def stop( self ):
        self.finished = time.time()
    
    def total_time( self ):
        return self.finished - self.created    


