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

from slimpy_base.utils.Interface import InterfaceType
from inspect import isdatadescriptor
from inspect import isroutine


class LinearOperatorType( InterfaceType ):
    interface_methods = {
        'H': isdatadescriptor,
        'adj' : isroutine,
        '__mul__' : isroutine,
        "applyop": isroutine,
        "domain":  isroutine,
        "range" : isroutine,
                             }

    LinearOperators = {}
    LinearOpFunctions = {}
    
    def __new__( cls, *args ):
        if args:
            name = args[0]
            if isroutine(name):
                cls.LinearOpFunctions[name.__name__] = name
                return name
        
        oper = InterfaceType.__new__(cls, *args)
        
        
        if args:
            cls.LinearOperators[name] = oper
            
        return oper
    
    @classmethod
    def print_opers( cls ):
        """
        register.print_opers( ) --> None
        
        print all of the linear operators. 
        any subclass of the LinearOperator class
        is registered.
        """
        
        print "#"*30
        print "Linear Operators"
        print "#"*30
        
        for name,doc in cls.list_opers():
            print "%(name)s:" %vars()
            print "-"*len(name)
            print doc
            print
            
        print "#"*30
        print "Linear Operator Functions"
        print "#"*30

        for name,doc in cls.list_opers(False):
            print "%(name)s:" %vars()
            print "-"*len(name)
            print doc
            print
    
    @classmethod
    def list_opers( cls, lt=True ):
        """
        list all classes that are subclasses of the LinearOperator
        base class.
        """
        if lt:
            lo = cls.LinearOperators
        else:
            lo = cls.LinearOpFunctions
            
        keys = lo.keys()
        keys.sort()
        for name in keys:
            item = lo[name]
            if item.__doc__:
                fill = '\n'+ " "*7
                doc = item.__doc__.strip( '\n\t ' )
                doc = [d.strip( '\t ' ) for d in doc.splitlines()]
                if len(doc) > 6:
                    doc = doc[:3] + [" ..."] + doc[-3:]

            else:
                doc = ["No documentation"]
            doc = " "*7 + fill.join( doc )
            yield name,doc
        return
    
is_oper = lambda item: type( type( item ) ) == LinearOperatorType
