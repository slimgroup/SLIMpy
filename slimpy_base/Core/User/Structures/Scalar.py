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
from slimpy_base.Core.Interface.node import Source,Target
from slimpy_base.Core.Command.CommandPack import CommandPack
from slimpy_base.Core.Command.Command import Command as general_command

import traceback
from numpy import inf

class ScalarProxy( object ):
    
    def __init__( self, value ):
        self.method_name = value
        
    def __call__(self , src_self,other_obj,trg_scal=None ):
            
        method = getattr(self, self.method_name)
        
        val = method( get_num(src_self), get_num(other_obj) )
        if trg_scal is None:
            return val
        else:
            trg_scal.set(val)
            return
    
    def __str__(self):
        return "Scalar Function: %s" %self.method_name
    
    def add( self, one, other ):
        return one + other
    def radd( self, one, other ):
        return other + one
    def sub( self, one, other ):
        return one - other
    def rsub( self, one, other ):
        return other - one
    def div( self, one, other ):
        if one == 0:
            return 0
        elif other == 0:
            return inf
        else:
            return one / other 
    def rdiv( self, one, other ):
        if other == 0:
            return 0
        elif one == 0:
            return inf
        else:
            return other / one 

    def mul( self, one, other ):
        return one * other
    def rmul( self, one, other ):
        return other * one
    def pow( self, one, other ):
        return one ** other
    def neg( self, one ,other):
        return -one
    def abs( self, one, other ):
        return abs(one)
    def real(self, x ,other ):
        return hasattr( x,'real') and x.real or x
    def imag(self, x ,other ):
        return hasattr(x,'imag') and x.imag or x , "imag" 
    def conjugate(self, x ,other ):
        return hasattr(x,'conjugate') and x.conjugate() or x
    def and_( self, one, other ):
        return one & other
    def or_( self, one, other ):
        return one | other
    def lt(self, one, other):
        return one < other
    def le(self, one, other):
        return one <= other
    def gt(self, one, other):
        return one > other
    def ge(self, one, other):
        return one >= other
    def eq(self, one, other):
        return one == other 
    def ne(self, one, other):
        return one != other
    
## Object to wrap python numbers for integration into the SLIMpy AST  
# @ingroup userclasses
class Scalar( object ):
    """
    Scalar object represents a number
    a scalar object does not contain a number until
    built by the AST
    """
    _count = 0
    
    env = InstanceManager( )

    @classmethod
    def _inc_count(cls):
        cls._count += 1
    
    def __init__(self,val=None):
        self._inc_count()
        if val is None:
            self._is_set = False
            self._name = "${SCALAR[%s]}" %self._count
            self.__val = self._name 
        else:
            self._is_set = True
            self._name = "${SCALAR[%s]}" %self._count
            self.__val = val 
      
        
    def set(self,val):
        if self._is_set:
            print "Warning: Scalar Object is already set"
#            raise TypeError( "Scalar Object is already set" )
        self.env['table'].scalars_map[self._name] = val         
        self.__val = val
        self._is_set = True
        
        return
    
    def item(self):
        if not self._is_set:
            if self.env['slimvars']['runtype'] == 'dryrun':
                raise Exception( 'can not do evaluation of slimpy.scalar in "dryrun" mode' )
            self.env['graphmgr'].flush( self )    
        return self.__val
    
    def get_data(self, nodename ):
        return self.__val
    
    def _get_data(self):
        return self.__val
    
    def get_nodenames(self):
        return ['localhost']
    
    data = property( _get_data )
    
    nodenames = property(get_nodenames)
    
    def _get_node_names(self):
        return [ 'localhost' ]
    
    def node_copy(self,to_node):
        pass
    
    def __str__(self):
        if self._is_set:
            st = "Scalar(%s)" %self.__val
        else:
            st = self._name
        
        return st
    
    def __repr__(self):
        return self.__str__( )
    
    def _num_src(self,num):
        if is_scalar_obj(num):
            return Source( num )
        else:
            return Scalar( num )
    
    def gen_new_scal(self,other,func):
        
        scalar = Scalar( )
        trg_scal = Target( scalar )
        src_self = Source( self )
        
        other_obj = self._num_src( other )
        
#        new_func = scalar_helper(func,func_name=func_name)
        
        tag = str(func)
        command = general_command( tag , None, src_self,other_obj,trg_scal )
        command.func = func
        
        if self.env['slimvars']['keep_tb_info']:
            stack = traceback.extract_stack( )
            st_list  = traceback.format_list( stack[:-3] )
            command.tb_info = "".join(st_list)
            
        compack = CommandPack([command], None, None)
        
        self.env['graphmgr'].graphAppend( compack )
    
        return scalar
    
    def __scalar_operation__(self,other,func):
        
        if has_num(self) and has_num(other):
            return func( get_num(self), get_num(other) )
            
        if is_number(other) or other is None:
            return self.gen_new_scal(other, func )
        else:
            return NotImplemented
           
    def __add__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('add') )
            
    def __radd__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('radd')  )
        
    def __sub__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('sub')  )

    def __rsub__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('rsub')  )
    
    def __div__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('div')  )
        
    def __rdiv__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('rdiv')  )
        
    def __mul__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('mul')   )
    
    def __rmul__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('rmul')   )
        
    def __pow__( self, other ):
        return self.__scalar_operation__(other, ScalarProxy('pow')  )
    
    def __neg__( self ):
        return self.__scalar_operation__(None, ScalarProxy('neg')   )
        
    def __abs__( self ):
        return self.__scalar_operation__(None, ScalarProxy('abs') )
        
    def __real__(self):
        return self.__scalar_operation__(None, ScalarProxy('real') )
    
    def __imag__(self):
        return self.__scalar_operation__(None, ScalarProxy('imag')  )
    
    def conjugate(self):
        return self.__scalar_operation__(None, ScalarProxy('conjugate') )
    
    real = property( __real__ )
    imag = property( __imag__ )
    
    def __and__( self, other ):
        return self.__scalar_operation__( other, ScalarProxy('and_')  )

    def __or__( self, other ):
        return self.__scalar_operation__( other, ScalarProxy('or_')  )
    
    def __lt__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('lt')  )

    def __le__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('le')  )

    def __gt__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('gt')  )
    
    def __ge__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('ge')  )
    
    def __eq__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('eq')  )

    def __ne__(self, other):
        return self.__scalar_operation__( other, ScalarProxy('ne')  )

    def __nonzero__(self):
        
        return bool( self.item( ) )
        
#===============================================================================
# Helper functions 
#===============================================================================
number = (int, long, float, complex, Scalar)
is_number = lambda num: isinstance(num, number) 
is_scalar_obj = lambda scal: isinstance(scal, Scalar)
is_source = lambda scal: isinstance(scal, Source )
has_num = lambda scal: is_scalar_obj(scal) and scal._is_set or not is_scalar_obj(scal)

def get_num( scal ):
    if is_source(scal) or is_scalar_obj( scal ) :
        return scal.data
    else:
        return scal
        


