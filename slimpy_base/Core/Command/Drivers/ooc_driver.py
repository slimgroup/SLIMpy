
"""
     

Driver function tracks dependencies and
parses slimlib objects


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

#from slimpy_base.utils.Logger import Log
from slimpy_base.Core.Interface.node import Node
#from slimpy_base.utils.hashTable import HashTable

from slimpy_base.Environment.InstanceManager import InstanceManager
#from slimpy_base.Core.Command.Drivers.multipipe import FileOut, FileIn, FileInOut
from os import system
#from slimpy_base.utils.GlobalVars import GlobalVars


class OutOfCoreDriver( object ):
    """
    takes a command string of an executable file as 
    an argument and then can be used as a callable 
    function with the 'Command' class  
    """
    
    
    def __init__( self, cmndstr ):
        self.__comndstr = cmndstr
        
        return
    
    def __str__( self ):
        return self.__comndstr
    
    def __repr__( self ):
        return self.__comndstr
    
    def getCmnd( self ):
        return self.__comndstr
    
    def __call__( self, *p, **k ):
        """
        call performs a system call and execute the file
        given by self.getCmnd() passed all of args and kargs as
        string parameters on the command line
        """
        print self.format( p, k )
        return system( self.format( p, k ) )
    
    def format( self, nodename, params, kparams ):
        """
        creates a dictionary with the key "cmnd" 
        which is a string of all the 
        """
        env = InstanceManager()
        
        table = env['table']
        l = lambda a, b : str( a )+'="'+str( b )+'"'
        
        cs = [ self.getCmnd() ]
        push = cs.append
        
        for par in params:
            if isinstance( par, Node ):
                src = table[par.getID()]
                par = src.get_data( nodename )
            push( par )
            
        for key, val in kparams.items():
            if isinstance( val, Node ):
                val = val.get_data( nodename )
            push( l( key, val ) )
#        p = " ".join(map(str, params))
#        k =  " ".join(map(l , kparams.items()))
#        cs = " ".join([self.getCmnd(),p, k])

        return " ".join( map(str,cs) )

          
