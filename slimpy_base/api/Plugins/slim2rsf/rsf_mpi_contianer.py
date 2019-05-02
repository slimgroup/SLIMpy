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


from slimpy_base.api.Plugins.slim2rsf.rsfContainer import rsf_data_container
from slimpy_base.api.Plugins.slim2rsf.mpi_factory import rsf_mpi_factory
from os.path import isfile
from slimpy_base.Core.Interface.node import Node
from slimpy_base.Core.Command.Drivers.Unix_Pipes import gethostname
class MPI_ScalarMethods( object ):
    def __call__(self,*args,**kw):
        raise Exception( 'rsf mpi has no scalar methods' )
    
class rsf_mpidata_container( rsf_data_container ): 
    '''
    
    '''
    suffix = ".xsf"
    psuffix = ".vpl"
    name = "rsfmpi"

    _scalar_methods = MPI_ScalarMethods( )
    sfFactory = rsf_mpi_factory()
    
    def __init__(self, data=None , parameters=None, command=None, tmp=None ):
        
#        self._node_names = ["localhost"]
        self._command = command
        self._node_map = None
        self._contained = None
        rsf_data_container.__init__(self, data=data , 
                                    parameters=parameters, 
                                    command=command, 
                                    tmp=tmp, 
                                    target_node='localhost' )
        
    
    @classmethod
    def isCompatibleWith( cls, obj ):
        '''
        statict method to determine if 'obj' is an rsf meta header file
        @param obj:
        @type obj: any object that would be 
            contained in a datacontainer class
        '''
        
        obj = str(obj)
        
        if obj.endswith( cls.suffix ):
            if not isfile( obj ):
                raise Exception, "the file %s can not be found" %( obj )
            return True
        if isfile( obj + cls.suffix ):
            return True
        
    
    def node_copy(self, node_name):
        if node_name == 'localhost' or node_name == gethostname( ):
            return
        else:
            raise Exception('can not copy meta header to local nodes')
    
    def has_built_meta_info(self):
        return self._contained is not None
    
    def expand_meta( self ):
        """
        Returns an list of all the subcontainers in this one.
        """
        
        if self._contained is None:
            
            self._contained = []
            if self._node_map is None:
                converter = self.get_converter( self._command.tag )
                self._node_map = converter.gen_node_map( self.params, self._command )
                metaspace = self.params['metaspace']
                
            tmp = self.istmp()
            self_id = Node(self).id
            
            siter = zip( self._node_map , metaspace.ravel( ) )
            for (data, nodelist), space in siter:
                
                dc = rsf_data_container( data, space ,
                                         target_node = nodelist,
                                         tmp=tmp )
                self._contained.append( dc )
                
                id = Node(dc).id
                
                self.add_referent(id)
                dc.add_referrers( self_id )
                
                
        return self._contained
        

