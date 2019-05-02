"""
Base rsf converter class
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


from slimpy_base.Core.Command.Converter import Converter
from slimpy_base.Core.Command.Drivers.ooc_driver import OutOfCoreDriver
from slimpy_base.api.Plugins.slim2rsf.AddComand import rsfAddCommands
#from slimpy_base.utils.GlobalVars import GlobalVars
from os.path import join, isfile, isabs, normpath, abspath
from stat import S_IMODE,ST_MODE
from os import pathsep ,stat, environ
from string import Template
from slimpy_base.Environment.InstanceManager import InstanceManager



class sfConverter( Converter ):
    """
    Base rsf converter class used when specific 
    command can not be found
    @postcondition: tansform returns voidspace
    """
    env = InstanceManager()
#    slimvars = GlobalVars()

    @classmethod
    def place_adder( cls, command ):
        command.adder = rsfAddCommands()
        return command
    
    @classmethod
    def map( cls, source, command ):
        
        cmnd = cls.default_function( command )
        
        return cls.pack(  cmnd ) 
    
    @classmethod
    def guess_exe_path(cls, name, error=0):
        
        if name.startswith('sf'):
            sfname = name
        else:
            sfname = "sf"+name
        slimvars = cls.env['slimvars']
        sfname = join( slimvars['RSFBIN'] , sfname )
            
        if is_executable(name):
            return abspath( name )
        
        elif is_executable(sfname):
            return sfname
        
        elif WhereIs(name):
            return WhereIs(name)
        
        elif error:
            raise EnvironmentError( "No files '%(name1)s' or '%(name2)s'" %vars() )
        else:
            return name
        
            
            
        
    
    @classmethod
    def default_function( cls, command, name=None ):
        slimvars = cls.env['slimvars']
        if name is None:
            name = command.tag
        else:
            name = str( name )
        
        exe = cls.guess_exe_path(name, error=slimvars['check_path'] )            

        command.func = OutOfCoreDriver( exe )
        command.adder = rsfAddCommands()
        
        return command
    
    @classmethod
    def mpi_function( cls, command, name=None, num_proc='all' ):
        slimvars = cls.env['slimvars']
        MPICOM = Template( slimvars['MPIFLAGS'] ) 
        
        if name is None:
            name1 = command.tag
        else:
            name1 = name
            
        name2 = join( slimvars['RSFBIN'] , 'xsf'+name1 )
        
        if isfile( name1 ):
            if isabs( name1 ):
                command_name = name1
            else:
                command_name = join( ".", name1 )
        else:
            command_name = name2
            
        if slimvars['check_path'] and not isfile( command_name ):
            raise EnvironmentError( "No files '%(name1)s' or '%(name2)s'" %vars() )
        
#        assert slimvars['mpi'], "called mpi map while slimpy mpi var is false"
        
        
        if "$NODEFILE" in slimvars['MPIFLAGS'] and slimvars['NODEFILE'] is None:
            raise Exception("SLIMpy detected an mpi process to be run needs a nodefile: "
                            "please set 'NODEFILE' global variable")
        mpi_cmd = MPICOM.substitute( **slimvars.slimGlobals )
        
        cmd = "%(mpi_cmd)s %(command_name)s" % vars()
        command.func = OutOfCoreDriver( cmd )
        command.adder = rsfAddCommands()
        
        command.command_type = 'multi_process'
        command.num_proc = num_proc
        
        return command    
    @classmethod    
    def constr( cls, command, *Spaces ):
        return True


def WhereIs( file ):

    path = environ['PATH']
    for d in path.split( pathsep ):
        f = join(d, file)
        if is_executable(f):
            return normpath( f )
        else:
            continue
        
    return None

def is_executable( f ):
    if isfile(f):
        try:
            st = stat(f)
        except OSError:
            return False
        
        if S_IMODE( st[ ST_MODE] ) & 0111:
            return True
        
    return False
    

