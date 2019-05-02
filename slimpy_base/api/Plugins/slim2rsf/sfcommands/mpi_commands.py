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
from slimpy_base.Core.Interface.node import Source
from slimpy_base.api.Plugins.slim2rsf.mpi_factory import rsf_mpi_factory
from slimpy_base.api.Plugins.slim2rsf.sfCommandFactory import rsfCommandFactory
from slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter import sfConverter
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
from itertools import izip
from numpy import  divide, prod, array, fromiter
from os.path import join
from slimpy_base.api.linearops.ScatterOperator import apply_along_axis
from slimpy_base.Core.Command.Drivers.FileDist import even_dist
from socket import getfqdn

#def gethostname():
#    return os.uname()[1]

def windowm_mpi_runtime_map( command ):
    
    _env = InstanceManager()
    
    nodemap = _env['slimvars'].get_node_map()
    params = []
    
    nodes = [node for node,_ in nodemap ]
    files = command.params
    dist = even_dist(nodes, files, 0)
    for (container,node_dist) in izip( files, dist ):
        
        if isinstance(node_dist, tuple):
            from_node, to_node = node_dist
            assert from_node in container.nodenames
            container.node_copy( to_node )
        else:
            from_node, to_node = node_dist,node_dist
        
        assert container.available_from( to_node )
        if to_node in ['localhost','']:
            to_node = getfqdn( )
        params.append( "%s:%s" %( to_node, container.get_data( to_node ) ) )
    
        
    return params , command.kparams

# create a Converter class
class create_meta_header_converter( sfConverter ):
    """
    This is a mapping instance that maps a SLIMpy command into an object that 
    can be run 
    This also maps the agruments and keyword arguments to be pugin specific
    """
    # alwas use classmethod or static method
    @classmethod
    def map( cls, source, command ):
        """
        map a SLIMpy command to a rsf command
        """
        # the RSF bin and 'sf' will be automaticaly prepended to fft1
        command = sfConverter.mpi_function(command, "create_meta", num_proc='all')
        
        meta_nX = source.space.meta.shape
        assert meta_nX is not None
        for i in range(3):
            command["N%s" %(i+1)] = 1
        for X,val in enumerate(meta_nX):
            meta_n = "N%s" %(X+1) 
            command[meta_n] = val

        numb_nX = source.space.meta['num_blocks']
        command.pop_kw('num_blocks', None)
        
        for i in range(3):
            command["p%s" %(i+1)] = 1

        for X,val in enumerate(numb_nX):
            block = "p%s" %(X+1) 
            command[block] = val
        
        if 'eps' in source.space.meta:
            command['eps'] = source.space.meta['eps']
        
        source_list = source.ravel().tolist()
        
        command.add_other_dep( Source )
        sources = [ Source(srtuc.container) for srtuc in source_list]
        command.params.extend( sources )
        
        slen = len(source_list)
        for i,val in enumerate([slen,1,1]):
            command['n%s' %(i+1)] = val
        
        
        command.runtime_map = windowm_mpi_runtime_map
        command = cls.truefalseHelper( command )
        
        return cls.pack( command, stdin=None )
    
    @classmethod
    def map_adj( cls, source, command ):
        command = sfConverter.default_function( command, "#Extracting Meta Info" )
        command.command_type = 'multi_process'
        return cls.pack( command, stdin=None,stdout=None )
        
    
    @classmethod
    def trans( cls, command, space, *spaces ):
        'define how this operator affect the space'
        # from metaspace to 
        metaspace = space.copy()
        space = space.coalesce( )
        space.plugin = 'rsfmpi'
#        space.shape = command['meta_shape']
#        space['num_blocks'] = command['num_blocks']
        space['metaspace'] = metaspace
        space.update( metaspace.meta )
        return space

    @classmethod
    def trans_adj( cls, command, space, *spaces ):
        'define how this operator affect the space'
#        space.plugin = 'slim2rsf'
        metaspace = space['metaspace'].copy()
        
        metaspace.meta = space.copy()
        return metaspace
    
    @classmethod
    def constr( cls, command, space ):
        assert isinstance( space, MetaSpace )
        
    @classmethod
    def constr_adj( cls, command, space ):
        'make sure the data on the adjoint command is complex'
        assert isinstance( space, PSpace )
        


