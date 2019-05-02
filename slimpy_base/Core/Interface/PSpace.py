"""
Parameter class is equivalent to a header file for data
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

from slimpy_base.Environment.InstanceManager import InstanceManager

## Class to track metadata of SLIMpy objects
# @ingroup userclasses
#
class PSpace( object ):
    """
    parameter is a simple tracking method to pass Metadata without
    being bound to each specific datatype
    methods are similar to a python dict
    """
    ## @var _space_dict 
    # @brief dict of information about this space
    
    ## @var _plugin 
    # @brief slimpy_base.api.Plugin represented by this space
    
    ## slimpy global variables
    env = InstanceManager( )
    
    ## Constructor, create a space from another space or like a dict object  
    #     @param plugin a string name or a subclass of DataContainer
    def __init__(self, plugin, *E, **D ):
        """
        create a space from another space 
        """
        
        if isinstance(plugin, PSpace):
            self._space_dict = dict( plugin.params, *E, **D )
            self.plugin = plugin.plugin
        else:
            self._space_dict = dict( *E, **D )
            self.plugin = plugin
            
        
    ## Get the plugin represented by this space
    def _get_plugin( self ):
        'Get the plug-in represented by this space'
        return self._plugin
    
    def _set_plugin(self,plugin):
        from slimpy_base.Core.Interface.ContainerBase import DataContainer
        plugin_type = type(plugin )
        assert plugin_type == str or issubclass(plugin, DataContainer) 
        if isinstance( plugin, str ):
            self._plugin = self.env['keystone'].getplugin( plugin )
        else:
            self._plugin = plugin
    
    ## get and set property for self._plugin
    plugin = property( _get_plugin ,_set_plugin)
    
    ## Make a new container from the current parameters
    # @param command may be a string or a slimpy_base.Core.Command.Command.Command
    # @tmp if the contaier is a temporary file
    def makeContaner( self, command=None ,tmp=None):
        """
        makeContaner( self, command=None ,tmp=None) -> Container
        Make a new container from the current parameters
        
        """
        return self.plugin( parameters=self, command=command, tmp=tmp)
    
    ## create a new PSpace updated with new keys
    def newParameter( self, *E, **F ):
        """
        Make a new parameter updated with the new keys, 'keys'
        """
        SpaceType = type(self)
        x = SpaceType( self.plugin, self, *E, **F )
        return x
    
    ## update this PSpace with another
    def update(self , *E, **F ):
        """
        update this PSpace with another same as a python dict  
        """
        
        for e in E:
            
            if isinstance(e, PSpace):
                self._space_dict.update(e.params)
            elif e is None:
                pass
            else:
                self._space_dict.update(e)
                
        self._space_dict.update( **F )
        
        return 
    
    ## number of elements the space represents
    def __len__(self):
        return self.size
    
    ## shallow copy
    def copy( self ):
        """
        returns a shallow copy of self
        """
        SpaceType = type(self)
        return SpaceType( self.plugin, self._space_dict.copy(  ) )
    
    ## returns tr 
    # @return bool 
    def has_key(self , k ):
        ' D.has_key(k) -> True if D has a key k, else False'
        return self._space_dict.has_key(k)
    
    ## shape of the underlying image 
    def _get_shape( self ):
        """
        Returns a list of the dimensions of the image of the underlying vector
        """
        shp = []
        
        N = 1
        while self.has_key( "n%s" %N ):
            val = self["n%s" %N]
            if val < 1:
                raise TypeError( "shape parameter does not conform to SLIMpy standard:\n"
                                "Should be an int greater than 0" )
            shp.append( val )
            N += 1
        
        if N is 1:
            return ( )
            
        i = len( shp ) -1
        while i > 0 and shp[i] is 1:
            shp.pop( -1 )
            i -= 1
            
        return shp
    
    ## setter for shape of the underlying image
    # @param shape is a sequence of integers  
    def _set_shape(self, shape ):
        """
        delete all n* keys and replace them with shape 
        """
        N = 1
        nN = "n%s" %N
        while self.has_key( nN ):
            del self[nN]
            N+=1; nN = "n%s" %N
        
        
        for N,val in enumerate(shape):
            nN = "n%s" %(N+1)
            self[nN] = val
    
    ## returns size of field of scalars
    def get_size(self):
        
        mul = lambda x,y:x*y
        prod = lambda shape:reduce( mul, shape, 1 )
        shape = self.shape
        
        for i in shape:
            if i == UnknownValue:
                return None
        if not shape:
            return 0
        else:
            return prod(shape)
    
    ## size property
    size = property( get_size )
    ## shape property
    shape = property( _get_shape, _set_shape )
    
    def _get_ndim(self):
        return len(self.shape)
    
    ndim = property( _get_ndim )
    
    ## list of keys
    def keys(self):
        return self._space_dict.keys( )
    
    ## pop a key from the dict
    # @exception raises a KeyError if k is not a key in self and no default is given  
    def pop(self,k,*default):
        return self._space_dict.pop( k, *default )
    
    def _get_params(self, keep_unknown=False ):
        if keep_unknown:
            params = self._space_dict.copy( )
        else:
            itemset = [ (k,v) for (k,v) in self.iteritems() if v is not UnknownValue ]
            params = dict( itemset )
            
        return params
    
    params = property( _get_params )
    
    ## @see dict
    def iteritems(self):
        """
        iterates over key value pairs in self
        """
        return self._space_dict.iteritems()
    
    ## helper for intersection and union
    def _space_helper(self, other ,error=False):
        set_self = set( self.keys( ) )
        set_other = set( other.keys( ) )
        
        intersect = set_self.intersection( set_other )
        diff_self = set_self.difference( set_other )
        diff_other = set_other.difference( set_self )
        
        new = {}
        for key in intersect:
            v1 = self[key];v2 = other[key]
            if not self.equal_keys( other, key):
                if error:
                    raise ValueError("item self[%(key)s] != other[%(key)s] ; %(v1)s != %(v2)s")
                else:
                    v1 = UnknownValue
                    v2 = UnknownValue
            
            if v1 == UnknownValue:
                new[key] =  v2
            else:
                new[key] =  v1
        
        SpaceType = type(self)
        inter_space = SpaceType( self.plugin , new ) 
        dspace_self = SpaceType( self.plugin , [ (key,self[key]) for key in diff_self] )
        dspace_other = SpaceType( self.plugin , [ (key,other[key]) for key in diff_other] )
        
        return  inter_space, dspace_self, dspace_other
    
    ## intersection of this space and another 
    def intersection( self , other ):
        """
        space.intersection( other ) -> Space
        
        returns a Space object that is the Intersection of self and other
        contains the restrictions of each space
        the shared restrictions in each must be equal:
        i.e. if self contains restriction n1=5 and other -> n1=6 
            intersection method will raise error.
        """
        inter_space, dspace_self, dspace_other = self._space_helper( other, True )
        
        inter_space.update( dspace_self, dspace_other )
        
        return inter_space
    
    def _union( self, other ):
        """
        space.union( other ) -> Space 
        
        returns the union of this space with another 
        """
        inter_space, dspace_self, dspace_other = self._space_helper( other, False )
        
        return inter_space
    
    ## union of this space with another
    def union(self, other, *others ):
        """
        space.union( other, *others ) -> Space 
        
        returns the union of this space with another
        that is only the restrictions that are the same in both spaces
         
        """
        
        next = self._union(other)
        
        for oths in others:
            next = next._union( oths )
            
        return next



    
    
    def __eq__(self,other):
        
        if type(self) != type(other):
            return False
        
        test1 = self._space_dict == other._space_dict
        test2 = self.plugin == other.plugin
        
        return test1 and test2
    
    ## True if self and other both have key k
    # @param other PSpace object
    # @param accept_unknown if the value at key k for either self or other is an slimpy_base.Core.Interface.PSpace.UnknownValue
    #     then  equal_keys returns accept_unknown
    def equal_keys(self,other,k , accept_unknown=True):
        """
        space.equal_keys( space2, key, accept_unknown=True ) -> bool
        returns true if key is present and equal in both spaces.
        If one value is UnknownValue then will return accept_unknown.
        """
        if self.has_key(k) and other.has_key(k):
            v1 = self[k]; v2 = other[k]
            if v1 is UnknownValue or v2 is UnknownValue:                
                return accept_unknown
            else:
                return v1==v2
        else:
            return False
    
    def itervalues(self):
        return self._space_dict.itervalues()
    def values(self):
        return self._space_dict.values()
    def iterkeys(self):
        return self._space_dict.iterkeys()
    
    def setdefault(self, k ,D=None ):
        return self._space_dict.setdefault( k, D=D )
        
    def has_unknown(self):
        return len( [ v for v in self.itervalues() if v == UnknownValue ] )
    
    ## true if self is a subspace of other.
    def is_subspace(self,other, accept_unknown=True ):
        """
        space.is_subspace(other) <--> space in other
        returns true if self is a subspace of other.
         
        """
        assert isinstance(other, PSpace)
        
        if self.plugin != other.plugin:
            return False
        
        key_set = set( self.keys() )
        key_set_other = set( other.keys() )
        
        
        issubset = key_set_other.issubset( key_set )
        
        if not issubset:
            return False
        
        for key in key_set_other:
            if not self.equal_keys(other, key ,accept_unknown=accept_unknown):
                return False
            
        return True
    
    ## true if self is a superspace of other.
    def is_superspace(self,other,accept_unknown=True):
        return not self.is_subspace( other, accept_unknown=accept_unknown )
    
    ## true if self is a contains k
    # @param k a PSpace a key in self or a vector
    def __contains__(self, k):
        """
        S.__contains__( k ) <-> k in S
        """
        if isinstance( k, PSpace ):
            return k.is_subspace( self )
        elif hasattr(k, 'space') and isinstance( k.space, PSpace ):
            return k.space.is_subspace( self )
        else:
            return self._space_dict.__contains__( k )
    
    def __getitem__(self,item):
        return self._space_dict[item]
    
    def __delitem__(self,item):
        self._space_dict.__delitem__(item)
    
    def get(self,k,default=None):
        return self._space_dict.get(k,default)
    
    def __setitem__(self,item,val):
        self._space_dict[item] = val
    
    def __repr__(self):
        name = self.__class__.__name__
        return "%s( %s, %s )" %( name, repr(self.plugin), repr(self._space_dict) )
    
    def __str__(self):
        dtype = self.get( 'data_type', "unknown data type" )
        size = self.size
        name = self.__class__.__name__
        return "<%(name)s %(dtype)s:%(size)s>" %vars()

class umet( type ):
    def __str__(self):
        return  "<Space.UnknownValue>"
    def __repr__(self):
        return  "<Space.UnknownValue>"

## Place holder for an unknown value inside of a PSpace
# @relates slimpy_base.Core.User.Structures.VectorSpace.VectorSpace
class UnknownValue( object ): 
    __metaclass__ = umet


class voidSpace( PSpace ):
    
    def create( self, out=0 ):
        """
        @raise TypeError: can not create data from a void space
        """
        raise TypeError( "can not create data from a void space" )
    
    def testCommand( self, cmd, *args, **kargs ):
        """
        returns VoidSpace
        """
        return self
