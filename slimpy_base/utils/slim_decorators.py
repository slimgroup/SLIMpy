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



def depends_on( *deps ):
    def depends_on_decorator( func ):
        if not hasattr(func, '__additional_dependancies__'):
            setattr(func, '__additional_dependancies__' , list(deps) )
        else:
            added_deps = getattr(func, '__additional_dependancies__')
            added_deps.extend( deps )
            
        return func 
    return depends_on_decorator

def depends_on_functions( *deps ):
    def depends_on_decorator( func ):
        if not hasattr(func, '__function_dependancies__'):
            setattr(func, '__function_dependancies__' , list(deps) )
        else:
            added_deps = getattr(func, '__function_dependancies__')
            added_deps.extend( deps )
            
        return func 
    return depends_on_decorator
    
