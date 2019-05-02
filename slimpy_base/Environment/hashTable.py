"""
HASHTABLE CLASS
contains all active and nonactive nodes ever made
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

from slimpy_base.Environment.Singleton import Singleton
from atexit import register as __register__

from slimpy_base.Environment.InstanceManager import InstanceManager
from sys import getrefcount


class _HashTable( Singleton ):
    """
    Basic hash table (same as __builtin__.dict)
    
    """
    env = InstanceManager()
    
    def __new_instance__( self , name ):
        
        Singleton.__new_instance__(self, name)
        self._hash = {}
        self._scalars = {}
        self._no_clean = False
        #===============================================================================
        # Make sure that at exit the clean function is set
        #===============================================================================
        __register__( self.clear_at_exit )
    
    def __len__(self):
        return len( self.getHash() )
    
    def has_key( self, k ):
        return self.getHash().has_key(k)
    
    def has_active_referers( self, node_id ):
        
        datacontainer = self[node_id]
        if not hasattr(datacontainer,'referrers'):
            return False
        
        for ref in datacontainer.referrers:
            if self[ref].isfull():
                return True
            
        return False
    
    def __clean__( self ):
        self.clear()
    
    def _do_not_clean(self):
        self._no_clean = True
    
    def get_scalars_map(self):
        return self._scalars
    
    scalars_map = property( get_scalars_map )
    
    def getHash( self ):
        return self._hash
    
    def _get_table( self ):
        return self._hash
    
    def _set_table(self,table):
        self._hash = table
    
    _map = property( _get_table, _set_table)
        
    def __getitem__( self, item ):
        
        try:
            
            return self.getHash().__getitem__( item )
        except KeyError, msg:
            
            raise KeyError, msg
    
    def __setitem__( self, item, val ):
        return self.getHash().__setitem__( item, val )
    
    def items( self ):
        
        return self._map.items()
    
    def values( self ):
        return self._map.values()
        
    def __str__( self ):
        s = "<Table{'%(i_name)s'}: %(elements)s elements, %(active)s active>"
        i_name = self._instance_name
        active = len(self.getActiveSet())
        elements = len(self.getHash())
#        sources = len( self.getSources() )
        
        return s %vars()

    def __repr__( self ):
                
        return self.__str__()
    
    def __contains__(self,item):
        return self._map.__contains__( item )
    
    def append( self, item ):
        """
        appends item to the hash table
        @Returns the id of item 
        """
        itemID = id( item )
        self._map[itemID] = item
        return itemID
    
    def getActiveSet( self ):
        return [item[0] for item in self.items() if getrefcount( item[1] ) > 3 ]
    
    def clear_at_exit( self ):
        """
        same as clear
        """
        self.clear()
    
    def clear( self ):
        """
        for each item in the graph try to remove it
        """
        if self._no_clean:
            return
        
        log = self.env['record']( 10, 'cleaner' )
        print >> log , "clear all called"
        from slimpy_base.Core.Interface.ContainerBase import DataContainer
        
        for node in self.values():
            
            # if the node is a data container try to remove it 
            if isinstance( node , DataContainer ):
                # note: that the remove call only removes
                # data that are there and not temporary
                data = node.data
                print >> log , "removing %(data)s" %vars()
                node.remove()

        self._map.clear()
#        self.getSources().clear()
        
    def getRef( self, item ):
        """
        returns the refrence count of the value that item 
        points to
        """
        return getrefcount( self[item] )-2

    def printHash( self ):
        """
        Prints a formated output of the hash table
        """
        log = self.env['record']
        
        print >>log, "     ID    | ref |  Value"
        print >>log, '-----------+-----+------------'
        for item in self.items():
            print >> log, "%10d | %03d | %s" %( item[0], getrefcount( item[1] )-2, item[1] )
            
#    def addSource( self, src  ):
#        """
#        add a source to a global list of sources
#        """
#        self.sources.add( src )
#
#    def isSource( self, item ):
#        """
#        query whether a source is in the global sources
#        is check is true ...
#        check not implemented
#        """
#        val = item in self.getSources(  )
#        return val
    
#    def getSources( self ):
#        """
#        get all of the sources fron the set of sources
#        if keys then will return the set of keys
#        else will return the set of values
#        """
#        
#        return self.__sources
#        
#        
#    
#    sources = property( getSources )
        
    def removeSource( self, src ):
        """
        remove a node from the set of sources
        """
#        self.getSources().remove( src )
            
