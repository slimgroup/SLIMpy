"""
Base Container class for plug-ins to use

can be used as a test class eg vector("vec.test")
returns a Vector instance with a DataContainer instance 
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


from slimpy_base.Core.Interface.PSpace import PSpace 
from slimpy_base.Core.Command.Converter import Converter
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Core.Interface.node import Node
from pdb import set_trace
#from slimpy_base.Core.Interface.PSpace import voidSpace

__env__ = InstanceManager()

def contain( data ):
    """
    Contain some data.
    Uses plug-ins associated with the keystone class
    to find a dataContainer compatible with data.
    """
    keystone = __env__['keystone']
    for plugin in keystone.getplugins().values():
        if plugin.isCompatibleWith( data ):
            # istantiate plugin data container
            return plugin( data )

    raise AttributeError, "The data '%s' could not be contained" % data

class ScalarMethods( object ):
    
    @classmethod
    def __call__(cls,container,scalar,*args,**kw):
        scalar.set( 0 )
        
        return
    
    def __str__(self):
        return "<adc ScalarMethods>"

class DataContainer( object ):
    """
    vectorflie has two main purposes - to keep track of "out of core" 
    vectors corresponding binary files on disk
    and to act as a wrapper to a given library.
    """
    name = "ADC"
    test = 0
    _scalar_methods = ScalarMethods( )
    
    def _get_referents(self):
        "Return the list of objects that are directly referred to by this container"
        return self._referents
    
    def _get_referrers(self):
        "Return the list of objects that directly refer to self"
        return self._referents
    
    referents = property( _get_referents, 
        doc="Return the list of objects that are directly referred to by this container" )
    
    referrers = property(  _get_referrers,
        doc="Return the list of objects that directly refer to self" )
    
    
    def add_referent(self, id):
        'add to the list of objects that are directly referred to by this container'
        self.referents.add( id )
        
    def add_referrers(self, id ):
        'add to the list of objects that directly refer to self'
        self.referrers.add( id )
    
    @classmethod
    def isCompatibleWith( cls, data ):
        """
        method to determine if the data is compatible with 
        Data 'data'.
        """
        if isinstance( data, str ):
            if data.endswith( '.test' ):
                return True
        return False

    def __init__( self , data=None , parameters=None, command=None, tmp=None, 
                  nodenames=None,
                  node_info=None, 
                  target_node=None ):
        """
        create container: both data and parameters may not be none.
        and are mutually exclusive.
        if parameters is None: data is expected to exist and parameters will be generated
        if data is None: this instance will be assumed to need to be created.
        """
        self._referents = set( )
        self._referrers = set( )
        self.__data = data
        self._temporary = True
        self._node_names = set()
        self._node_info = { }
        self._target_node = None
        
        
        if parameters is None and data is None:
            raise TypeError, "parameters and data may not both be None"
        
        elif data is None:
            
            if tmp is None:
                self._temporary = True
            else:
                self._temporary = tmp
            
            if nodenames:
                raise Exception("Data not created yet node is specified")
            
            self._target_node = target_node
            # data is None so we generate a name and set the parameters to the 
            #given value
            self.__data = self.genName(command=command)
            self.__parameters = parameters
        else:
            if tmp is None:
                self._temporary = False
            else:
                self._temporary = tmp
            
            if nodenames and target_node:
                raise Exception("can not specify both keyword arguments "
                                "'nodenames' and 'target_node'")
            elif nodenames:
                self._node_names.update( nodenames )
            elif target_node:
                self._target_node = target_node
                if node_info:
                    self._node_info[target_node] = node_info
            else:
                self.add_node_name( "localhost" )

            if node_info:
                for node in self.nodenames:
                    self._node_info[node] = node_info
            
                    
            if parameters is None:
                self.__parameters = self.makeparams()
            else:
                self.__parameters = parameters
        
        if node_info:
            for node in self.nodenames:
                self._node_info[node] = node_info
        
        return

    def add_target_to_current( self ):
        self.add_node_name( self.target_node )

    def getScalar_methods(self):
        return self._scalar_methods    
    
    def __is_global(self):
        if self.nodenames:
            return  bool( 'localhost' in self.nodenames)
        elif self.target_node:
            return  bool( 'localhost' == self.target_node)
        else:
            return False
#            raise Exception( "no known destination for this node" )
    
    def __is_local(self):
        
        return not self.__is_global( )
    
    is_global = property( __is_global )
    is_local = property( __is_local )
    
    
    def add_node_name(self,name):
        if self.is_global:
            self._node_names.add( 'localhost' )
        else:
            self._node_names.add( name )
    
    def _get_node_names(self):
        return self._node_names
    
    nodenames = property( _get_node_names )
    
    def node_copy(self,node_name):
        """
        copy data from node to node, data container stays the same
        """
        self.add_node_name(node_name)
        
    def _get_target_node(self):
        return self._target_node
    
    target_node = property( _get_target_node )
    
    def _get_data( self ):
        """
        get the data contained
        """
        return self.__data

    def _set_data( self ,val ):
        """
        get the data contained
        """
        self.__data = val
    
    def get_data( self, node_name ):
        return self.__data
    
    def setData( self, data ):
        
        self.__data = data
    
    data = property( _get_data , _set_data )
    
    def __setitem__( self, item, value ):
        
        assert item == 'data', "can not set the item %s(item)s" % vars()
        
        self.__data = value
        


    def isempty( self ):
        """
        Returns True if the data associated with self.data does not exist
        """
        return True
    
    def isfull( self ):
        """
        Returns True if the data associated with self.data exists
        """
        if self.__dict__.has_key( 'full' ) :
 
            return True
        
        
        return not self.isempty()
    
    
    def tmp( self, TMP=None ):
        """
        set whether the data is  temporary
        or not
        """
        if TMP is None:
            self._temporary = not self._temporary
            
        else:
            self._temporary = TMP
    
    def istmp( self ):
        """
        query whether the data is  temporary
        """
        return self._temporary
    
    def remove( self ):
        """
        remove the data from memory
        """
        return self.rm()
    
        

    # __STR__ 
    def __str__( self ):
        """Adds the current lib's suffix to the end of filename
        note: if no lib is set then self.plugin.suffix returns ''
        """
        return str( self.__data )

    def __repr__( self ):
        """
        see: __str__
        """
        return str( self )
    
#    def getConverter( self, command ):
#        
#        return Converter
    
    @classmethod
    def get_converter(cls , command ):
        return Converter

    def getParameters( self ):
        """
        return parameter instance
        """
        return self.__parameters
    
    params = property( getParameters )
    
    def available_from( self, nodename ):
        return true
#    def apply_command(self, command ):
#        
#        """
#        apply a command to a dataContainer or a dataContainer holder obeject
#        returns a new dataContainer instance
#        """
#        # other.parse manipulates the command relative to the
#        # data container that it is in
#        # so now the command can be run with that par
#        
#        
#        converter = self.get_converter( command )
#        
#        
#        strict_check = __env__['slimvars']['strict_check']
#        
##        if self.sglobals['strict_check'] == 0:
##            pass
#        if strict_check > 0:
#            converter.constrain( command, self.params )
#        
#        # Now that the data has been parsed we can get the new 
#        # space the data formed by that command
#        # is in
#        newspace = converter.transform( command, self.params )
#        
#        compack =  converter.convert( self, command )
#        
#        if strict_check > 1:
#            if isinstance( newspace, voidSpace ):
#                msg = ( "'strict_check >= 2' prevents commands "
#                        "from returning voidSpace\n"
#                        "command '%(command)s' returned voidSpace" %vars() )
#                raise Exception( msg )
#        # Make a new contnainer that knows a bout its space
#        newcontainer = newspace.makeContaner( command=command )
#        # append the command to the graph to be executed later 
#        # by a flush command
#        
#                
#        return compack, newcontainer

    
    def makeparams( self ):
        """
        make the parameter object from the given data
        should be extended for each plug-in
        """
        par= PSpace( self.__class__, self.readattr() )
        
        return par
    

    def genName( self, command=None ):
        """
        generate a name for the data
        """
        DataContainer.test += 1
        return"%s_%04d.test" %( self.name, self.test )
    

    def __del__( self ):
        """ overrides the del method
        if the object is deleted and there is a file that corresponds to filename and self.istpm
        then remove will be called to remove the file
        """
        #if self.istmp:
        #   self.rm()
        

    


    def plot( self ):
        """
        Plot the data to view it
        
        """
        pass
    

    def readattr( self ):
        """
        read the attributes of the data
        """
        return {}
    

    def readbin( self, i, shape ):
        """
        read the binary elements of the data
        """
        pass
    
    def scalar_reduction( self, cmd, *args, **kargs ):
        """
        return the string '${SCALAR}' 
        """
        return "${SCALAR}"
  
    def writebin( self, data, i , j ):
        """
        write the binary elements of the data
        """
        pass

 
    def writeattr( self, vector_dict, file_dict ):
        pass
    
        
    def rm( self ):
        """
        remove the data from memory
        """
        pass
        
    def diagnostic(self):
        
        return True

    scalar_methods = property( getScalar_methods )

    def expand_meta( self, metaspace ):
        
        raise Exception('this is not meta data')
        
        
    def _get_contained(self):
        return self._contained
    
    def _set_contained(self, val ):
        meta_id = Node( self ).id
        
        for node in [ Node(container) for container in val ]:
            node.add_referrers( meta_id )
            self.add_referent( node.id )
        
        self._contained = val
    
    contained = property( _get_contained, _set_contained )
    
    
