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

"""
Vector Interface to RSF.
"""

raise NotImplementedError("Sorry, not finneshed yet")

from slimpy_base.Core.Interface.containers import Abstract_data_container as __ADC

def addAll():
    pass

def get_container():
    return numarray_data_container


class numarray_data_container(__ADC):
    """
    rsf_data_container - to keep track of "out of core" vectors corresponding binary files on disk.
    """

    name = "numarray"
    isavalable = False

    @staticmethod
    def isCompatibleWith(obj):
        return False

    def __init__(self , data ,istmp=False,full=False,flow=False):
        pass
        
    def isempty(self):
        pass
        
    
    def parse(self,obj):
        pass

   
    # __STR__ 
    def __str__(self):
        pass
        
    def __repr__(self):
        pass

    def path(self):
        pass

    def base(self):
        pass
    
    def plot(self):
        pass
        
    def setname(self,newname):
        pass

    def remove(self):
        pass

    def readattr(self):
        pass
            
    def readbin(self,start=0,shape=(-1,1)):
        pass
    
    def writebin(self,data,start=0,size=0):
        pass
    def book(self,header):
        pass


    def writeattr(self,header,vector_dict,file_dict):
        pass
    
    def write(self,header,data,book):
        pass
        
    def getfilepos(self,*index):
        pass
    
    
