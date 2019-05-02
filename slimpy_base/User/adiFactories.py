"""
Factory Classes to create Structure instances from actual data

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

from slimpy_base.Core.Interface.AbstractDataInterface import ADI
from slimpy_base.Core.Interface.ContainerBase import contain
from slimpy_base.Core.User.Structures.serial_vector import  Vector
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.utils.Profileable import Profileable,note


class VectorFactory( object ):
    """
    factory class to contain data into a subclass of 
    dataContainer and put that into a vector
    """
    
    __metaclass__ = Profileable
    """
    Class used as a convinience method to contain various data formats and
    return a vector
    """
#    graphmgr = GraphManager()
    env = InstanceManager()
    
    @note("class is initialized by user")
    def __init__( self ):
        """
        nothing done in the init
        """
        pass
    
    def __call__( self, data ):
        """
        contain data into a subclass of dataContainer and put that into a vector
        """
        if isinstance(data, ADI):
            newdata = data.container

        else:
            newdata = contain( data )
            self.env['graphmgr'].add_source( newdata )

        return Vector( newdata )
    
    def __str__(self):
        return "<SLIMpy function: vector>"
    
    def __repr__(self):
        return "SLIMpy.VectorFactory( )"
    

