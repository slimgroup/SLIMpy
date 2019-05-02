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

def slim_test_builder( target, source, env ):
    
    import slimpy_base
    from slimpy_base.test_SLIMpy.LatexTestResult import LatexTextTestRunner
    from slimpy_base.test_SLIMpy import suite

    slimpy_base.parse_env(env)
    
    
    stream = open( str(target[0]), 'w' )
    
    test = suite()
    
    tr = LatexTextTestRunner( stream=stream)
    tr.run(test)
#    result = SLIMpy.test(2, 2, stream)
        
    return


def slim_test_emitter(target, source, env):
    import slimpy_base
    vers_val = env.Value( slimpy_base.__version__ )
    source = [ vers_val ]
    
    return target,source
