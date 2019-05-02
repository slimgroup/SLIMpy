"""
Class to be used by plug-ins
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


from slimpy_base.Core.Command.CommandPack import CommandPack
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Core.Interface.PSpace import voidSpace

__env__ = InstanceManager()

class ConstraintFunctions( object ):
    """
    Class containing classmethod methods to 
    use in the constraint definitions of 
    plug-in commands
    """
    
    @classmethod
    def match( cls, params, *keys, **kargs ):
        """
        match args to params and if keyword args are specified
        match the values as well 
        """
        msg = "Space does not have key %(key)s" 
        
        for key in keys:
            if not params.has_key( key ):
                raise TypeError( msg %vars() )
        
        for key in kargs:
            if  not  params.has_key( key ):
                raise TypeError( msg %vars() )
            
            elif params[key] != kargs[key]:
                raise TypeError( "space restriction space[%s]=%s failed, got =%s " 
                                 %(repr(key) , kargs[key], params[key] ) )
            

    @classmethod
    def eqType( cls, command, params ):
        """
        test if all of the spaces given are of
        equal shape.
        """
        
        def assert_has_data_type( spc ):
            if spc.has_key( 'data_type' ):
                pass
            else:
                msg  = "The parameter object %(spc)s does not have a data_type"
                raise TypeError( msg %vars() )
        
        assert_has_data_type( params[0] )
        
        pre = params[0]["data_type"]
        for s_spc in params:
            assert_has_data_type( s_spc )
            new = s_spc['data_type']
            if not pre  == new:
                msg = "need equal data type: %(pre)s != %(new)s"
                raise TypeError( msg  %vars() )
    
    @classmethod
    def shape( cls, space ):
        n_val = 1
        key = "n%(n_val)s" %vars()
        shp = []
        while space.has_key( key ):
            shp.append( space[key] )
            n_val += 1
            key = "n%(n_val)s" %vars()
            
        n_val -= 2
        while n_val and shp[n_val] == 1:
            shp.pop()
            n_val -= 1
        return shp

    @classmethod
    def eqShape( cls, command, params ):
        """
        raise a TypeError if the param/Space instances in params
        are not of equal type
        """
        
        
        shapes = [ par.shape for par in params ]
        
#        shapes.append( cls.shape(params) )
            
        z = zip( *shapes )
        for l in z:
            item = l[0]
            for i in l:
                if not item == i:
                    raise TypeError( "Shape Mismatch %s" % " != ".join(map(repr,shapes)) )
                
        return 
    
        
    @classmethod
    def eqVectorType( cls, *spaces ):
        """
        TODO: 
        """
        vt = spaces[0].vector_type
        for s in spaces:
            if not s.vector_type == vt:
                raise TypeError( "TODO: doc" )
        return True
    
    
    
class MapFunctions( object ):
    """
    methods for helping the mapping of generic SLIMpy 
    commands to a specific plug-in command
    """

    @classmethod
    def pack( cls, command , stdin=True, stdout=True ):
        """
        pack a source, command and target into
        a CommandPack instance
        @return: CommandPack instance
        """
        if isinstance( command, (tuple, list) ):
            comm = command
        else:
            comm = [command]
        
        return CommandPack(  comm, stdin, stdout )
    
#    @classmethod
#    def _replace_sources(cls,comm):
#        for i,par in enumerate(cmd.params):
#            if isinstance(par, _source):
#                pass
#
#        return []
#    
#    @classmethod
#    def _replace_targets(cls,comm):
#        return []
# 
        
    
    @classmethod
    def keep( cls, command, keywords ):
        """
        keeps only the  keywords in cmnd
        """
        for key in command.kparams.keys():
            if key not in keywords:
                command.kparams.pop( key )
        
        return command
    @classmethod
    def discard( cls, command, keywords ):
        """
        discards all of keywords found in cmnd
        """
        for key in keywords:
            command.kparams.pop( key, None )
        
        return command
    
    @classmethod
    def keywordmap( cls, command, Dict ):
        
        """
        maps keys in the kparams dictionary to the
        the value of the key in the mapDict
        note that if the key 'a' maps to 'b'
        and 'b' is already defined then the behavior becomes unpredictable
        
        """
#        k = {}
        kparams = command.kparams
        for key in kparams.keys():
            if Dict.has_key( key ):
                kparams[ Dict[key] ] = kparams[key]
                kparams.pop( key )
                
        return command
    
    @classmethod
    def split( cls, command ):
        """
        split the command into 2 identical copies
        """
        command1 = command.copy()
        command2 = command.copy()
        return command1, command2
    
    @classmethod
    def truefalseHelper( cls, command, true='y', false='n' ):
        """
        convert python boolean True/False values
        to 'y'/'n' strings 
        """
#        command = command.copy()
        kparams = command.kparams
        
        for key in kparams.keys():
            if kparams[key] is True:
                kparams[key] = true
            elif kparams[key] is False:
                kparams[key] = false
                
        return command
        
    
class TransformFunctions( object ):
    """
    Helper methods for transformation of spaces 
    to the resulting spaces of a command
    """
    @classmethod
    def change( cls, space, *d, **k ):
        """
        update the space with dict d or keyword arguments
        """
        space.update( *d, **k )
        return space

class Converter( ConstraintFunctions, MapFunctions, TransformFunctions ):
    """
    class is subclass of 'ConstraintFunctions', 
    'MapFunctions' and 'TransformFunctions'
    for one convenience class
    
    """
    def __init__( self ):    
        pass
    
    @classmethod
    def apply_command( cls, command, source):
        strict_check = __env__['slimvars']['strict_check']
        
#        if self.sglobals['strict_check'] == 0:
#            pass
        if strict_check > 0:
            cls.constrain( command, source.params )
        
        # Now that the data has been parsed we can get the new 
        # space the data formed by that command
        # is in
        newspace = cls.transform( command, source.params )
        
        compack =  cls.convert( source, command )
        
        if strict_check > 1:
            if isinstance( newspace, voidSpace ):
                msg = ( "'strict_check >= 2' prevents commands "
                        "from returning voidSpace\n"
                        "command '%(command)s' returned voidSpace" %vars() )
                raise Exception( msg )
        # Make a new container that knows about its space
        newcontainer = newspace.makeContaner( command=command )
        # append the command to the graph to be executed later 
        # by a flush command
                
        return compack, newcontainer

    @classmethod
    def convert( cls, source, command  ):
        """
        Used internally by SLIMy.Core.Interface sub-package
        calls regex - map.* - of subclasses  
        """
        method = cls.getmatch( command, 'map_' )
        result = method( source, command.copy() )
        if not isinstance( result, CommandPack ):
            msg = "converter function '%(method)s' did not return a CommandPack instance " % vars()
            raise Exception( msg )
        return result

    @classmethod
    def transform( cls, command, space ):
        """
        Used internally by SLIMy.Core.Interface sub-package
        calls regex - trans.* - of subclasses  
        """
        space = space.copy( )
        spaces = [ space ] + command.get_source_spaces( )
        method = cls.getmatch( command, 'trans_' )
        result = method( command, space, *spaces )

        if result is None:
            raise TypeError( "'$(method)s' did not return a Parameter object, got '%(result)s'" %vars() )
        return result
    
    @classmethod    
    def constrain( cls, command, Space ):
        """
        Used internally by SLIMy.Core.Interface sub-package
        calls regex - constr.* - of subclasses  
        """

        method = cls.getmatch( command, 'constr_' )
        return method( command, Space )

    
    @classmethod
    def map( cls, source, command ):
        """
        default mapping 1 to 1
        """
        return CommandPack(  [command]  )
    
    @classmethod
    def trans( cls, command, space, *spaces ):
        """
        default trans, returns voidSpace
        """
        from slimpy_base.Core.Interface.PSpace import voidSpace
        return voidSpace( space.plugin )
    
    
    @classmethod
    def getmatch( cls, command, prefix ):
        """
        helper method to match 
        """
        lp = len( prefix )
        isp = lambda item: item[lp:].split( '_' ) 
        
        items = [ isp( item ) for item in dir( cls ) 
                     if item.startswith( prefix ) ]
        
#        all_in = lambda keys, comm : bool(
#                  [ True for key in keys if key in comm and comm[key] ] )
        
        lcmp = lambda a1, b1: cmp( len( a1 ), len( b1 ) )
        items.sort( lcmp, reverse=True )

        for func_keys in items:
#            print 'key',keys,'command',command,allin(keys,command)
            
            if all_in( func_keys, command ):
                method = prefix + "_".join( func_keys )
                return getattr( cls, method )
        
        return getattr( cls, prefix[:-1] )

def all_in( func_keys, command ):
    """
    returns true if all of the strings in func_keys
    are also in command and the values of the keys are 
    True --or-- if command does not have the key but 
    the value is true in  SLIMpy.GlobalVars
    """
    slimvars = __env__['slimvars']
    for fkey in func_keys:
        if fkey in command:
            if command[fkey]:
                continue
            else:
                return False # command[fkey] == False
        elif fkey in slimvars and slimvars[fkey]:
            continue 
        else:
            return False
        
    return True
                
            


