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

from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
from slimpy_base.Core.Interface.node import Source,Target
from slimpy_base.Core.Interface.Structure import Structure
from slimpy_base.Core.User.Structures.serial_vector import Vector
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType
from slimpy_base.Environment.InstanceManager import InstanceManager
from numpy import prod


## @ingroup linop 
class Meta( LinearOperatorStruct ):
    name = 'meta'
    
    def __new__( cls,  *params, **kparams ):
        return object.__new__(cls, *params, **kparams)
        
        
    def __init__( self, domain ):
        if isinstance( domain, MetaSpace):
            adj=False
#            meta_shape = domain.meta.shape
            num_blocks=domain.shape
        else:
            adj=True
#            meta_shape = domain.shape
            num_blocks = domain['num_blocks']
        
        
        LinearOperatorStruct.__init__(self, domain, 
#                                      meta_shape=tuple(meta_shape), 
                                      num_blocks=tuple(num_blocks), 
                                      adj=adj)
            
    def applyop(self, other):
        
        if self.isadj:
            ans = self.create_aug( other )
        else:
            ans = self.createmeta( other )
        return ans
    
    def create_aug( self , other ):
        
        already_exists = other.container.has_built_meta_info()
            
            
        cm = other.container.expand_meta( )
        lst = []; push = lst.append
        for cont in cm:
            push( Vector( cont ) )
            
        aug_vec = AugVector( lst )
        aug_vec.resize( self.kparams['num_blocks'] ) #IGNORE:E1101
        
        aug_vec.meta = self.domain()
        aug_vec.meta['num_blocks'] =  self.kparams['num_blocks']
        
        aug_vec.meta_vector = other
        
        if already_exists:
            return aug_vec
         
        struct = Structure( )
        
        command = struct.generate_command( 'meta' ,Source(other.container),  **self.kparams )
#        command.add_other_dep(  )
        for cont in cm:
            command.add_other_dep( Target( cont ) )

        converter = other.container.get_converter( command )
        commpack = converter.convert( other, command )
        
        commpack.target = None
        commpack.source = None
        
        self.env['graphmgr'].graphAppend( commpack )
        
        return aug_vec
    
    def createmeta( self, other ):
        
        if hasattr(other,  'meta_vector' ) and other.meta_vector is not None:
            return other.meta_vector
        
        struct = Structure()
        
        container = other.ravel()[0].container
        command = struct.generate_command( 'meta' , **self.kparams )
        
        converter = container.get_converter( command)
        
        compack, meta_container = converter.apply_command( command, other )
        
        compack.source = container
        compack.target = meta_container
        
        struct.env['graphmgr'].graphAppend( compack )
        
        meta_container.contained = [ vec.container for vec in other.ravel().tolist() ]
        
        return Vector( meta_container )
 
## @ingroup linop    
class ScatterMPI( LinearOperatorStruct ):
    """
    mpi scatteroperator
    """
    name = "window_mpi"
    
    def __init__( self, inSpace, num_blocks ):
        env = InstanceManager()
        np = env['slimvars']['np']
        if prod(num_blocks) != np:
             raise Exception( "num_blocks does not match mpi variable 'np', %(num_blocks)s != %(np)s " %vars() )

        kparams = dict( num_blocks=tuple(num_blocks) )

        LinearOperatorStruct.__init__( self, inSpace, **kparams )


## @ingroup linop 
@LinearOperatorType
def MScatter( domain, num_blocks ):
    """
    helper function for ScatterMPI
    """
    S = ScatterMPI( domain, num_blocks)
    M = Meta( S.range() )
    return M(S) 


## @ingroup linop 
class GhostTaper( LinearOperatorStruct ):
    """
    mpi scatteroperator
    """
    name = "ghost_taper"
    
    def __init__( self, inSpace, eps ):
        
        kparams = dict( eps=eps )

        LinearOperatorStruct.__init__( self, inSpace, **kparams )


## @ingroup linop 
@LinearOperatorType
def MGhostTaper( domain, eps):
    M1 = Meta( domain )
    G = GhostTaper( M1.range() , eps )
    M2 = Meta( G.range( ) )
    return M2( G( M1 ) )
    
