"""
load pluging from enclosed folders
does not import on a NotImplementedError
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

import os
#from slimpy_base.utils.Logger import Log

class loader( object ):
    """
    Class to load pluging from enclosed folders,
    replaces same as import * as list
    """
#    log = Log()
    
    def __init__( self ):
        pass
    
    def load( self ):
        """
        reutrns a dictionary of modules
        """
            #returns a lis of modules in parseLIB
        plugins = {}
        
        
        modnames = self.getModules()
        warn = ( "Warning: Plugin module `%(module)s` could not be loaded: "
                 "to debug try importing the modual on its own\n\t--%(msg)s" )
        for module in modnames:
            try:
                mod = __import__( module, globals(), locals() )                
#                mod.addAll()
                
                plugins.update( mod.get_containers() )
                
            
            except NotImplementedError:
                continue
            
        return plugins
    
    def getModules( self ):        
        """
        Returns the names of all of the modules in the 
        directory of this file
        
        """
        dir =  os.path.dirname( __file__ )

        files =  os.listdir( dir )

        List = []
        for file in files:
            path = os.path.join( dir, file ) 
  
            if ( os.path.isfile( path ) 
                and path.endswith( '.py' ) 
                and not path.endswith( "__init__.py" )
                and not path == __file__.split( '.py' )[0]+".py" ) :
                List.append( file.split( '.py' )[0] )

                
            elif os.path.isdir( path ):
                if os.path.isfile( os.path.join( path, '__init__.py' ) ):
                    List.append( file )

                    
        return List
