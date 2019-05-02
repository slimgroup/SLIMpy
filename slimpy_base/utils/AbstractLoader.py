"""
The loader module provieda a funtion to load a dictionary into 
the local and global memory
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


class loader(object):
    """
    Load the data in Loader.g and Loader.l into 
    the global and local namespce
    """
    g = {}
    l = {}
    
    def load(self,locals,globals):
        """
        
        pass the parameters locals() and globals()
        
        """
        locals.update(self.l)
        globals.update(self.g)
        
        
