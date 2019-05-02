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

from slimpy_base.Core.Command.Converter import Converter
from sfcommands.sfConverter import sfConverter

class rsfCommandFactory(object):
    shared_state = {}
    converters = {}
    
    def __init__(self):
        self.__dict__ = self.shared_state
    
    def add(self,class_,name=None):
        if name is None:
            name = class_.__name__        
        self.converters[ name ] = class_
    
    def addallfrom(self,all):
        for classes in dir(all):
            class_ = getattr( all,classes )
            try:
                is_con =  issubclass(class_, Converter)
            except:
                is_con = False
            if is_con:
                self.converters[ class_.__name__ ] = class_
    
    def __setitem__(self,name,val):
        self.add(val, name)
        
    def __getitem__(self,name):
#        key = command.func
        converters = self.converters
        if converters.has_key( name ):
            return converters[ name ]
        else:
            return sfConverter
                 
