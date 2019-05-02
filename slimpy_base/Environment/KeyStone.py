# SLIMpy/KeyStone.py
"""
KEYSTONE CLASS
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


from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.api.Plugins.pluginLoader import loader as PluginLoader

from slimpy_base.Environment.Singleton import Singleton


class KeyStone( Singleton ):
    """
    Singleton Class to be used to connect all the moduals of SLIMpy together
    """

    def __new_instance__( self, name ):
        """
        Initialize Class note that this constructor returns a shared state instance
        """
        Singleton.__new_instance__(self, name)

        self.setplugins( )
    
    def setplugins( self, *par, **kw ):
        """
        sets the woking plugins to kargs
        """
        #by initializing the loader we initialize all plugins
        pl = PluginLoader()
        # get all of the working plugins
        plugins = pl.load() 

        
        plugins['adc'] = DataContainer
        #set the plugins as a global SLIMpy variable

        plugins.update( *par, **kw )
        
        
        self.PLUGINS = plugins 
                

    # get a plugin from dict
    def getplugin( self, plugin ):
        """
        get a single plugin from a string
        """
        try:
            return self.PLUGINS[plugin]
        except KeyError:
            plugins = self.PLUGINS.keys()  #IGNORE:W0612
            msg = ( "plugin '%(plugin)s' does not exist. Available "
                    "plugins are: - %(plugins)s" )
            
            raise KeyError( msg % vars() ) 
        

    def getplugins( self ):
        """ 
        returns all plugins
        """
        return self.PLUGINS


    def listPlugins( self ):
        """
        list all available plugins
        """
        print 'List Plugins:'
        for plugin in self.PLUGINS.keys():
            print '  -', plugin
    
    def __repr__( self ):
        return "<SLIMpy: " + self.__class__.__name__ + " object>"