class scatter_mpi_converter( sfConverter ):
    """
    This is a mapping instance that maps a SLIMpy command into an object that 
    can be run 
    This also maps the agruments and keyword arguments to be pugin specific
    """
    fprefix = 0
    @classmethod
    def gen_node_map(cls, space, command ):
        mapping = cls.env['slimvars'].get_node_map( )
        
        filenodemap = []
        
        fprefix = space['fprefix']
        for nodename, rank in mapping:
            filename = fprefix+".%.4d.rsf"  %rank
            filenodemap.append( (filename,nodename) )
#            filenodemap[filename] = nodename
            
        return filenodemap
    
    @classmethod
    def get_fprefix(cls):
        fprefix = "scatter_mpi.%d" %cls.fprefix
        cls.fprefix +=1 
        return fprefix
        
    # alwas use classmethod or static method
    @classmethod
    def map( cls, source, command ):
        """
        map a SLIMpy command to a rsf command
        """
        
        # the RSF bin and 'sf' will be automaticaly prepended to fft1
        command = sfConverter.mpi_function(command, "winscumpi")
                
        command['datapath'] =  cls.env['slimvars']['localtmpdir'] 
        #change all python True/False objects to 'y'/'n' strings
        
        command = cls.keywordmap(command, {'adj':'inv'})
        command = cls.truefalseHelper( command )
        #map the adj flage to inv
        num_blocks = command.pop_kw('num_blocks')
        for X,pX in enumerate(num_blocks):
            command[ 'p%s' %(X+1) ] = pX
            
        
        return cls.pack( command )
    
    @classmethod
    def trans( cls, command, space, *spaces ):
        'define how this operator affect the space'
        num_blocks = command['num_blocks'] 
        slist = []
        for blk in range( prod(num_blocks) ):
            comp = space.copy( )
            comp.shape = divide( comp.shape, num_blocks )
#            for i in range(comp.ndim):
#                comp['s%s' %(i+1)] = 0
            slist.append( comp ) 
            
        
        space.plugin = 'rsfmpi'
        
        fprefix = cls.get_fprefix()
        command['fprefix'] = fprefix
        localtmpdir = cls.env['slimvars']['localtmpdir']
        space['fprefix'] = join( localtmpdir, fprefix )
        
        space['num_blocks'] = num_blocks
        
        metaspace = MetaSpace( slist )
        metaspace.resize( num_blocks )
        metaspace.meta = space.copy()
        
        set_offset(metaspace)
        
        space['metaspace'] = metaspace
         
        return space

    @classmethod
    def trans_adj( cls, command, space, *spaces ):
        'define how this operator affect the space'
        space.plugin = 'rsf'
        space.pop( 'metaspace' , None )
        space.pop( 'fprefix' , None )
        space.pop( 'num_blocks' , None )
        
        
        return space
    
    @classmethod
    def constr( cls, command, space ):
        'make sure the data on the forward command is float'
    
    @classmethod
    def constr_adj( cls, command, space ):
        'make sure the data on the adjoint command is complex'


def add_eps( metaspace, eps, oper):
    
    mshape = list( metaspace.meta['num_blocks'] )
    ndim = len(mshape)
    
#    set_trace() 
    epsary = array( [eps]*ndim ) #* (array(mshape) != 1) 
#    shpary = array( mshape )
#    z0 = zeros_like(epsary)
    
    for pos in xrange(metaspace.size):
        space = metaspace.flat[pos]
        space.shape = oper( space.shape, epsary*2 )
        
    return

def set_offset_eps( metaspace ,eps ):
    mshape = list( metaspace.meta['num_blocks'] )
    blocksize = array(metaspace.meta.shape)/mshape
    ndim = metaspace.ndim
    def f( arr, axis, multipl,eps ):
        for space,sX in zip(arr, multipl):
            space['s%s' %(axis+1)] = sX-eps
        
        return arr
    
    for axis in xrange(ndim):

        multipl = fromiter( xrange(0, metaspace.meta.shape[axis], blocksize[axis] ), int)
        apply_along_axis( f, axis,metaspace,axis,multipl ,eps )
    
    return 

