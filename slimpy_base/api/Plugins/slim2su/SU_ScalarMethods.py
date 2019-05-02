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


class SU_ScalarMethods( object ):
    
    
    def __init__(self, cmd):
        
        if not  hasattr(self, cmd):
            name = self.__class__.__name__
            raise TypeError('No Scalar command "%s" in %s ' %(cmd,name) )
        self._command_name = cmd
        
    def __call__(self, container, scalar, *args, **kw):
        '''
        only non classmethod calls methoc given by self._command_name
        '''
        if not hasattr(self, "_command_name"):
            raise AttributeError("scalar class not initialized")
        
        cmd = self._command_name
        attr = getattr( self, cmd )
        attr( container, scalar, *args, **kw )
      
