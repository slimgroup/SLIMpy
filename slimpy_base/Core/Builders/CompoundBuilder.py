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

from slimpy_base.Core.Builders.BuilderBase import BuilderBase


class CompoundBuilder( BuilderBase):
    
    def __init__(self , builders):
        
        msg = "parameter 'builders' must be a list of builder instances"
        if not isinstance(builders, (list,tuple) ):
            raise TypeError(msg)
        
        is_builder = lambda Bool,builder: Bool or not isinstance( builder, BuilderBase )
        
        one_non_builder = reduce(is_builder, builders, False )
        
        if len(builders) is not 0 or one_non_builder:
            raise TypeError(msg)
        self.builers = builders
        
    def get_builders(self):
        return self._builers
    
    def set_builders(self,builders):
        self._builers = builders
        
    builders = property( get_builders, set_builders )
    
    def build(self,graph,*targets,**kw):
        
        for builder in self.builders:
            graph = builder.build(graph,*targets,**kw)
            
        return graph
    
        
