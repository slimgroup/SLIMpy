"""
see log class
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


from sys import stderr,stdout
from os.path import devnull
from slimpy_base.Environment.InstanceManager import InstanceManager

NULLOUT = open( devnull, 'w' )

class _Log( object ):
    """
    log object is used by all of slimpy to coordinate output
    suggested use:
    alog = log()
        print >>alog, "logging somthing"
    to print unconditionally or: 
        print >>alog(3), "logging somthing"
    to print only of verbosity is above 3
     
    """
    
    name = "log"
    env = InstanceManager()
    __shared_state = {}

    
    def __init__( self ):
        """
        singleton instance
        """
        self.__dict__ = self.__shared_state
    
    
    def init( self, lfile=stderr, nullout=NULLOUT, verbose = 1 ):
        """
        init is for internal use only. use setter funtions to promote
        consistancy.
        """
        self.verbose = verbose 
        self.setLogFile( lfile )
        self.setNullOut( nullout )

    def setVerbose( self, verb ):
        """
        set verbosity level
        """
        self.verbose = verb
    
    def setLogFile( self, lfile ):
        """
        @param:lfile must have a write method
        """
        if isinstance( lfile, str ):
            if lfile == "stdout":
                lfile = stdout
            elif lfile == "stderr":
                lfile = stderr
            elif lfile == 'null':
                lfile = NULLOUT
            else:
                lfile = open( lfile, 'w' )
        assert hasattr( lfile, 'write' ), "lfile object: %(lfile)s must have a write method " %vars() 
        
        self.logFile = lfile

    def setNullOut( self, no ):
        """
        set where the null out points to 
        this is so the log can discriminate what output it will print 
        """
        if isinstance( no, str ):
            no = open( no, 'w' )
        assert hasattr( no, 'write' ), "no object: %(no) must have a write method " %( vars() )
        
        self.nullOut = no
        
    def write( self, string ):
        """
        write to file
        """
        slimvars = self.env['slimvars']

        string = str( string )
        if slimvars['abridge']:
            string = self.abridge( string )
        self.logFile.write( string )
        self.logFile.flush()
    
    def get_slimvars(self):
        slimvars = self.env['slimvars']

        logfile = slimvars['logfile']
        
        if not isinstance(logfile, dict):
            self.setLogFile( logfile )
            slimvars['logfile'] = { }
        
        logfile = slimvars['logfile']
        
        logfile.setdefault('log', self)
        logfile.setdefault('null', NULLOUT )
        
        return logfile,slimvars['debug'] 
    
    def set_default_log(self ,verb,logname):
        
        logfile,debug = self.get_slimvars()
        
        has_key = logfile.has_key(logname)  
        if not has_key:
            if isinstance(debug, (list,tuple) ):
                debug_log = logname in debug
            else:
                debug_log = logname == debug
            
            if verb or debug_log:
                logname = 'log'
            else:
                logname = 'null'
        
        logfile[logname] = self.log_open( logfile[logname] )
        return logfile[logname]
        
        
    def log_open(self,logname):
        if isinstance(logname, file):
            return logname
        elif isinstance(logname, _log):
            return logname
        elif logname == "stdout":
            return stdout
        elif logname == "stderr":
            return stderr
        elif logname == 'null':
            return NULLOUT
        else:
            return open( logname, 'w' )
        
        
    
    def __call__( self, lval, debug=None ):
        """
        used like print >> log(3,'solver')
        which will print if the current verbosity is greater than or eual to 
        3 or the debug variable is set to 'solver'
        """
        slimvars = self.env['slimvars']

        verb = slimvars['verbose'] >= lval
#            logname = 'log'
#        else:
#            logname = 'null'
#        
#        log = None

        if debug:
            log = self.set_default_log( verb, debug )
        elif verb:
            log = self.set_default_log(verb, 'log')
        else:
            log = self.set_default_log(verb, 'null')
            

#        if not log:
#            log = self.set_default_log(logname)
#        
        return log
#        if self.slimvars['verbose'] >= lval or debug == self.slimvars['debug']:
#            return self
#        else:
#            return self.nullOut
        
    def abridge( self, string ):
        """
        uses the global dict variable 'abridgeMap' in SLIMGlobals
        to replace all of the ocurrences of each key with the value
        this is helpful in reducing the amount of garbage input
        for examle in the simple1 tutorial I replace each $RSFROOT path with ''
        
        """
        slimvars = self.env['slimvars']
        
        for item in slimvars['abridgeMap'].items():
            string = string.replace( *item )

        return string


_log = _Log
