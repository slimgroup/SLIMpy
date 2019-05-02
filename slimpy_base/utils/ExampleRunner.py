"""
runs examples in examples package with text output
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


from slimpy_base import __file__ as SLIMpyfile
from glob import glob
from os.path import basename, dirname, join
from sys import stdout 


def getExampleDirs():
    """
    returns all of the packages in the example directory
    """
    
    dir = dirname( SLIMpyfile )
    tpath = join( dir, "examples", "*" )
    exampledirs = glob( tpath )
    
    try: exampledirs.remove( join( dir, "examples", "__init__.py" ) )
    except: pass
    try: exampledirs.remove( join( dir, "examples", "__init__.pyc" ) )
    except: pass
    return exampledirs

def runexample( name, run, clean ):
    """
    run an example
    @param run: must be a callable object with no
        parameters
    @param clean: must be a callable object with no
        parameters
    """
    moderrors = 0
    print "%(name)20s" % vars(), "...", 
    stdout.flush() 
    try:
        run()
    except EnvironmentError, msg:
        print msg, "- Skipping test."
        
    except Exception, msg:
        print "ERROR"
#        raise
        moderrors = 1
    else:
        print "ok"
        
    try:
        err = clean()
        if err:
            print "Error with Clean" 
    except:     #IGNORE:W0704
        pass    #IGNORE:W0702
    return moderrors

def runExamples():
    """
    fetch all examples and run them
    
    @postcondition: exceptions NotImplementedError and Environment Error
    will not count as errors 
    """
    num = 0 
    exampledirs = getExampleDirs()
    
    errors = 0

    for examples in exampledirs:
        
        moderrors = 0
        name = basename( examples )
        
        print "%(name)s ..." %vars() , 
        try:
            mod = __import__( ".".join( ["SLIMpy.examples", name] ), globals(), locals(), name )
            if hasattr(mod, 'canrun'):
                mod.canrun()
            else:
                print mod
                raise AttributeError("module has no attr: canrun")
        except NotImplementedError,msg:
            print msg
        except AttributeError, msg:
            print msg
            moderrors += 1
        except:
            print "Failed to Import"
            moderrors += 1
        else:
            print 
            for name, run, clean in mod.get():
                num += 1 
                if run is None:
                    print "%(name)20s" % vars(), "...", "Error: Could not Import"
                    moderrors += 1
                else:
                    err = runexample( name, run, clean )
                    if err:
                        moderrors += 1
        if moderrors:
            print " ... Module: FAIL"
            errors += moderrors
        else:
            print " ... Module: PASS"
        
    return errors, num

