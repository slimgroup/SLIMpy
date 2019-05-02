"""
A SLIMpy linear operator consists of a dictionary of values operator_dict and
an undefined pipeobject to be defined upon application to a vector.
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

#from slimpy_base.utils.GlobalVars import GlobalVars

from slimpy_base.Core.User.linop.LinearOperatorType import LinearOperatorType, is_oper
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.utils.DotTest import DotTester
from copy import copy
from itertools import chain
from numpy import all
import warnings

## @ingroup linop
class LinearOperator( object ):
    """
    The base linear operator object should not be called by itself.
    """
    ## implements LinearOperatorType
    __metaclass__ = LinearOperatorType
    
    name = "Identity"
    env = InstanceManager()
    
    __tester__ = DotTester()
    __block_diagonal__ = True
    
    def __new__( cls, *params, **kparams ):
        if params:
            inspace = params[0]
            from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
            
            if isinstance(inspace, MetaSpace):                
                if hasattr(cls, "__meta_space__"):
                    
                    meta_space_bldr = getattr(cls, "__meta_space__")
                    return meta_space_bldr( *params, **kparams )
                
                elif hasattr(cls, "__block_diagonal__") and getattr(cls, "__block_diagonal__"):                    
                    from slimpy_base.User.AumentedMatrix.HelperFunctions import From_sapce    
                    return From_sapce( cls,  *params, **kparams)
                else:
                    raise TypeError( "LinearOperator %(cls)s got MetaSpace instance as first argument\n"
                                     "need '__meta_space__' creator or '__block_diagonal__' flag" %vars( ) )

        return object.__new__( cls, *params, **kparams )
    
    ##Initialize the vector
    def __init__( self, inspace, outspace, *params, **kparams ):
        """
        The init method is used to initialize the operator_dict with default values.
        """
        if not kparams.has_key( "adj" ):
            kparams['adj'] = False
#            raise Warning("no ajd flag found in kparams")
        
        self.params = params
        self.kparams = kparams
        
        self.inSpace = inspace
        self.outSpace = outspace
#        self.isadj = False
        
        self.__tester__.addLinearOp( self )
        
    def __str__( self ):
        """
        Returns the operators name and attributes
        """
        eqs = lambda ( kev, val ): "%s=%s" %( kev, val )
        name = self.name                                     # IGNORE:W0612
        lst = ", ".join( map( eqs, self.kparams.items() ) )  # IGNORE:W0612
        s = "<Linear Operator: %(name)s; %(lst)s>" % vars()
        return s
    
    def __repr__( self ):
        """
        Returns the operators name from operator_dict
        """
        
        eqs = lambda ( kev, val ): "%s=%s" %( kev, repr(val) )
        name = self.name                                     # IGNORE:W0612
        lst1 = [ eqs(item) for item in self.kparams.items() ]  # IGNORE:W0612
        lst2 = [ repr(item) for item in self.params ]  # IGNORE:W0612
        
        args = ", ".join( chain(lst1,lst2) )
        name = self.__class__.__name__
        return "%(name)s( domain, %(args)s )" %vars()
        
        return self.__str__() 
        
    def __eq__( self, other ):
        
        if type(self) != type(other):
            return False
        
        slots = ["inSpace","outSpace","params",
                     "kparams","tname","tparams","tkparams","isadj"]
        
        for name in slots:
            h1 = hasattr( self, name )
            h2 = hasattr( other, name )
            
            if h1 ^ h2:
                return False
                
            if h1 and h2:
                a1=getattr( self, name )
                a2=getattr( other, name )
                if not all(a1 == a2):
                    return False
        return True
    
    def __neg__(self):
        return CompoundOperator ( [-Identity(self.range()) , self ] )
    
    def domain( self ):
        """
        return inSpace
        """
        return self.inSpace
    
    def range( self ):
        """
        return outSpace
        """
        return self.outSpace
    
    def copy( self ):
        """
        Perform shallow copy of self
        """
        
        return copy( self )
    
    def _copy(self):
        
        cls = type(self)
        params = self.params
        kw = self.kparams
        domain = self.inSpace
        
        return cls( domain, *params, **kw )
    
    def adj( self , *other ):
        """
        The adjoint flips the operator_dict key transp. and updates the domain and range.
        """
        
        t = self.copy()
        
        inSpace = copy( t.inSpace )
        t.inSpace = copy( t.outSpace )
        t.outSpace = inSpace
        
#        #        t.isadj = not self.isadj
        
        t.kparams = copy( t.kparams )
        t.params = copy( t.params )
        
        t.kparams['adj'] = not t.kparams['adj']
        
        if other:
            assert len(other) == 1
            return t * other
        else:
            return t
    
    def _H_( self ):
        'proxy for sub classes to use Op.H'
        return self.adj()
    
    H = property( _H_ )
    
    def _getadj( self ):
        "get the adj key in the kparams"
        return self.kparams['adj']

    def _setadj( self, val ):
        "set the adj key in the kparams"
        self.kparams['adj'] = val
    
    isadj = property( _getadj , _setadj )
    
    def __mul__( self, other ):
        """
        Not defined in this class
        """
        if other is 0:
            return 0
        elif other is 1:
            return self
        elif is_oper(other):
            return CompoundOperator( [self,other] )
        else:
            return self.applyop( other )
    
    def __add__( self, other ):
        return ArithmaticOperator( '+', self, other )

    def __radd__( self, other ):
        return ArithmaticOperator( '+', other, self )

    def __sub__( self, other ):
        
        return ArithmaticOperator( '-', self, other )

    def __rsub__( self, other ):
        
        return ArithmaticOperator( '-', other, self )
    
    def __call__( self, other ):
        """
        Not defined in this class
        """
        if other is 0:
            return 0
        elif other is 1:
            return self
        elif is_oper(other):
            return CompoundOperator( [self,other] )
        else:
            return self.applyop( other )
            
    def applyop( self, other ):
        
        return other
    
    def getdim( self ):
        """
        Returns the dimensions of the operator. Usually not defined.
        """
        return [len( self.inSpace ), len( self.outSpace )]
        
    def norm( self ):
        """
        returns Identity
        """
        warnings.warn("please use SLIMpy.Norm Function", DeprecationWarning, 2)
        return Identity( self.outSpace )
    
    def __norm_col__(self):
        """
        Norm( oper , col=True ) -> oper.__norm_col__( )
        """
        return NotImplemented

    def __norm_row__(self):
        """
        Norm( oper , col=False ) -> oper.__norm_row__( )
        """
        return NotImplemented
    
    def normalize( self ):
        """
        returns comp( [self.norm(), self] )
        """
        warnings.warn("please use SLIMpy.Normalize Function", DeprecationWarning, 2)
        return CompoundOperator( [self.norm(), self] )
        
    def minvelconst( self, *args, **kargs ):
        """
        returns Identity
        """
        warnings.warn("please use SLIMpy.MinVelConst Function", DeprecationWarning, 2)
        return Identity( self.outSpace )
        

## @ingroup linop
class Identity( LinearOperator ):
    """
    I = Identity( space )
    Operator that does nothing
    """
    
    __block_diagonal__ = True
    
    def __init__( self, space ):
        LinearOperator.__init__( self, space, space, adj=False )
        self.kparams = {"adj":False}
        self.params = []
        self._pos_sign = True 
        return 
    
    def __neg__(self):
        I = self.copy( )
        I._pos_sign = not self._pos_sign
        
        return I
    
    def applyop(self,other):
        if self._pos_sign:
            return other
        else:
            return -other

## @ingroup linop
class CompoundOperator( LinearOperator ):
    """
    C = CompoundOperator( [o1, o2, ... ] ) 
    compound operator class used to chain together 
    Linear operators 
    """
    def __init__( self, alist ):
        
        self.alist = alist

#        self.ch
        inspace = self.domain()
        outspace = self.range()
        LinearOperator.__init__( self, inspace, outspace, adj=False )
        
    def __checklist( self ):
        """
        check if all of the domains and ranges can 
        be chained together
        """
        lambda y, x: bool( y.domain() == x.range() ) #IGNORE:W0104
        
        lst = self.alist
        check = zip( lst, [lst[-1]] + lst[:-1] )
        
        return
        
    def __getitem__( self, item ):
        return self.alist[item]
    
#    def append(self,item):
#        self.alist.append(item)
        
    def reverse( self ):
        """
        return a new object in reverse order
        """
        alist = copy( self.alist )
        alist.reverse()
        return alist
    
    def applyop( self, other ):
        """
        Overloads Applyop to apply each element 
        in this operator from the right most first
        """
        
        for i in range( len( self.alist )-1, -1, -1 ):
            other = self[i] * other
        return other
        
    def domain( self ):
        return self[-1].domain()
    
    def range( self ):
        return self[0].range()
        
    def adj( self ):
        alist  = self.reverse()
        newlist = CompoundOperator( [A.adj() for A in alist] )
        return newlist
    
    
    def __str__( self ):
        return "Comp:%s"%self.alist.__str__()
    
    def __repr__( self ):
        rplst = ", ".join( [ repr(item) for item in self.alist ] )
        return "CompoundOperator( [%(rplst)s] )" %vars()

    def copy(self):
        alist = self.alist
        return CompoundOperator( [A.copy() for A in alist] )
        pass

## @ingroup linop
class ArithmaticOperator( LinearOperator ):
    """
    Operator to handle arithmatic 
    operations on implicit operators
    ArithmaticOperator( '-', I, A )*x -> (I-A)*x -> (Ix - Ax)
     
    """
    def __init__(self, arithop, oper1, oper2):
        self.oper1 = oper1
        self.oper2 = oper2
        self.arithop = arithop
        
        from slimpy_base.Core.User.Structures.VectorSpace import VectorAddition
        domain = VectorAddition( [self.oper1.domain() ,self.oper2.domain()] )
        range = VectorAddition(  [self.oper1.range() ,self.oper2.range()] )
        LinearOperator.__init__( self, domain, range )

    def __str__(self):
        return "( %(oper1)s %(arithop)s %(oper2)s )" %self.__dict__
    
    def __repr__(self):
        oper1 = repr(self.oper1)
        oper2 = repr(self.oper2)
        arithop= repr(self.arithop)
        return "ArithmaticOperator( %(arithop)s, %(oper1)s, %(oper2)s )" %vars()
    
    def applyop(self,other):
        res1 = self.oper1 * other
        res2 = self.oper2 * other
        
        if self.arithop == '+':
            res = res1 + res2
            
        elif self.arithop == '-':
            res = res1 - res2
            
        return res
