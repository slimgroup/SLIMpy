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

from inspect import isroutine
from string import Template


UnittestTemplate = Template("""
from unittest import TestCase,defaultTestLoader

class ${CLASS}Tester( TestCase ):
${METHODS}

def suite():
    return defaultTestLoader.loadTestsFromTestCase( ${CLASS}Tester )
""")

MethodTemplate = Template("""
    def test${NAME}( self ):
        raise NotImplementedError("test not implemented")
""")

def make_unittest( klass ):
        
    klass_methods = [key for key,item in klass.__dict__.items() if isroutine(item) ]
    
    CLASS = klass.__name__
    
    subst = lambda name: MethodTemplate.substitute(NAME=name)
    methods = [ subst(name) for name in klass_methods]
    
    res = UnittestTemplate.substitute( CLASS=CLASS,
                                 METHODS="\n".join(methods)
                                 )
    print res
