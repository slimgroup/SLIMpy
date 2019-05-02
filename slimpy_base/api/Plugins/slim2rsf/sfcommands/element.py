"""
Element-wise command converters
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
from slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter import sfConverter
from os.path import join
from slimpy_base.Core.Command.Drivers.ooc_driver import OutOfCoreDriver
from slimpy_base.Core.Interface.node import Source
from pdb import set_trace

class sfmathFixture( sfConverter ):
    mathstr = ""
    
    @classmethod
    def funcmap( cls ):

        sfmath = join( cls.env['slimvars']['RSFBIN'], 'sfmath' )
        return OutOfCoreDriver( sfmath )

    @classmethod
    def map( cls, source, command ):
        
        command = cls.default_function( command, "math" )
        command = cls.place_adder( command )
        
        command = cls.keep( command, ['output', 'vec'] )
        command = cls.mathhelper( command )
        
#        source,command = cls.fill_unusedsource( source,command)
        
        return cls.pack(  command )
    
            
    @classmethod
    def mathhelper( cls, command ):
        
        output = cls.mathstr
        kparams = command.kparams
        params= command.params
        
        if kparams.has_key( 'vec' ):
            if '${val}'in output:
                kparams['output'] = output.replace( "${val}", 'vec' )
        else:
            if '${val}'in output:
                val = params.pop()
                if isinstance(val, Source):
                    command.add_other_dep( val )
                    val = val.data
                kparams['output'] = output.replace( "${val}", str( val ) )
            else:
                kparams['output'] = output
                
        return command
    
    @classmethod
    def constr( cls, command, *params ):
        cls.eqShape(command,  params )
        cls.eqType( command, params )
        flt_or_cmpx = params[0]['data_type'] in ['float','complex']
        assert flt_or_cmpx , "data must be either 'float' or 'complex'"
        return 
    
    @classmethod
    def trans( cls, command, space, *Spaces ):
        return space
    
class all( object ):
    """
    container class for converters
    """
    
    class radd( sfmathFixture ):
        mathstr = 'input+${val}'
    class add( sfmathFixture ):     
        mathstr = '${val}+input'
    class mul( sfmathFixture ):      
        mathstr = '${val}*input'
    class weightoper( sfmathFixture ):      
        mathstr = '${val}*input'
    class rmul( sfmathFixture ):    
        mathstr = 'input*${val}'
    class sub( sfmathFixture ):      
        mathstr = 'input-${val}'
    class rsub( sfmathFixture ):     
        mathstr = '${val}-input'
    class div( sfmathFixture ):      
        mathstr = 'input/${val}'
    class rdiv( sfmathFixture ):     
        mathstr = '${val}/input'
    class neg( sfmathFixture ):     
        mathstr = '-input'
    class abs( sfmathFixture ):    
        mathstr = 'abs(input)'
    class pow( sfmathFixture ):     
        mathstr = 'input^${val}'
    class conj( sfmathFixture ):     
        mathstr = 'conj(input)'
        
    class real( sfConverter ):
        @classmethod
        def trans( cls, command, space, *spaces ):
            #InSpaceConstr =  Constr(match=Constr.match(data_type='complex') ),
            space = cls.change( space, data_type='float' )
            return space
         
    class create( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            
            c1, c2 = cls.split( command )
            c1 = cls.default_function( c1, 'math' )
            c1 = cls.keywordmap( c1, {'out':'output', 'data_type':'type'} )
            c1 = cls.keep( c1, ['output', 'type', 'n1', 'n2', 'n3', 'n4', 'n5'] )
            
            c2 = cls.default_function( c2, 'put' )
            c2 = cls.discard( c2, ['Curvelet', 'out', 'esize', 'data_format', 'data_type', 'n1', 'n2', 'n3', 'n4', 'n5'] )
            
            # Dirty fix to touch on the subject that we can't create spaces that include vector headers.
            # This will see if the parameter starts with a (, if it does, it assumes if's a vector header
            # and will remove all the '(' ')' and whitespace from the key value. This will produce the
            # right vector header for the RSF file.
            # It leaves the original space as is.
            clist = [c1]
            if c2.kparams:
                for key in c2.kparams:
                    if c2[key].__str__()[0] == "(":
                        c2[key] = c2[key].__str__().strip('()').replace(' ','')
                clist.append( c2 )

            return cls.pack( clist )

    class create_noise( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            
            c1, c2 = cls.split( command )
            c3, c4 = cls.split( c2 )
            
            c1 = cls.default_function( c1, 'math' )
            c1 = cls.keywordmap( c1, {'out':'output', 'data_type':'type'} )
            c1 = cls.keep( c1, ['output', 'type', 'n1', 'n2', 'n3', 'n4', 'n5'] )
            
            clist = [c1]
            
            c2 = cls.default_function( c2, 'put' )
            c2 = cls.discard( c2, ['Curvelet', 'out', 'esize', 'data_format', 'data_type', 'n1', 'n2', 'n3', 'n4', 'n5', 'mean', 'seed'] )
            
            if c2.kparams:
                for key in c2.kparams:
                    if c2[key].__str__()[0] == "(":
                        c2[key] = c2[key].__str__().strip('()').replace(' ','')
                clist.append( c2 )
                
            data_type = c1['type']
            c1['type'] = 'float'
            c1['output'] = 0
            
            c4 = cls.keep( c4, ['mean','seed'] )
            c4 = cls.default_function( c4, 'noise' )
            clist.append(c4)
            
            if data_type == 'complex':
                c3 = cls.keep( c3, [] )
                c3 = cls.default_function( c3, 'rtoc' )
                clist.append(c3)
            
            
            return cls.pack(  clist )
            
    class fdct2vects( sfConverter ):
        @classmethod
        def map( cls, source, command ):
            command = cls.default_function( command )
            command = cls.truefalseHelper( command )
            cInSpace = command.kparams.pop('cInSpace')
            sizes,cparams = gen_sizes_file(command, cInSpace )
            
            command.kparams.pop('nba')
            command.kparams.pop('nbs')
            command.kparams.pop('ac')
            
            wedgconstr = command.kparams.pop( 'wedgconstr' )
            if command.kparams['mode'] == 'zang':
                command.kparams['nba2zL'] = wedgconstr[0]
                command.kparams['nba2zR'] = wedgconstr[1]
            
            return cls.pack(  command, stdin=sizes )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            space['data_type'] = "float"
            return space
    
    class thr( sfConverter ):
        @classmethod
        def constr( cls, command, *Spaces ):
            if command.kparams.has_key( 'thr' ):
                assert command.kparams['thr'] > 0
            assert command.kparams.has_key( 'mode' )
            assert command.kparams['mode'] in ['hard', 'soft', 'nng']
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space
    
    class noise( sfConverter ):
        @classmethod
        def trans( cls, command, space, *spaces ):
            return space

    class cmplx( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "cmplx" ) 
            return cls.pack(  cmd, stdin=None )
        
        @classmethod
        def trans( cls, command, space, *spaces ):
            #InSpaceConstr =  Constr(match=Constr.match(data_type='float')
            space = cls.change( space, data_type='complex' )
            return space
        
    class reshape( sfConverter ):
        
        @classmethod
        def constr( cls, command, *Spaces ):
            assert command.kparams.has_key( 'shape' )
            
            prod = lambda seq: reduce(lambda x,y:x*y, seq ,1 )
            
            assert prod( command['shape'] ) == prod( Spaces[0].shape )
           
        @classmethod 
        def trans( cls, cmd, space, *spaces ):
            d = lambda val,i,dct: dct.__setitem__('n%s' %i,val) 
            shape = cmd.kparams['shape']
            [ d(val,i+1,space) for i,val in enumerate(shape ) ]
            return space 

        @classmethod
        def map( cls, src, cmd ):
            d = lambda val,i,dct: dct.__setitem__('n%s' %i,val) 
            cmd = cls.default_function( cmd, "put" )
            shape = cmd.kparams.pop('shape')
            [ d(val,i+1,cmd.kparams) for i,val in enumerate(shape ) ] 
            return cls.pack(  cmd )
        
    class cat( sfConverter ):
        @classmethod 
        def trans( cls, cmd, space, *spaces ):
            
            axis = cmd.kparams['axis']
            nX = "n%s" %(axis)
            nXval = sum( [spc[nX] for spc in spaces ] )
            space[ nX ] = nXval
            return space 

    class spike( sfConverter ):
        @classmethod
        def map( cls, src, cmd ):
            cmd = cls.default_function( cmd, "spike" )
            
            k = cmd.pop_kw('k',None)
            if k:
                for X,kX in enumerate(k):
                    cmd['k%s' %(X+1)] = kX+1
            
            return cls.pack(  cmd )

        @classmethod 
        def trans( cls, cmd, space, *spaces ):
            return space 

sffactory = rsfCommandFactory()
sffactory.addallfrom( all )
