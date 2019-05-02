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

from slimpy_base.Core.Interface.PSpace import PSpace
from slimpy_base.Core.Interface.Structure import Structure
from slimpy_base.Core.User.Structures.serial_vector import Vector
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace


class VectorSpace( PSpace, Structure ):
    """
    PSpace type that knows about vectors 
    Class to track metadata of @ref slimpy_base.Core.User.Structures.serial_vector.Vector "Vector" objects  
    @ingroup userclasses
    """
    def testCommand( self, cmd, *args, **kargs ):
        """
        returns the resulting space from applying the command 
        but does not add the command to the graph
        @return new VectorSpace
        """
        new_space = Structure.testCommand( self, cmd, *args, **kargs )
        assert new_space is not None
        
        if isinstance(new_space, MetaSpace):
            return new_space.copy()
        else:
            return self.__class__( new_space )

    def create( self, out=0 ,istmp=None ):
        """
        space.create( self, out=0 ,istmp=None ) -> vector
        Create a vector within this vectorspace
        where the following evaluates to True: 
        @code
            >>> vector in space
        @endcode 
        
        @return Vector
        """
        param = self.copy( )
        param.pop( 'out', None )
        
        command = self.generate_command( "create", out=out, **self.params )
        # empty data container 
        
        data_container = self.makeContaner( command=command ,tmp=istmp)
        
        converter = data_container.get_converter( command )
        
        commpack = converter.convert( None, command )
        
        commpack.target = data_container
        commpack.source = None
        
        self.env['graphmgr'].graphAppend( commpack )
        
        return Vector( data_container )

    def noise( self, mean=0, seed=None, var=None ):
        """
        Create a vector within this vector space
        @param mean mean value of the noise
        @param seed random seed
        @param var variance 
        """
        param = self.copy( )
        param.pop( 'out', None )
        
        param.update(mean=mean)
        if seed is not None:
            param.update(seed=seed)
        if var is not None:
            param.update(var=var)
        
        command = self.generate_command( "create_noise",  **param.params )
        # empty data container 
        
        data_container = self.makeContaner( command=command )
        
        converter = data_container.get_converter( command )
        
        commpack = converter.convert( None, command )
        
        commpack.target = data_container
        commpack.source = None
        
        self.env['graphmgr'].graphAppend( commpack )
        
        return Vector( data_container )

    def zeros( self ):
        """
        Create a vector of zeros within this vector space
        
        space.zeros( ) -> vector
        """
        return self.create()
    
    def spike(self,**kw):
        """
        create a vector with spikes
        """
        space = self.copy( )
        space.pop( 'out', None )
        istmp = kw.pop( 'istmp', True )
        
        params = self.params.copy()
        params.update( kw)
        
        command = self.generate_command( "spike", **params )
        # empty data container 
        
        data_container = self.makeContaner( command=command ,tmp=istmp)
        
        converter = data_container.get_converter( command )
        
        commpack = converter.convert( None, command )
        
        commpack.target = data_container
        commpack.source = None
        
        self.env['graphmgr'].graphAppend( commpack )
        
        return Vector( data_container )
    
    def ones( self ):
        """
        Create a vector of ones within this vector space
        """
        return self.create( out=1 )  
    
    def isReal( self ):
        'test is the space contains real values'
        return self['data_type'] == 'float' or self['data_type'] == float   
    
    ## test is the space contains complex values
    def isComplex( self ):
        return self['data_type'] == 'complex' or self['data_type'] == complex
    
    def isInt( self ):
        "test is the space contains integer values"
        return self['data_type'] == 'int' or self['data_type'] == int

    ## space that would result from vector additions
    def VectorAddition(self, *other_spaces ):
        """
        VectorSpace.VectorAddition( *spaces ) -> New space
        """
        plugin = self.plugin
        addition = self.generate_command('add')
        newspace = self
        
        for space in  other_spaces:
            if isinstance( space, PSpace ):
                converter = plugin.get_converter( addition )
                converter.constr(  addition, newspace, space )
                newspace = converter.trans( addition, newspace, space )
            else:
                pass
            
        return newspace.copy( )
    
def VectorAddition( stuff , *default ):
    """
     space that would result from vector additions
     @ingroup userclasses
     @param stuff a list of vector spaces  
     @param default object to return if no space instances are found in param stuff
     @exception TypeError if no spaces are in param stuff and default is not given  
     @return VectorSpace 
     @relatesalso slimpy_base.Core.User.Structures.VectorSpace.VectorSpace
    """
    if len(default) > 1 :
        raise TypeError( "too many arguments need at most two" )
    
    
    item = stuff.pop()
    while not isinstance(item, PSpace ):
        if not stuff:
            if not default:
                raise TypeError( "no Spaces found to add and no default specified" )
            else:
                return default[0]
            
        item = stuff.pop()
        
    
    space = VectorSpace( item )
    
    return space.VectorAddition( *stuff )
    
