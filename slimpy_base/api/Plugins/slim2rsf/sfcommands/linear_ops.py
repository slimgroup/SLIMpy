"""
Converters for linear operators
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

from slimpy_base.api.Plugins.slim2rsf.sfCommandFactory import rsfCommandFactory

from contourlet import surfSpaceChange, surfInvSpaceChange
 
from curvelet import GetShapeFwd, GetShapeInv
from curvelet import GetShapeFwd3d, GetShapeInv3d
 
from numpy import ceil
from pad import ( padHelper, 
                  padAdjHelper, 
                  padReplaceHelper )

from sfConverter import sfConverter

class all( object ):

    class fft1( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            command = cls.default_function( command, "fft1" ) 
            command = cls.truefalseHelper( command )
            command.kparams['inv'] = command.kparams['adj']
            command.kparams.pop( 'adj', None )

            return cls.pack( command )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            n1 = spaces[0]['n1']
            space['n1_fft']= n1
            space["n1"] = int( ceil( n1/2. )+1 )
            space['data_type']='complex' 
            return space
        
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            n1 = spaces[0]['n1_fft']
            space['data_type']='float'
            space['n1']= n1
            return space
        
        @classmethod
        def constr( cls, command, space ):
            cls.match( space, data_type='float' )
        @classmethod
        def constr_adj( cls, command, space ):
            cls.match( space, data_type='complex' )
#    
    class fft( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            command = cls.default_function( command, "fft3" ) 
            command = cls.truefalseHelper( command )
            command.kparams['inv'] = command.kparams['adj']
            command.kparams.pop( 'adj', None )
            return cls.pack( command )
        @classmethod
        def trans( cls, cmd, space, spaces ):
            return space
        
    class dwt( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd ) 
            cmd = cls.truefalseHelper( cmd )
            return cls.pack( cmd )
            
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space 
        
    class mdwt1( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd ) 
            cmd = cls.truefalseHelper( cmd )
            return cls.pack( cmd )
            
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
        
    class mrdwt1( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd ) 
            cmd = cls.truefalseHelper( cmd )
            return cls.pack( cmd )
            
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
        
    class daubcqf( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd ) 
            cmd = cls.truefalseHelper( cmd )
            cmd.kparams.pop( 'adj', None )
            return cls.pack( cmd )
            
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space               
        
    class fdct2( sfConverter ):
        """
        This is a mapping instance that maps a SLIMpy command into an object that 
        can be run 
        This also maps the agruments and keyword arguments to be pugin specific
        """
        # always use classmethod or static method
        @classmethod
        def map( cls, source, command ):
            """
            map a SLIMpy command to a rsf command
            """
#            __grahpmgr__.addBreakPoint( source )         
            # the RSF bin and 'sf' will be automaticaly prepended to fft1
#            sizes, curvepars = gen_sizes_file(command, source.params)
            
            command = cls.keywordmap(command, {'adj':'inv'} )
            command = cls.default_function( command, "fdct2left" )
            command.kparams.pop( 'cpxIn' ,None)
#            rfile = gen_rand_file()
#            sizes_target = Target( rfile )
#            command.kparams['sizes'] = sizes_target
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            #always must return a CommandPack instance
            
            return cls.pack( command )
    
        @classmethod
        def map_adj( cls, source, command ):
            """
            map a SLIMpy command to a rsf command
            """         
            # the RSF bin and 'sf' will be automaticaly prepended to fft1
            # tup = command['nbs'], command['nba'], command['ac'], source.params['n1'], source.params['n2']
            # sizes = sizes_files[ tup ]
            
            command = cls.keywordmap(command, {'adj':'inv'} )
            cpxIn = command.kparams.pop( 'cpxIn' ,False)
            # command.kparams['sizes'] = Source( sizes )
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            
            if cpxIn:
                command = cls.default_function( command, "fdct2" )
            else:
                c1, c2 = cls.split( command )
                c1 = cls.default_function( c1, "fdct2" )
                c2 = cls.keep( c2, [] ) # keep no arguments
                c2 = cls.default_function( c2, "real" )
                command = [ c1, c2 ]
            #alwas must return a CommandPack instance
            return cls.pack( command )
         
        @classmethod
        def trans( cls, command, space, *spaces ):
            
            shape = GetShapeFwd( command, space )
            
            space['N1'] = space['n1']
            space['N2'] = space['n2']
            
            space['n1'] = shape[0]
            space['n2'] = 1
            
            space['nbs'] = command['nbs']
            space['nba'] = command['nba']
            space['ac'] = command['ac']
            
            space['data_type'] = 'complex'
            return space
            
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            shape = GetShapeInv( command, space )
    
            space['n1'] = shape[0]
            space['n2'] = shape[1]
            if command['cpxIn']:
                pass
            else:
                space['data_type'] = 'float'
            return space
        
        @classmethod
        def constr( cls, command, space ):
            cls.match( space, data_type='float' )
            if not space.ndim == 2:
                raise Exception("wrong number of dimentions for fdct2 got %s" %( space.ndim ) )
    
        @classmethod
        def constr_adj( cls, command, space ):
            pass

    class fdct3( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            

            command = cls.keywordmap(command, {'adj':'inv'} )
            command = cls.default_function( command, "fdct3" )
            command.kparams.pop( 'cpxIn' ,None)
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            #always must return a CommandPack instance
            
            return cls.pack( command )
        
        @classmethod
        def map_adj( cls, source, command ):
            """
            map a SLIMpy command to a rsf command
            """         
            # the RSF bin and 'sf' will be automaticaly prepended to fft1
            # tup = command['nbs'], command['nba'], command['ac'], source.params['n1'], source.params['n2']
            # sizes = sizes_files[ tup ]
            
            command = cls.keywordmap(command, {'adj':'inv'} )
            cpxIn = command.kparams.pop( 'cpxIn' ,False)
            # command.kparams['sizes'] = Source( sizes )
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            
            if cpxIn:
                command = cls.default_function( command, "fdct3" )
            else:
                c1, c2 = cls.split( command )
                c1 = cls.default_function( c1, "fdct3" )
                c2 = cls.keep( c2, [] ) # keep no arguments
                c2 = cls.default_function( c2, "real" )
                command = [ c1, c2 ]
            #always must return a CommandPack instance
            return cls.pack( command )
        
#        @classmethod
#        def map_mpi( cls, source, command ):
#            command = cls.mpi_function( command , "fdct3_mpi" )
#            command = cls.truefalseHelper( command )
#            command = cls.keywordmap( command, {'adj':'inv'} )
#            return cls.pack( command )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            space['data_type'] = 'complex'
            
            
            shape = GetShapeFwd3d( command, space )
            
            space['N1'] = space['n1']
            space['N2'] = space['n2']
            space['N3'] = space['n3']
            
            space.shape = shape
#            space['n2'] = 1
            
            space['nbs'] = command['nbs']
            space['nbd'] = command['nbd']
            space['ac'] = command['ac']

            return space
        
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            
            shape = GetShapeInv3d( command, space )

            space.shape = shape
            
            if command['cpxIn']:
                pass
            
            else:
                space['data_type'] = 'float'
            return space
            
        @classmethod
        def constr( cls, command, space ):
            pass
#            cls.match( space, data_type='float' )
#            ndim = len( space.shape )
#            if len( space.shape ) != 3:
#                raise TypeError("3d curvelet transform got %sd data" %ndim)
            
        @classmethod
        def constr_adj( cls, command, space ):
            cls.match( space, data_type='complex' )

    class fdct( sfConverter ):
        """
        The fast discrete curvelet transform in-core with PYCT (sffdct)
        """
        @classmethod
        def map( cls, source, command ):
            command = cls.default_function( command, "fdct" )
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            command.kparams.pop( 'curveSpace' )

            return cls.pack( command )
    
        @classmethod
        def trans( cls, command, space, *spaces ):
            space['sizes'] = (space['n1'],space['n2'])

            if command.kparams['curveSpace'] != None:
                space['n1'] = command.kparams['curveSpace']['n1']
            space['n2'] = 1

            return space
            
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            space['n1'] = spaces[0]['sizes'][0]
            space['n2'] = spaces[0]['sizes'][1]

            return space

    class surf( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            command = cls.default_function( command, "surf" ) 
            command = cls.truefalseHelper( command )
            command.kparams.pop('inv', None )
            return cls.pack( command )
        
        @classmethod
        def map_adj( cls, source, command ):
            command = cls.default_function( command, "surf" ) 
            command = cls.truefalseHelper( command )
            
            if command.kparams.has_key( 'inv' ):
                if command.kparams['inv'] == 'n':
                    command.kparams.pop('inv', None )
                elif command.kparams['inv'] == 'y':
                    command.kparams.pop('adj', None )
            
            return cls.pack( command )

        @classmethod
        def trans( cls, command, space, *spaces ):
            surfSpaceChange( command, space, *spaces )
            return space

        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            surfInvSpaceChange( command, space, *spaces )
            return space
        
    class pad( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "pad" ) 
            cmd = cls.truefalseHelper( cmd )
            cmd.kparams.pop( 'adj' )
            return cls.pack( cmd )
        
        @classmethod
        def map_adj( cls, src, cmd ):
            cmd = cls.default_function( cmd, "window" ) 
            cmd = cls.truefalseHelper( cmd )
            cmd = padReplaceHelper( cmd , src.params )
            cmd.kparams.pop( 'adj' )
            cmd.kparams[ 'squeeze'] = 'n'
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            padHelper( command, space, *spaces )
            return space
        
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            padAdjHelper( command, space, *spaces )
            return space
        
    class mig( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "rtmig" ) 
            cmd = cls.truefalseHelper( cmd )
            cmd.kparams.pop( 'modelSpace' )
            cmd.kparams.pop( 'dataSpace' )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            space['n1'] = command.kparams['dataSpace']['n1']
            space['n2'] = command.kparams['dataSpace']['n2']
            space['d1'] = command.kparams['dataSpace']['d1']
            space['d2'] = command.kparams['dataSpace']['d2']
            return space

        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            space['n1'] = command.kparams['modelSpace']['n1']
            space['n2'] = command.kparams['modelSpace']['n2']
            space['d1'] = command.kparams['modelSpace']['d1']
            space['d2'] = command.kparams['modelSpace']['d2']
            return space

        @classmethod
        def constr( cls, command, space ):
            cls.match( space, data_type='float' )
            
        @classmethod
        def constr_adj( cls, command, space ):
            cls.match( space, data_type='float' )

    class dipfilter( sfConverter ):
        @classmethod
        def map(cls, src, cmd):
            cmd = cls.default_function( cmd, "dipfilter" ) 
            cmd.kparams.pop( 'adj' )
            return cls.pack( cmd )
        
        @classmethod
        def map_adj(cls, src, cmd):
            cmd.kparams.pop( 'adj' )
            c1, c2 = cls.split( cmd )
            
            c2 = cls.default_function( c2, 'conj' )
            c2 = cls.keep( c2, [] )
            c2.kparams['output'] = 'conj(input)'
            
            c1 = cls.default_function( c1, "dipfilter" ) 
            c2 = cls.default_function( c2, "math" ) 
            return cls.pack( [c1, c2] )
        
        @classmethod
        def constr( cls, command, space ):
            cls.match( space, data_type='complex' )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
            
    class pick( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "headercut" ) 
            cmd.kparams.pop( 'adj' )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space

        @classmethod
        def constr( cls, command, space ):
            mask_shape = command['mask'].params.shape
            exp_ndim = len(space.shape)-1
            ndim = len( mask_shape )
            assert ndim == exp_ndim , "mask must be one dimension less than the data - got %(ndim)s, expected %(exp_ndim)s" %vars()
            msg  =  "mask's n1 must equal data's n2, got mask n1=%s data n2=%s" 
            assert mask_shape[0] == space.shape[1], msg %(mask_shape[0],space.shape[1]) 
            pass

    class restrict( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "headerwindow" ) 
            cmd.kparams.pop( 'adj' )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            #n2 will equal the number of non-zero elements in mask
            #space['n2'] = 
            return space

    class sort( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            
            cmd = cls.default_function( cmd ) 
            cmd = cls.truefalseHelper( cmd )
            
            shape = cls.shape( src.params )
            if len(shape) is 0:
                pass
            elif len(shape) is not 1:
                prod = reduce(lambda a,b: a*b, shape)
                c1, c2 = cls.split( cmd )
                c1 = cls.default_function( c1, 'put' )
                lam = lambda i: c1.kparams.__setitem__( 'n%s' %i, 1)
                for i in range(len(shape)):
                    lam( i+1 )
                c1.kparams['n1'] = prod
                c1 = cls.keep( c1, ['n1', 'n2', 'n3', 'n4', 'n5'] )
                cmd = [c1,c2]
                
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
        
    class transp( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd )
            cmd.kparams.pop( 'adj', None )
            plane = cmd.kparams['plane']
            cmd.kparams['plane'] = '%s%s' %( plane[0], plane[1] )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, cmd, space, *spaces ):
            a, b = cmd.kparams['plane']
            
            na = "n%(a)s" %vars()
            nb = "n%(b)s" %vars()
            
            atmp = space[nb]
            space[nb] = space[na]
            space[na] = atmp
            return space
        
    class halfderiv( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "halfint" ) 
            cmd = cls.truefalseHelper( cmd )
            return cls.pack( cmd )
       
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space

    class cosinetrans( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            
            cmd.kparams.pop( 'adj', False )
            c1, c2 = cls.split( cmd )
            
            c1 = cls.default_function( c1, "cosft" )
             
                
            for i in range(src.params.ndim):
                c1.kparams["sign%s"%(i+1)] = '1' 
            
            c2 = cls.default_function( c2, "math" )
            size = src.params.size
            c2.kparams['output'] = "input/sqrt(2*%s)" %(size)
            return cls.pack( [c1,c2] )

        @classmethod
        def map_adj( cls, src, cmd ):
            
            cmd.kparams.pop( 'adj', False )
            c1, c2 = cls.split( cmd )
            
            c2 = cls.default_function( c2, "cosft" )
             
            c2.kparams.pop( 'adj', False )
                
            for i in range(src.params.ndim):
                c2.kparams["sign%s"%(i+1)] = '-1' 
            
            c1 = cls.default_function( c1, "math" )
            size = src.params.size
            c1.kparams['output'] = "input*sqrt(2*%s)" %(size)
            return cls.pack( [c1,c2] )

       
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
        
    class costaper( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "costaper" ) 
            cmd = cls.truefalseHelper( cmd )
            cmd.kparams.pop( 'adj', None )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space

    class taper( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "taper" ) 
            cmd = cls.truefalseHelper( cmd )
            cmd.kparams.pop( 'adj', None )
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
        
    class multpred( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "multpred" ) 
            cmd.kparams['adj'] = 0
            return cls.pack( cmd )
        
        @classmethod
        def map_adj( cls, src, cmd ):
            cmd = cls.default_function( cmd, "multpred" ) 
            cmd.kparams['adj'] = 1
            return cls.pack( cmd )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space

    class matrixmult( sfConverter ):
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
            if source.params['data_type'] == 'float':
                command = cls.default_function( command, "matmultn" ) #change to matmult for original
            elif source.params['data_type'] == 'complex':
                command = cls.default_function( command, "matmultn" ) #change to cmatmult for original
            #change all python True/False objects to 'y'/'n' strings
            command = cls.truefalseHelper( command )
            #alwas must return a CommandPack instance
            return cls.pack( command )
         
        @classmethod
        def trans( cls, command, space, *spaces ):
            mat = command.get_structure('mat').params
            space["n1"] = mat["n2"]
    #        space['data_type']='float'
            return space
        
        @classmethod
        def trans_adj( cls, command, space, *spaces ):
            mat = command.get_structure('mat')
            space["n1"] = mat.params["n1"]
    #        space['data_type'] = 'float'
            return space
        
        @classmethod
        def constr( cls, command, space ):
            mat = command.get_structure('mat')
            cls.match(space, n1=mat.params["n1"])
            cls.eqType(command, (space,mat.params) )
    
        @classmethod
        def constr_adj( cls, command, space ):
            mat = command.get_structure('mat')
            cls.match(space, n1=mat.params["n2"])
            cls.eqType(command, (space,mat.params) )
        
sffactory = rsfCommandFactory()
sffactory.addallfrom( all )
