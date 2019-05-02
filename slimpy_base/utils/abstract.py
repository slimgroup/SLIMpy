"""
This package is not currently used by slimpy
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


class checktype(object):
    
    def __init__(self,f,p,k,Return):
        print "checktype"
        self.f = f
        self.p = p 
        self.k = k
        self.Return = Return
        
    def __call__(self,*q,**r):
        print "call"
        self.check(q, r)
        Return  = self.f(*q,**r)
        if self.Return is not None and not isinstance(Return, self.Return):
            raise Exception
        return Return
        
    def check(self,q,r):
        for i in range(len(self.p)):
            print i
            print self.p[i] , type(q[i])
            if not isinstance(q[i],self.p[i] ):
                raise Exception
        for i in self.k.keys():
            if i in r:
                if not isinstance(r[i],self.k[i] ):
                    raise Exception         


def prototype(Return=None,*p,**k):
    print "check"
    def func(f):
        print "func"
        return checktype(f,p,k,Return=Return)
    return func



def abstractmethod(method):
    """Decorator for tagging a method as abstract. """
    def NotImplementedMethod(*p,**k):
        raise NotImplementedError, "Abstract method %s not implemented" % method
    return NotImplementedMethod




class abstractclass(object):
    def __abstractmethods(self):
        for methodname in dir(self):
            method = getattr(self, methodname, None)
            if not callable(method):
                continue
            if hasattr(method, "abstract"):
                raise NotImplementedError, ("Abstract method %s not implemented" %
                      method)
                
    def __getattribute__(self,attribute):
        method = object.__getattribute__(self,attribute)
        if hasattr(method, "abstract"):
                raise NotImplementedError, ("Abstract method %s not implemented" %
                      method)
        return method


class interface(object):
    
    def __new__(self):
        raise Exception, "Unimplemented interface"
    
        

class implements(abstractclass):
    def __abstractmethods(self):
        pass
        
    def __getattribute__(self,attribute):
        return object.__getattribute__(self,attribute)
                
                
