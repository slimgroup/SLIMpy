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

from slimpy_base.api.Plugins.slim2rsf.sfCommandFactory import rsfCommandFactory
from slimpy_base.api.Plugins.slim2rsf.sfcommands.sfConverter import sfConverter
from slimpy_base.Core.Interface.ContainerBase import DataContainer

iscontainer = lambda obj : isinstance(obj , DataContainer )

class cmpfixture( sfConverter ):
    cmd = None
    
    @classmethod
    def constr( cls, command, *params ):
        cls.eqShape(command, params)
       
    @classmethod 
    def trans( cls, cmd, space, *spaces ):
        cls.change(space, data_type = "int"  )
        
        return space 

    @classmethod
    def map( cls, src, cmd ):
        cmd = cls.default_function( cmd, "boolcmp" )
        
        right = cmd.kparams['right']
        
        if not iscontainer(right):
            cmd = cls.keywordmap(cmd, {"right":"right_f"})
        
        cmd.kparams.update( sign=cls.cmd )
        return cls.pack( cmd )

class all( object ):
    
    class eq( cmpfixture ):
        cmd = 'eq'
    class gt( cmpfixture ):
        cmd = 'gt'
    class ge( cmpfixture ):
        cmd = 'ge'
    class le( cmpfixture ):
        cmd = 'lq'
    class lt( cmpfixture ):
        cmd = 'lt'
    class ne( cmpfixture ):
        cmd = 'ne'
    class and_( cmpfixture ):
        cmd = 'and'
    class or_( cmpfixture ):
        cmd = 'or'

sffactory = rsfCommandFactory()
sffactory.addallfrom( all )


