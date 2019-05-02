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

class Storage(object):
    
    Dict = {}
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
    def __setitem__(self, name, value):
        self.Dict[name] = value
        
    def __getitem__(self,name):
        return self.Dict[name]

    def changeName(self,newname,name):
        try:
            data = self.Dict.pop(name)

            self.Dict[newname] = data
        except :
            print self.Dict
            raise
