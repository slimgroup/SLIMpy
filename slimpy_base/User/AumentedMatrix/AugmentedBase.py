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

from numpy import ndarray, array,zeros_like
from itertools import izip,starmap,cycle
from pdb import set_trace


class AugmentBase( ndarray ):
    'base class for augmented vector and operator'
    _contained_type = None
    
    def __new__(cls, *args, **kw ):
        kw['dtype'] = object
        return  array( *args, **kw).view(cls)

    def __array_finalize__(self,obj):
#        print "finalize",type(obj)
        if hasattr(obj,"_contained_type"):
            self._contained_type = type(self)._contained_type

        if hasattr(obj,"meta") and obj.meta is not None:
            self.meta = obj.meta.copy()
#        ndarray.__array_finalize__(self,obj)
        
    def __array__(self):
        return self.view( ndarray )
    
    def __array_wrap__(self, obj):
        new_obj =  self.view( self.__class__ )
        new_obj._contained_type = self._contained_type
        return new_obj
    
    def for_each( self ):
        return self.ravel().__iter__( )
        
    def __init__(self,*args,**kw):
#        print "init"
        return ndarray.__init__( self, *args,**kw )
    
    def __attr_func__( self, attr, pkw_obj ):
#        print "func"
        new_array = zeros_like(self).view( self.__class__ )
        
        for i in range(self.size):
            item = self.flat[i]
            if isinstance(item, self._contained_type):
                method = getattr(item, attr) 
                p,kw = pkw_obj.next()
                new_array.flat[i] = method( *p, **kw )
            else:
                new_array.flat[i] = item
                
        new_array = new_array.view( self.__class__ )
        
        if hasattr(self, 'meta' ):
            try:
                new_array.meta = self.meta
            except AttributeError:
                pass
        
        return new_array
    
    def __pk_helper__( self, _iter, itm):
        """
        aug.__pk_helper__( _iter, itm ) -> None
        pk_helper performs an inplace change of itm
        _iter is an iterator that loops through (key,value)
        pairs of itm.
        if array(val) returns an array of size 0 then itm[key]
        is replaced with a 1D array of 'value' of len self.size
        if   array(val) returns an array of size equal to self.size
        then itm[key] is replaced with a 1D array(val). 
        """
        
        for key,val in _iter:
            array_val = array(val)
            if not array_val.shape:
                array_val = array( [val]*self.size )
            array_val = array_val.ravel( )
            if not self.size == array_val.size: 
                msg = "'augmatrix size' %s != 'parameter size' %s,\n\tFor parameter '%s'='%s'" %(self.size, array_val.size,key,val)
                raise ValueError(msg)
             
            itm[key] = array_val
                 
    def __pk_expannder__( self, *p, **kw):
        '''
        aug.__pk_expannder__( *p, **kw ) -> iterator
        expands takes each item element of p and k and calls
        uses __pk_helper__ to create an array of size of self.size
          
        iterator returns tuples of ( p, kw )
        '''

        if p:
            p = list(p)
            self.__pk_helper__( enumerate(p), p )
            p_izip = izip(*p)
        else:
            p_izip = cycle([()])
        
        if kw:
            self.__pk_helper__( kw.iteritems(), kw )
            keys,values = zip( *kw.items() )
            vals = izip(*values)
            zipkw = starmap( lambda *item: dict(zip(keys,item)),vals)
        else:
            zipkw = cycle([{}])
    
        return izip( p_izip,zipkw)

    def __obj_or_array__(self,obj):
        if isinstance(obj, ndarray):
            return obj.view( ndarray ).reshape( self.shape )
        else:
            return obj
    
    def __func__(self,other,name):
        o_obj = self.__obj_or_array__(other)
        self_func = getattr( self.view( ndarray ), name )
        new = self_func( o_obj ).view(self.__class__ )
        if hasattr(self,"meta") and self.meta is not None:
            new.meta = self.meta.copy()

        return new
    
    
    def __add__( self, other ):
        return  self.__func__(other, '__add__')
            
    def __radd__( self, other ):
        return  self.__func__(other, '__radd__')
    
    def __sub__( self, other ):
        return  self.__func__(other, '__sub__')

    def __rsub__( self, other ):
        return  self.__func__(other, '__rsub__')
    
    def __div__( self, other ):
        return  self.__func__(other, '__div__')
        
    def __rdiv__( self, other ):
        return  self.__func__(other, '__rdiv__')
        
    def __mul__( self, other ):
        return  self.__func__(other, '__mul__')
    
    def __rmul__( self, other ):
        return  self.__func__(other, '__rmul__')
        
    def __pow__( self, other ):
        return  self.__func__(other, '__pow__')
    
    def __neg__( self ):
        new = self.view( ndarray ).__neg__( ).view(self.__class__ )
        if hasattr(self,"meta") and self.meta is not None:
            new.meta = self.meta.copy()
        return new
        
    def __abs__( self ):
        new = self.view( ndarray ).__abs__().view(self.__class__ )
        if hasattr(self,"meta") and self.meta is not None:
            new.meta = self.meta.copy()
        return new



