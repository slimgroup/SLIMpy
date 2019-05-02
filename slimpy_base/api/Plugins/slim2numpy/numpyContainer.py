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

from slimpy_base.Core.Interface.containers import Abstract_data_container as __adc
from slimpy_base.utils.SLIMpyGlobal import GlobalVars as __slimglobal
from slimpy_base.utils.AbstractLog import log as __log
from Storage import Storage
from numpyCommands import numpyCommandFactory

_numpyContainer__log=__log
_numpyContainer__slimglobal=__slimglobal
_numpyContainer__adc=__adc
class numpyContainer(__adc):
    """
    rsf_data_container - to keep track of "out of core" vectors corresponding binary files on disk.
    """

    name = 'numpyDataContainer'
    globals = __slimglobal()
    log = __log()
    
    #check if numpy exists
    try: 
        import numpy
        isavalable = True
    except ImportError:
        numpy = None
        isavalable = False

        
    numpyCommandFactory = numpyCommandFactory()
    store = Storage()

    @staticmethod
    def isCompatibleWith(obj):
        return isinstance(obj, numpyContainer.numpy.ndarray)
    
    
    def __init__(self , data=None ,parameters=None,flow=False):

        if not data is None:
            
            name = self.genName()
            
            self.store[name] = data
            
            data = name
            
            
        __adc.__init__(self,data=data,parameters=parameters ,flow=flow)
    
    def getData(self):
        return self.store[self.getName()]     

        
    def isempty(self):
        
        return not self.store.Dict.has_key(self.getName())
        
    def parse(self,obj):
        
        return self.numpyCommandFactory.parse(obj)
    
    # __STR__ 
    def __str__(self):
        """Adds the current lib's suffix to the end of filename
        note: if no lib is set then self.plugin.suffix returns ''
        """
        return self.genName()
        
    def __repr__(self):
        return str(self)

    
    def getName(self):
        return self.data


    def plot(self):
        """
        plot returns the path the the plotfile
        """
        pass
    
    def setName(self,newname):
        """wrapped by SLIMpy.serial_vector.setname"""
        if self.isfull():
            self.store.changeName(newname,self.getName())
        else:
            self.data = newname



    

    def rm(self):
        """
        removes the file on disc
        """
        print >> self.log(10), "call to rm %s" %self.genName()
    
    def readattr(self):
        
        data  = self.getData()
        file_dict = {}
        
        
        for i , n in enumerate(data.shape):
            file_dict['n%(i)s'] = n
        
        return file_dict 
            
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
    
