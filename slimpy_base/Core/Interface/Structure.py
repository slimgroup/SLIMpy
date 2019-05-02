"""
Interface of Graph and Vector and Linear operator classes 
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

from slimpy_base.Core.Command.Command import Command as general_command
from slimpy_base.Core.Command.CommandPack import CommandPack
from slimpy_base.Core.Interface.node import Source, Target
from slimpy_base.Core.User.Structures.Scalar import  Scalar
from slimpy_base.Environment.InstanceManager import InstanceManager
from traceback import extract_stack, format_list
from slimpy_base.Core.Interface.PSpace import voidSpace


class Structure( object ):
    """
    Structure class
    SLIMpy is set up such that there is a hierarchy of 
        + Structure
        |--+ Graph
        |--+ Container
        |  |--+ Data
          
    This is because we need the abstraction at each level
    The container provides a constant interface for each type of data for the
    structure to use.
    The structure knows about the standard container interface and 
    Graph and interfaces the two.
    structure is designed to be the super class for all of the SLIMpy concrete 
    data class (e.g., Vector, Linear Operator, Array, ...)
    """
    __scalarcount = 0
    name = "Sructure"

    env = InstanceManager()
    
    @classmethod
    def generate_command( cls, cmnd, *args, **kargs ):
        """
        return a new slimpy_base.Command.command instance
        """
        # Make a command from the command maker factory
        # if the command cmnd is recognized then it can have a few attributes 
        # such as transforms and .. packed in with it
        # otherwise it will return a new command
        command = general_command( cmnd, None, *args, **kargs )

        if cls.env['slimvars']['keep_tb_info']:
            stack = extract_stack( )
            st_list  = format_list( stack[:-3] )
            command.tb_info = "".join(st_list)

        return command
    
    @classmethod
    def apply_command(cls,structure, command ):
        
        container = structure.container
        converter = container.get_converter( command )
        compack, newcontainer = converter.apply_command( command, container )
        
        compack.source = container
        compack.target = newcontainer
        
        cls.env['graphmgr'].graphAppend( compack )
        
        return newcontainer
    
    @classmethod
    def testCommand( cls, space, cmnd_tag, *args, **kargs ):
        """
        Returns the resulting space from applying a command
        """
        command = cls.generate_command( cmnd_tag, *args, **kargs )
        
#        data_container = space1.makeContaner( command=command )
        converter = space.plugin.get_converter( command )
        
        return converter.transform( command, space )
    
    @classmethod
    def generateNewWithSpace( cls, data, space, cmd, *args, **kargs ):
        """
        Generate a new Structure instance (note: that the new instance will be the current subclass)
        Also see: genData
        """
        # generate a new Command instance from the given parameters
        command = cls.generate_command( cmd, *args, **kargs )
        
        # Get a new data container
        try:
            newdata = cls.apply_command( data, command, space )
        except TypeError, msg:
            if not cls.env['slimvars']['WARNCONFLICT']:
                raise
            else:
                print "Warning", msg
        
        # wrap the new data in the current Structure [sub]class
        return data.__class__( newdata )
    
    @classmethod
    def generateNew( cls, data, cmd_tag, *args, **kargs ):
        """
        Generate a new Structure instance (note: that the new instance will be the current subclass)
        Also see: genData
        """
        # generate a new Command instance from the given parameters
        command = cls.generate_command( cmd_tag, *args, **kargs )
        
        # Get a new data container

        newdata = cls.apply_command( data, command )
        
        # wrap the new data in the current Structure [sub]class
        return data.__class__( newdata )
    
    @classmethod
    def genData( cls, data, cmd, *args, **kargs ):
        """
        Same as generateNew. However genData returns a dataContainer instance
        """

        command = cls.generate_command( cmd, *args, **kargs )
        
        return cls.apply_command( data, command )
                
    @classmethod
    def AppendToGraph( cls, container1, cmnd, container2 ):
        """
        Append to the current graph in the keystone Class
        """
        raise  DeprecationWarning( "do not use this function" )
#        cls.graphmgr.graphAppend( container1, cmnd, container2 )
    
#    # TODO: not started yet  
#    def genScalar( cls, container, cmd, *args, **kargs ):
#        """
#        generate a Scalar from a command
#        """
#        Structure.__scalarcount += 1
#        sc = Structure.__scalarcount
#        try:
#            Structure.flush( cls, container )
#        except AssertionError: # IGNORE:W0704
#            # if the flush fails form assertions error assume
#            # that the container has not been in entered into the 
#            # graph yet and does not need flushing
#            pass
#        
#        x = ", ".join( map( str, args ) )
#        y = ", ".join( [ "%s=%s" %(key,val)   for key,val in  kargs.iteritems() ] )
#        if x:
#            z = ", ".join( [x, y] )
#        else:
#            z =y 
#            
#        runtype = cls.env['slimvars']['runtype']
#        
#        if runtype == 'dryrun':
#            answer =  scalar( "${SCALAR%(sc)02d}"%vars() )
#        else:
#            answer = container.genScalar( cmd, *args, **kargs )
#            
#        print >> cls.log( 1 ) , "%(answer)s = %(cmd)s(%(container)s, %(z)s)"  %vars()
#        return answer
    
    @classmethod
    def scalar_reduction(cls, container, tag, *args, **kargs ):
        """
        generate a Scalar from a command
        """
        scalar_methods = container.scalar_methods
        
        scmd = scalar_methods.get_command( tag )
        
        scalar = Scalar( )
        cont = Source( container )
        scal = Target( scalar )
        
        if cls.env['slimvars']['use_scalar_obj']:

            command = general_command( tag, None, cont, scal, *args, **kargs )
            # set command
            command.func = scmd
            compack = CommandPack( [ command ], None, None )
            cls.env['graphmgr'].graphAppend( compack )
        else:
            scalar = scal.data
        
        return scalar
    @classmethod
    def genScalar( cls, container, tag, *args, **kargs ):
        """
        generate a Scalar from a command
        """
        return cls.scalar_reduction(container, tag, *args, **kargs)
    
    @classmethod
    def source_or_num( cls, obj ):
        """
        struc.source_or_num( obj ) -> result
        returns a source if obj is a SLIMpy scalar, or returns obj if obj is 
        a number 
        """
        if isinstance( obj, Scalar ):
            return Source( obj )
        elif hasattr( obj, 'container' ):
            return Source( getattr( obj, 'container' ) )
        else:
            return obj
    
    @classmethod
    def flush( cls, data ):
        'see GraphManager.flush'
        cls.env['graphmgr'].flush( data )
    
    @classmethod
    def dependant( cls, container ):
        """
        prints a dependency table for
        container
        """
        v = id( container )
        return cls.env['graphmgr'].printInvAdj( v )
         
    @classmethod
    def addBreakPoint( cls, container ):
        """
        add a breakpoint in the graph
        container will always be build, even if it 
        breaks a pipe
        """
        cls.env['graphmgr'].addBreakPoint( container )
    
    # for consistency in boolean functions
    def __nonzero__( self ):
        """
        always true
        """
        return 1

    def __repr__( self ):
        return "<SLIMpy: " + self.__class__.__name__ + ">"
    
