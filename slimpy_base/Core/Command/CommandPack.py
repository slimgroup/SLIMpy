"""
Helper Class to store values destined for the graph
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


from slimpy_base.Core.Interface.node import Node

    
class CommandPack( object ):
    """
    Class to contain commands sources and targets for
    convenience
    
    """
    def __init__( self, comm, in_cont=True, out_cont=True ):
        
#        assert out_cont is place_holder or out_cont is None
#        assert in_cont is place_holder or in_cont is None
        self.in_cont = in_cont
        self.out_cont = out_cont
        self.commlist = comm
    
    def getNodeList( self ):
        """
        returns the commands as a list of Node instances
        """
        return [ Node( node ) for node in  self.commlist ]
    
    def getTargets( self ):
        """
        return a list of all of the targets in the 
        commands
        """
        targets = []
        for comm in self.commlist:
            targets.extend( comm.getTargets() )
        return targets

    def getSources( self ):
        """
        return a list of all of the sources in the 
        commands
        """
        sources = []
        for comm in self.commlist:
            sources.extend( comm.getSources() )
        return sources
    
    
    def getSourceNode( self ):
        """
        returns main source as a Node instance
        """
        return Node( self.in_cont )
     
    def getTargetNode( self ):
        """
        returns main target as a Node instance
        """
        return Node( self.out_cont )

    def getSource( self ):
        """
        returns stdin source
        """
        return self.in_cont

    def setSource( self, src ):
        'sets stdin source'
        if self.source is True:
            self.in_cont = src
        elif self.source is None and src is not None:
            com = self.commlist[-1]
            if com.has_unusedsource():
                com.setunusedsource( src )
                return
            else:
                raise Exception(
                             'CommandPack instance initialized with stdin=None.\n'
                             'Need "Source" class object in the command as a placeholder.\n'
                             '\t(i.e) Command["somval"] = Source ' )
        return 

    
    def getTarget( self ):
        'returns stdout target'
        return self.out_cont

    def setTarget( self, tgt ):
        'returns stdout target'
        if self.target is True:
            self.out_cont = tgt
            
        elif self.target is None and tgt is not None:
            com = self.commlist[-1]
            if com.has_unusedtarget():
                com.setunusedtarget( tgt )
                return
            else:
                raise Exception( 'target has not been set '
                             'could not set stdout target and \n'
                             'no target was found in the command')
                
        return 

    source_node = property( getSourceNode )
    target_node = property( getTargetNode )
    source = property( getSource, setSource )
    target = property( getTarget, setTarget )
    

