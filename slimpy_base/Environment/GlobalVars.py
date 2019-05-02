"""
Singleton class  that contains all of the global variables  
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

from slimpy_base.setup.DEFAULTS import DEFAULTS
from pdb import set_trace

from os.path import abspath
from slimpy_base.Environment.Singleton import Singleton
from os import environ


class GlobalVars( Singleton ):
    """
    Singleton class used by slimpy to store global 
    variables
    """
#    __shared_state = {}
    
    def _get_slim_global(self):
#        print "getting _slim_globals"
        return self._slim_globals
    
    def _set_slim_global(self,val):
#        print "setting _slim_globals"
        self._slim_globals = val
    
    slimGlobals = property( _get_slim_global, _set_slim_global )
    
    
    def __new_instance__( self, name ):
        Singleton.__new_instance__(self, name)
        self.slimGlobals = { }
        
    
        
        self.PATHS = ["datapath", 'localtmpdir', 'globaltmpdir']
        self.INTS  = ["memsize", "verbose", 'ispipe', "eps"]
        self.BOOLS = ['ispipe']
        self.EVALS = ['nwin']
        
        self.slimdoc = {
            # PATHS
            "datapath":     "path where perminant data files will be built", 
#            "tmpdir":       "temporary header files will be built", 
#            'tmpdatapath':  "perminant data files will be built", 
            'localtmpdir':  'mpi - temp header files will be built (local to each node) ', 
            'globaltmpdir': 'mpi - temp header files will be built (global for every node) ', 
            
            "memsize":      'set the memory available to each program', 
            "verbose":      'set the verbosity from 1 to 10', 
            "eps" :         'Domain decomposition overlap', 
            'nwin' :        'dimentions to split the data into - mpi', 
            
            'MPIRUN':       'executable for mpi, used with MPIFLAGS' ,   
            'NODEFILE':     'file containing list of node names for mpi',
            "MPIFLAGS":     "defaults to '${MPIRUN} -np=${np} ${NODEFILE}'",
            'NODELIST':     'python list containing node names for mpi', 
            'abridge':      'abridge output with abridge-map', 
            'check_path':   'bool - check if all executable paths exist', 
            'debug':        'print extra info to logfile eg. print >> log(10,"foo") will print if debug=foo', 
            'logfile':      'file to print to', 
            'mpi':          'bool - force running mpi  or not', 
            'np':           'number of processors running in mpi', 
            'runtype':      '"normal" or "dryrun" ', 
            'strict_check' :'0,1 or 2. On 0 no domain/range checking. 1 checking. 2 no void Spaces will be accepted', 
            'test_devel':   'run developer tests, usualy known bugs', 
            
            'abridgeMap': "dictionary of strings to call 'output.replace(key,val)' before printing",
            'no_del': "bool, if true SLIMpy will not delete data until the end",
            'walltime':'amount of time a command is allowed to take',
            'rsh':'distributed mode: command used to talk with nodes [default "ssh"]',
            
            'sync_disk_om_rm':'calls $SYNC_CMD before removing data on disk'
            
               }
        
        self.update( **DEFAULTS )

    def get(self, key, *val):
        '''
        get method, see dict.get
        '''
        
        return self._slim_globals.get( key, *val)
        
    
    def update(self, **kw):
        'see: dict.update'
        self.setglobal( **kw )
        
    def setglobal( self, **kargs ):
        """
        Sets the global parameters accessed by the rest of the module
        if the entry is None then the variable will be none
        """
        self.setpath( kargs, *self.PATHS )
        self.applyFunc( kargs, int, *self.INTS )
        self.applyFunc( kargs, bool, *self.BOOLS )
        self.applyFunc( kargs, eval, *self.EVALS )
        
        self._slim_globals.update( kargs )
#        set_trace()
#        print "setglobal"
#        print kargs
#        print
        return
    
    def __contains__( self, key ):
        return self._slim_globals.has_key( key )
    
    def __getitem__( self, item ):
        return self._slim_globals[item]

    def __setitem__( self, key, val ):
        
        if isinstance( val, tuple ):
            assert len( val ) == 2, "value must be a 2-tupel of (value,doc) "
            value = val[0]
            doc = val[1] 
        
        else:
            value = val
            doc = None 
            
        self.set(key, value, doc)
        
    
    def set( self, key, value, doc=None ):
        'set item with optional documentation param'
#        print "setting ", key,'to', value
        if doc:
            self.slimdoc[key] = doc
        
        if isinstance(value, str) and key in self.PATHS:
            value = abspath( value )
            
        self._slim_globals[key] = value
    
    def applyFunc( self, dict, func, *keylist ):
        """
        apply a function on a values of dict
        specified by keylist
        """
        for key in keylist:
            if dict.has_key( key ):
                value = dict[key]
                if isinstance(value,  str ):
                    dict[key] = func( dict[key] )

    def keys(self):
        "see: dict.keys"
        return self._slim_globals.keys()
    
    def setpath( self, dict, *arglist ):
        """
        change values in dict specified by arglist
        to its absolute path
        """
        for arg in arglist:
            if dict.has_key( arg ):
                try:
                    dict[arg] = abspath( dict[arg] )
                except:
                    print arg, dict[arg]
                    raise
            
    def updateAbridgeMap( self, *d, **k ):
        """
        same as dict.update for self['abridgeMap']
        """
        self['abridgeMap'].update( *d, **k )
        
            # SETWORKINGDIR sets the place where headers and data are stored
    def setworkingdir( self, path ):
        """
        sets the working directory for all out of core operations
        """
        self.setglobal( tmpdir=path )
        environ['DATAPATH'] = path
        
    def printGlobals( self , paths=True ):
        """
        pretty printing of the globals
        """
        if paths:
            print " -- Paths --"
            print '='*35
            keys = self.PATHS
            keys.sort()
            for key in keys:
                print "%13s --| %s" % ( key, self[key] )
                doc = self.slimdoc.get( key, "" )
                if doc:
                    print ' '*18, "%s" % doc

        print '-- Vars --'
        print '='*35
        keys = self._slim_globals.keys()
        keys.sort()
        if 'abridgeMap' in keys:
            keys.remove( 'abridgeMap' )
        keys = [key for key in keys if key not in self.PATHS]
        for key in keys:
            print "%13s --| %13s -|- %s" % ( key, self[key], self.slimdoc.get( key, "" ) )
            
    def get_node_map(self):
        ntype = self['nodemap_type']
        
        NODELIST = None
        if self['NODEFILE']:
            NODELIST= [ node.strip() for node in open( self['NODEFILE'] ).read().split() ]
        elif self['NODELIST']:
            NODELIST = self['NODELIST']
            
        nmap = []
        if NODELIST:
            sorted_list = list(NODELIST)
            if ntype == 'lin':
                sorted_list=sorted_list
            elif ntype == 'sort':
                sorted_list.sort()

            else:
                raise Exception( 'unknowm value for nodemap_type' )
                
            for rank,node in enumerate(sorted_list):
                
                nmap.append((node,rank))
        else:
            for rank in range(self['np']):
                node = 'localhost'
                nmap.append((node,rank))
                    
        return nmap
        

