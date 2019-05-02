"""
distutils classes to override default install, build commands
genarates and installs man file
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


from distutils.command.build import build
from distutils.command.install import install
from distutils.core import Command, setup
from distutils.errors import DistutilsOptionError
from os.path import join, exists
from slimproj_core.manfile_gen import genorate_man

class install_man( Command ):
    """
    installs manfile
    """
    
    # Brief (40-50 characters) description of the command
    description = "install an automatially genarated slimproj manfile"

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [( 'dir=', 'd', 
                     "path to install man too" ),
                     ( 'slimpy-tools=', None, 
                     "additional tools to include in man" ), ]
    # user_options = []


    def initialize_options ( self ):      
        self.dir = None
        self.slimpy_tools = ""
    # initialize_options()


    def finalize_options ( self ):
        if self.dir is None:
            raise DistutilsOptionError, "must supply '--dir' option"
#        self.ensure_dirname( "dir=" )

    def run ( self ):
        from os.path import pathsep,split,splitext
        from sys import path as sys_path
        if self.slimpy_tools:
            for py_module in self.slimpy_tools.split(pathsep):
                path,name = split( py_module )
                base,ext = splitext(name)
                sys_path.insert(0,path)
                exec "import %(base)s" %vars()
                del sys_path[0]
            
        
        print "   Generateing man contents from slimproj ..."
        content = genorate_man()
        slimproj_manfile = join( self.dir, 'slimproj.1' )
        print "   Writing contents to '%s'" %slimproj_manfile
        open_manfile = open( slimproj_manfile , 'w' ) 
        open_manfile.write( content )
    # run()


class build_with_man( build ):
    '''
    builds man file to 'build_base'/man/
    '''
    
    def initialize_options ( self ):
        'initialize options'
        build.initialize_options( self )
        
    
    def finalize_options ( self ):
        build.finalize_options( self )
        
        self.build_man = join( self.build_base, 'man' )
        
    def run( self ):
        
        build.run( self )
        self._run_build_man()
    
    
    def _run_build_man( self ):
        import os

        slimproj_manfile = join( self.build_man, 'slimproj.1' )
        
        if not exists( slimproj_manfile ):
            if not exists( self.build_man ):
                os.makedirs( self.build_man )
        
            print "   Generateing man contents from slimproj ..."
            content = genorate_man() 
            print "   Writing contents to '%s'" %slimproj_manfile
            open_manfile = open( slimproj_manfile , 'w' ) 
            open_manfile.write( content )
            return

class install_with_man( install ):
    user_options = install.user_options + [( 'install-man=', None, "path to install man too" )]
#    user_options =  [('install-man=', None, "path to install man too")]
    def initialize_options ( self ):
        install.initialize_options( self )
        self.install_man = None
    
    def finalize_options ( self ):
        install.finalize_options( self )
        
        if self.install_man is None:
            install_man = join( self.prefix, 'share', 'man', 'man1' )
            self.install_man = install_man 


    def run( self ):

        install.run( self )
        build_man = join( self.build_base, 'man' )
                
        self.copy_tree( build_man, self.install_man )
#        self._run_install_man( )
         

if __name__ == '__main__':
    setup( cmdclass={ 'install_man': install_man } )
    

