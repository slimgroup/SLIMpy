"""
define callbacks for the option parser
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


from slimpy_base.Core.Runners.dotRunner import dotRunner
from slimpy_base.Core.Runners.dottestRunner import dottestRunner
from slimpy_base.Core.Runners.multicorerunner import MultiCoreRunner
from slimpy_base.Environment.InstanceManager import InstanceManager
#from slimpy_base.setup.default_options import options
from optparse import OptionValueError
from sys import modules
from pdb import set_trace

__env__ = InstanceManager()


def runner_callback( option, opt_str, value, parser ): #IGNORE:W0613@UnusedVariable
    """
    callback for option parser to set the runner class used by the graphmgr
    """
#    set_trace()
    from slimpy_base.setup.default_options import options
    
    if option == options['dot']:
        runner = dotRunner()
        parser.saw_dot = True
    elif option == options['dottest']:
        runner = dottestRunner()
        
    elif option == options['multicore']:
        parser.values.jobs = int(value)
        # set the node names of the threads to 'master'
        hosts = ['localhost']*int(value)
        __env__['slimvars']['NODELIST'] = hosts
        parser.values.NODELIST = hosts
        
        runner = MultiCoreRunner()
    elif option == options['dist']:
        
        __env__['slimvars']['NODEFILE'] = value
        parser.values.NODEFILE = value
        runner = MultiCoreRunner()
            
    elif option == options['scons']:
        raise OptionValueError( "scons runner no longer supported" )
    else:
        raise OptionValueError( "unknown SLImpy runner for option parser use one of [dot,scons,dottest,jobs]" )

    __env__['graphmgr'].setRunner( runner )

def builder_callback( option, opt_str, value, parser ): #IGNORE:W0613@UnusedVariable
    '''
    callback to set the builder    
    '''
    from slimpy_base.Core.Builders.PipeBuilder import PipeBuilder
    __env__['graphmgr'].set_builder( PipeBuilder(chain=False) )
    
def opts_callback( option, opt_str, value, parser ):#IGNORE:W0613@UnusedVariable
    '''
    print options and exit
    '''
    main = modules['__main__']
    if hasattr(main, "options"):
        main_options = getattr(main, "options")
        for opt in main_options:
            print opt
    raise SystemExit
####################

def optest( option, opt_str, value, parser ):#IGNORE:W0613@UnusedVariable
    """
    run tests and exit
    """    
    from slimpy_base.test_SLIMpy import test
    test()
    raise SystemExit, "tests completed"
