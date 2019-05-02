"""
Base class for all runner subclasses 
needed by the GraphManager
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


#from slimpy_base.utils.Logger import Log

#from slimpy_base.utils.hashTable import HashTable
#from slimpy_base.utils.GraphManager import GraphManager
#from slimpy_base.utils.GlobalVars import GlobalVars

from slimpy_base.Environment.InstanceManager import InstanceManager
from pdb import set_trace

class Runner( object ):
    """
    Abstract class
    """
#    log = Log()
    env = InstanceManager()
    cleaner = None
    created_nodes = None
    
    def set_graph(self,graph):
        raise NotImplementedError("Please use a subclass of RunnerBase")

#    def addSource(self, source):
#        """
#        add a source to the graph manager
#        """
#        self.env['graphmgr'].addSource(source)
        
    def add(self, commands):
        """
        simple helper function
        TODO: replace with reduce( lambda x,y:y+y,commands)
        """
        commands = list( commands )
        prev = commands.pop(0)
        if not commands:
            if prev.adder is None:
                return prev
            else:
                return prev + None
            
        while commands:
            next = commands.pop(0)
            prev = prev + next
            
        return prev

    def get_new_sources(self):
        if self.cleaner is None:
            cleaned_nodes = set()
        else:
            cleaned_nodes = self.cleaner.get_cleaned_nodes()
            
        if self.created_nodes is None:
            remaining = set()
        else:
            remaining = self.created_nodes.difference( cleaned_nodes )
        
        return remaining