def set_offset( metaspace  ):
    
    mshape = list( metaspace.meta['num_blocks'] )
    blocksize = array(metaspace.meta.shape)/mshape
    ndim = metaspace.ndim
    def f( arr, axis, multipl ):
        for space,sX in zip(arr, multipl):
            space['s%s' %(axis+1)] = sX
        
        return arr
    
    for axis in xrange(ndim):

        multipl = fromiter( xrange(0, metaspace.meta.shape[axis], blocksize[axis] ), int)
        apply_along_axis( f, axis,metaspace,axis,multipl  )
    
    return 
            
class ghost_taper_converter( sfConverter ):
    """
    This is a mapping instance that maps a SLIMpy command into an object that 
    can be run 
    This also maps the agruments and keyword arguments to be pugin specific
    """
    fprefix = 0
    @classmethod
    def gen_node_map(cls, space, command ):
        mapping = cls.env['slimvars'].get_node_map( )
        
        filenodemap = []
        
        fprefix = space['fprefix']
        for nodename, rank in mapping:
            filename = fprefix+".%.4d.rsf"  %rank
            filenodemap.append((filename,nodename))
            
        return filenodemap
    
    @classmethod
    def get_fprefix(cls):
        fprefix = "ghost_update_mpi.%d" %cls.fprefix
        cls.fprefix +=1 
        return fprefix
        
    # alwas use classmethod or static method
    @classmethod
    def map( cls, source, command ):
        """
        map a SLIMpy command to a rsf command
        """
        
        # the RSF bin and 'sf' will be automaticaly prepended to fft1
        command = sfConverter.mpi_function(command, "wintpgmpi")
                
#        command.params.extend([ '-datapath', cls.env['slimvars']['localtmpdir'] ] )
        command['datapath'] =  cls.env['slimvars']['localtmpdir']
        #change all python True/False objects to 'y'/'n' strings
        
        command = cls.keywordmap(command, {'adj':'inv'})
        command = cls.truefalseHelper( command )
        #map the adj flage to inv
        
        return cls.pack( command )
    
    @classmethod
    def trans( cls, command, space, *spaces ):
        'define how this operator affect the space'
        num_blocks = space['num_blocks']
        metaspace = space['metaspace'].copy()
        
        fprefix = cls.get_fprefix()
        command['fprefix'] = fprefix
        localtmpdir = cls.env['slimvars']['localtmpdir']
        space['fprefix'] = join( localtmpdir, fprefix )
        
        
#        blocks = zeros( num_blocks, dtype=object )
        eps = command['eps']
        add_eps( metaspace, eps, 
                 lambda shape,epsary:shape+epsary )
        
        
        set_offset_eps(metaspace, eps)
        
        space['eps'] = eps
        space['metaspace'] = metaspace
        return space

    @classmethod
    def trans_adj( cls, command, space, *spaces ):
        'define how this operator affect the space'
        
        space['metaspace']
        fprefix = cls.get_fprefix()
        command['fprefix'] = fprefix
        localtmpdir = cls.env['slimvars']['localtmpdir']
        space['fprefix'] = join( localtmpdir, fprefix )
        
        eps = command['eps']

        metaspace = space['metaspace'].copy()
        
        add_eps( metaspace, eps, 
                 lambda shape,epsary:shape-epsary )
        
        set_offset(metaspace)
        
        space['metaspace'] = metaspace
        space['eps'] = 0
        return space
    
    @classmethod
    def constr( cls, command, space ):
        'make sure the data on the forward command is float'
    
    @classmethod
    def constr_adj( cls, command, space ):
        'make sure the data on the adjoint command is complex'



factory = rsfCommandFactory()
# add the converter class to the factory
# now converter will be invoked when tag is called
factory['meta'] = create_meta_header_converter

factory['window_mpi'] = scatter_mpi_converter

mpi_factory = rsf_mpi_factory( )
mpi_factory['window_mpi'] = scatter_mpi_converter
mpi_factory['meta'] = create_meta_header_converter
mpi_factory['ghost_taper'] = ghost_taper_converter
