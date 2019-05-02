"""
rsfAddCommands class to chain together commands into a pipe
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


from slimpy_base.Core.Command.Command import Command
from slimpy_base.Core.Command.Drivers.remote_pipe import RemoteDriver
from slimpy_base.Core.Interface.ContainerBase import DataContainer 

class rsfAddCommands( object ):
    """
    class to add two commands together
    """
    ERRORMSG1 = ( "add commands must recieve "
                 "either a datacontainer or a Command"
                 "\ngot a %s" )
    
    ERRORMSG2 = "add commands must recieve either a DataContainer or a Command"
    
    def __init__( self ):
        pass
    
    
    def __call__( self, c1, c2 ):
        """
        add c1 and c2 together to form a pipe command
        @return: a  multiDriver instance
        """
        if isinstance( c1, DataContainer ):
            driver = RemoteDriver()
            
            if isinstance( c2, Command ):
                driver.setSource( c1 )
                driver.addCommand( c2 )

            else:
            
                raise TypeError(self.ERRORMSG2)

        elif isinstance( c1, Command ):
            
            
            if isinstance( c1.func, RemoteDriver ):
                driver = c1.func
            else :
                driver = RemoteDriver()
                driver.addCommand( c1 )
            
            if isinstance( c2, DataContainer ):
                driver.setTarget( c2 )
            
            elif isinstance( c2, Command ):
                driver.addCommand( c2 )
                
            elif c2 is None:
                pass
            else:
                raise TypeError( self.ERRORMSG1 % type( c2 ) )
        else:
        
            raise TypeError( self.ERRORMSG1 % type( c2 ) )
        
        com = Command( "_multi_", self )
        com.func = driver
        
        return com
            
        
        
    
    
