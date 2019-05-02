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

from slimpy_base.Core.Interface.Structure import Structure as __Structure

class ADI( __Structure ):
    """
    Same as Structure except that this class has a dataContainer instance within
    """
    name = "Abstract_data_interface"
    
    def __init__( self, data_container ):
        self.__data_container = data_container
        self._scalar_lookup = {}
        

    def accept_command( self, command ):

        return super( ADI, self ).apply_command( self, command )
    
    def generateNew( self, cmd, *args, **kargs ):
        
        return super( ADI, self ).generateNew( self, cmd, *args, **kargs )
    
    def genData( self, cmd, *args, **kargs ):
        
        return super( ADI, self ).genData( self, cmd, *args, **kargs )

    def testCommand( self, cmd, *args, **kargs ):
        """
        returns the resulting space from applying the command but does not add the command to the tree
        """
        return super( ADI, self ).testCommand( self.getParameters(), cmd, *args, **kargs )
        


    def __str__( self ):
        """
        wrapper method to data_container.__str__
        """
        return "<SLIMpy.%s '%s'>" %( self.name, self.container )

    # Overloads print
    def __repr__( self ):
        return self.__str__()

    
    def getContainer( self ):
        return self.__data_container
    
    def getParameters( self ):
        
        return self.container.params
    
    container = property( getContainer )
    params = property( getParameters )
    
    def switchto( self, newSubclass, *p, **k ):
        """
        pass a class as the newSubclass arg and returns a new
        instance of the newSubclass with this structure's 
        """
        return newSubclass( self.container, *p, **k )
    
    def scalar_reduction( self, cmd, *args, **kargs ):
        """
        generate a Scalar from a command
        """
        scal_key = ( cmd, args, tuple( kargs.items() ) )
        if self._scalar_lookup.has_key( scal_key ):
            scal = self._scalar_lookup[ scal_key ]
            return scal
        else:
            scal = super( ADI, self ).scalar_reduction( self.container, cmd, *args, **kargs )
            self._scalar_lookup[ scal_key ] = scal 
            return scal
    
    def flush( self ):
        """
        force the commands in the graph to be run only to build this target.
        """
        
        super( ADI, self ).flush( self.getContainer() )
        
        return self

    def dependant( self ):
        return super( ADI, self ).dependant( self.getContainer() )
        
    def addBreakPoint( self ):
        """
        set the data from the interface as a needed
        resource without setting it as a target.
        """
        super( ADI, self ).addBreakPoint( self.getContainer() )
        
        return self
