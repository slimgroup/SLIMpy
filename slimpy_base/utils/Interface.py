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


class InterfaceType( type ):
    
    interface_methods = {}
    
    def __new__( cls, *p, **kw ):
        
        implementation = type.__new__( cls, *p, **kw )
        
        cls.check_implements( implementation )
        
        return implementation
         
    @classmethod
    def check_implements( cls , implementation ):
        
        for key, check in cls.interface_methods.items():
            
            if not hasattr( implementation, key ):
                raise InterfaceMustImplement( key )
            
            attr = getattr( implementation, key )
            
            if check is not None:
                check_result = check( attr )
                if not check_result:
                    raise InterfaceMustImplement( "%s is not correctly implemented" %key )
        
        return 

class InterfaceMustImplement( Exception ): pass 

