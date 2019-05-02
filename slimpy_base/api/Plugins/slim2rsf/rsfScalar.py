"""

scalar class complements vector class

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


from slimpy_base.Environment.InstanceManager import InstanceManager
from numpy import inf
from numpy import int32, float32, float64, complex64 #IGNORE:E1101 @UnresolvedImport
from os.path import join
from re import compile as re_compile
from string import Template
from subprocess import Popen, PIPE


__env__ = InstanceManager()

SFATTR = lambda :join( __env__['slimvars']['RSFBIN'], 'sfattr' )

ATTRMD  = lambda **kw: Template( "${attr} <  ${file} want=${want} lval=${lval} " ).substitute( **kw )
PROJCMD = lambda **kw: Template( "${project} < ${file} lambda=${lamb}" ).substitute( **kw )

SFPROJECT = lambda :join( __env__['slimvars']['RSFBIN'], 'sfproject' )


class Scalar( object ):
    '''
    Scalar object contains class methods to work on rsf data
    '''
    
    env = InstanceManager()
#    log = Log()
    re_float = re_compile( '[-+]?\d*\.\d*' )
    
    @classmethod
    def get_command( cls, cmd ):
        '@deprecated: '
        if hasattr( cls, cmd ):
            return cls(cmd)
        else:
            raise TypeError('No Scalar command "%s" in RSF ' %cmd)
    
    def __init__(self, cmd):
        if not  hasattr(self, cmd):
            raise TypeError('No Scalar command "%s" in RSF ' %cmd)
        self._command_name = cmd
        
    def __call__(self, container, scalar, *args, **kw):
        '''
        only non classmethod calls methoc given by self._command_name
        '''
        if not hasattr(self, "_command_name"):
            raise AttributeError("scalar class not initialized")
        
        cmd = self._command_name
        attr = getattr( self, cmd )
        container.node_copy( 'localhost' )
        attr( container, scalar, *args, **kw )
      
#    slimvars = GlobalVars()
    def __str__(self):
        return "rsf scalar method %s" %self._command_name
    
    def __repr__(self):
        return self.__str__( )
    
    @staticmethod
    def rms( container, scalar ):
        """    Returns the root mean square"""
        num = Scalar.attr( container, scalar, want='rms' )
        scalar.set( num ) 
    
    @staticmethod
    def max( container, scalar ):
        """    Returns the maximum value"""
        num = Scalar.attr( container, scalar,  want='max' )
        scalar.set( num ) 
    
    
    @staticmethod
    def min( container, scalar ):
        """    Returns the minimum value"""
        num = Scalar.attr( container,  scalar, want='min' ) 
        scalar.set( num ) 
    
    @staticmethod
    def mean( container, scalar ):
        """    Returns the mean value"""
        num = Scalar.attr( container, scalar,  want='mean' )
        scalar.set( num ) 
    
    @staticmethod
    def var( container, scalar):
        """    Returns the variance"""
        num = Scalar.attr(  container, scalar, want='var' )
        scalar.set( num )
    
    @staticmethod
    def sdt( container, scalar ):
        """    Returns the root"""
        num =  Scalar.attr( container, scalar, want='std' )
        scalar.set( num ) 
    
    @staticmethod
    def norm( container, scalar, lval=2 ):
        """    Returns the lval norm of the vector """
        is_inf = lval == inf or (isinstance(lval, str) and lval.lower() == 'inf') #IGNORE:E1103
        
        if is_inf :
            a1 = Scalar.attr( container, scalar,  want='max' )
            a2 =  Scalar.attr( container, scalar,  want='min' )
            
            num = max( abs(a1), abs(a2) )
        else:
            
            num = Scalar.attr( container, scalar, want='norm', lval=lval )
            
        scalar.set( num )
            
    
    @staticmethod
    def attr_make_number(atr):
        '''
        call eval on atr if result is tuple make complex
        @param atr: string 
        @type atr:str
        '''
        
        num = eval( atr )
        if isinstance(num, tuple):
            num = complex( *num )
        return num
    
    @staticmethod
    def attr( container, scalar,  want='norm', lval=2 ):
        
        """
        fetches various attributes of the vector.
        vector will be flushed prior to the operation.
        TODO: make it so that the vector does not flush automatically. 
        """        
        
#        command = "%(path)s < %(data)s want=%(want)s lval=%(lval)s" %vars()
        command = ATTRMD( attr=SFATTR(), 
                          file=container.get_data( 'localhost' ), 
                          want=want, 
                          lval=lval )
        #define parameters for the pipe
        print >> __env__['record']( 1 ,'cmd'), command
        p0 = Popen( command, shell=True ,stdout=PIPE,stderr=PIPE)
        err = p0.wait()
        if err:
            lines = p0.stderr.read()
            p0.stderr.close()
            p0.stdout.close()
            raise IOError(err,command +'\n'+ lines)
        output = p0.stdout.read()
        p0.stderr.close()
        p0.stdout.close()
        
        n = output.split( '=' )[-1].split( 'at' )[0]
        
        return Scalar.attr_make_number( n )
    
    @staticmethod
    def project( container, scalar, lamb=None):
        '''
        returns threshold value that will
        threshold the vector to a 1-norm of lamb
        '''
        if lamb is None:
            raise TypeError( 'Must specify "lamb=" value' )

        command = PROJCMD( project=SFPROJECT(), 
                              file=container.get_data( 'localhost' ), 
                              lamb=lamb,
                                   )
        
        p0 = Popen( command, shell=True ,stdout=PIPE,stderr=PIPE)
        err = p0.wait()
        if err:
            lines = p0.stderr.read()
            p0.stderr.close()
            p0.stdout.close()
            raise IOError(err,command +'\n'+ lines)
        n = p0.stdout.read()
        p0.stderr.close()
        p0.stdout.close()
        
        assert 'tau=' in n
        
        num = n.split('=')[-1].strip()
        scalar.set( float( num ) )

    @staticmethod
    def getitem( container, scalar, item):
        "get item-th element from the vector"
        if not isinstance( item, int ):
            raise TypeError, "getitem got %(item)s expected int"
        
#        params = container.getParameters( )
        print >> __env__['record']( 1 ,'cmd' ), "getitem( %s )" %(item)
        
        item = container.readbin( start=item, len=1 )[0]
        
        l = lambda x : ( ( x == int32     and int ) or
                        ( x == float32   and float ) or 
                        ( x == float64   and float ) or 
                        ( x == complex64 and complex ) )
        
        
        t = l( type( item ) )
        
        
        
        num = t( item )
        scalar.set( num )
        
        return 

