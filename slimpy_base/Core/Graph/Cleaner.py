"""
contains a cleaner class that tracks dependencies and removes
any data that is no longer in use and has no unmet dependencies
"""
import pdb

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

#from slimpy_base.utils.hashTable import HashTable
#from slimpy_base.utils.Logger import Log

from slimpy_base.Environment.InstanceManager import InstanceManager


class cleaner( object ):
    """
    cleaner cleans the graph of obsolete data, cleaner 
    does not necessarily have to remove dead branches from
    the graph but the data that the nodes point to.
    """
#    table = HashTable()
    env = InstanceManager()
#    log = Log()
    
    def __init__( self, graph, depth=1 ):
        """
        cleaner instance takes a graph and a depth 
        """
        self.graph = graph
        self.depth = depth
        self.__source = {}
        self._stored = set( [] )
        
        self._cleaned = set()
        
    def clean( self, node ):
        """
        usage: Call clean on a node after the node is finished
        adds the dependencies of node to the list of sources by calling add source.
        once all of ...
        """

        for nondep in self._stored.copy():
            #print "#### ==> here", nondep
            self.remove( nondep )
        
        log = self.env['record']
        print >> log( 10, 'cleaner' ) , "clean called on node %(node)s" %vars()

        for prev in self.graph.invAdj( node ):
            #print 'prev',prev
            self.addSource( prev )
    
    def addSource( self, node ):
        """
        Add a source node to the cleaner.
            
        compares the number of nodes to how many times 
        node has been added to the cleaner.
        for example:
            let  a subset of a graph be:
                data1 -> command1
                data1 -> command2
            then the number of nodes data1 depends on is 2
            when command1 is finished processing Cleaner.Clean(command1) will be called
            and Cleaner.Clean(command2) will be called after command2 is finished with
            each time Cleaner.addSource(data1) is called
            so on the call of Cleaner.Clean(command2) data1 will be removed
            by using the method Cleaner.remove(data1)
        """
        
        dep = len( self.graph.adj( node ) )
        
        num = self.__source.get( node , 0 )
        
        num += 1
        
        self.__source[node] = num
        
        if num >= dep:
            
            self.remove( node )
            self.__source[node] = 0
            
    def remove( self, node ):
        """
        removes node only if the reference count of node is 1
        
        """

        if isinstance( node, tuple ) :
            return
        
        table = self.env['table']
        slimvars = self.env['slimvars']
        log = self.env['record']( 10, 'cleaner' )
        log2 = self.env['record']( 1, 'cln' )
        refcount = table.getRef( node )
        if refcount:
            print >> log, 'Cleaner: NOT removing node,\nnode still active refcount=%(refcount)s' %vars()
#            obj = self.table[node]
#            import gc
#            print >> self.log( 10, 'cleaner' ), gc.get_referrers(obj)
            self._stored.add( node )
            return False
        elif table.has_active_referers( node ):
            print >> log, 'Cleaner: NOT removing node,\nnode still has active referrers' %vars()
            self._stored.add( node )
            return False
        else:
            self._stored.discard( node )
            item = table[node]
            
            print >> log, 'Cleaner: removing node', item , 'refcount=',refcount
            
#            table.removeSource( node )
            self._cleaned.add( node )
        
        if not slimvars['no_del']:
            try:
                print >> log2, "Cleaner Removing", item
#                if '00013' in str(item):
#                    pdb.set_trace()
                
                item.remove()
            except AttributeError: #IGNORE:W0704
                pass

        return True
            
    def get_cleaned_nodes(self):
        return self._cleaned
            
def all( func, iterable ):
    """
    returns true if all values in iterable
    evaluate to True
    @param iterable: list 
    """
    
    val = True
    for x in iterable:
        val = func( x ) and val
    return val

