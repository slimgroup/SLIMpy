"""
@mainpage SLIMpy 
  
This page has been generated from the source code of SLIMpy. 
    
@section intro Introduction
SLIMpy is a Python interface that exposes the functionality of seismic
data processing packages, such as MADAGASCAR, through operator
overloading. SLIMpy provides a concrete coordinate-free
implementation of classes for out-of-core linear (implicit
matrix-vector), and element-wise operations, including calculation of
norms and other basic vector operations. The library is intended to
provide the user with an abstract scripting language to program
iterative algorithms from numerical linear algebra. These algorithms
require repeated evaluation of operators that were initially designed
to be run as part of batch-oriented processing flows. The current
implementation supports a plugin for Madagascar's out-of-core UNIX
pipe-based applications and is extenable to pipe-based collections of
programs such as Seismic Un*x, SEPLib, and FreeUSP. To optimize
performance, SLIMpy uses an Abstract Syntax Tree that parses the
algorithm and optimizes the pipes.


@section Installation Installation

@subsection Prerequisites Prerequisites

 - \b Python
   SLIMpy is written in pure Python. 
   - see http://www.python.org 
   - python 2.5 is required 
 - \b SCons
   is a build tool similar to make. 
   - see http://www.scons.org
   - scons 0.98+ is required
 - \b svn
   is a version control client similar to cvs 
   - see http://www.subversion.tigris.org
 - \b Madagascar
   is an open-source software package for geophysical data processing and reproducible numerical experiments. 
   - see http://rsf.sourceforge.net/

@subsection DandI Download and Install

To install SLIMpy check it out of the SLIMpy repository by using the commands:
@code
    [shell]$ svn co https://wave.eos.ubc.ca/Public/Public.Software.SLIMpy/STABLE ./core 
    [shell]$ svn co https://wave.eos.ubc.ca/Public/Public.Software.SLIMpy-contrib/STABLE ./contrib
@endcode

Once the files are on your machine from both the core and contrib directories run:
@code
    [shell]$ python setup.py install [--prefix=/path/to/mypython]
@endcode

\note If you use the \b --prefix option the path you set \b must be on your \b PYTHONPATH.

@section quickstart Quick Start Guide
 - @subpage tutpage 
 - @ref slimpyopers

@section REFERENCE Reference
  
  If you are just browsing the SLIMpy documentation the best place to start 
  is from the groups: 
    @arg @ref userclasses
    @arg @ref functions 
    @arg @ref linop.


@section HELP Help

SLIMPy is an academic research code which we share with the community
through this alpha release. By releasing SLIMpy as open source, we
hope to create an active community to help us further develop this
software.

Through this release, we hope that SLIMpy can grow into a widely-used
library, supplementing the functionality of currently available
processing-flow oriented (seismic) software packages.  Please, use
SLIMpy-user (http://slim.eos.ubc.ca/mailman/listinfo/slimpy-user)
mailing list to report concerns and exchange the ideas. Those of you,
who wish to contribute to development, please, subscribe to
SLIMpy-devel (http://slim.eos.ubc.ca/mailman/listinfo/slimpy-devel).

@section features Features
The main features of SLIMpy include:

- Powerful interpreted programming language (Python)
- Syntax (through overloading) close to pseudo-code for numerical linear algebra
- Abstract Syntax Tree analyzer/optimizer (including command rearrangement form improved performance)
- Concrete linear operator and vector classes, including dottests, domain-range
  and type checks
- Elementwise reduction-transformation operations (norms, elementary
  math)
- Compounded linear operators
- Augmented linear operators and vector classes
- Plugin mechanism for Unix pipe-based collections of (seismic) data processing programs
- Parallel execution of reduction/transformation operations
- Parallel execution of embarrassingly parallel linear operators (block diagonal) 
- Integration with SCons
- Automatic cleanup of temporary datafiles (garbage collection)
- In-code documentation through Doxygen 

@section LICENCE License

%SLIMpy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

%SLIMpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SLIMpy . If not, see http://www.gnu.org/licenses/

For the full licence, please see the @subpage licencefile and @subpage licencefilelesser 
files.


@author Sean Ross-Ross
@date May 22, 2008 


 
@page licencefile COPYING
\verbinclude COPYING
@page licencefilelesser COPYING.LESSER
\verbinclude COPYING.LESSER


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


#import distutils.command.install
from distutils.core import setup
from os.path import join
from glob import glob


slimpy_base_packages = [
    
"slimpy_base",
"slimpy_base.api",
"slimpy_base.api.functions",
"slimpy_base.api.linearops",
"slimpy_base.api.Plugins",
"slimpy_base.api.Plugins.slim2numpy",
"slimpy_base.api.Plugins.slim2rsf",
"slimpy_base.api.Plugins.slim2rsf.sfcommands",
"slimpy_base.api.Plugins.slim2su",
"slimpy_base.Core",
"slimpy_base.Core.Builders",
"slimpy_base.Core.Command",
"slimpy_base.Core.Command.Drivers",
"slimpy_base.Core.Graph",
"slimpy_base.Core.Graph._dep_Builders",
"slimpy_base.Core.Graph.Graph",
"slimpy_base.Core.Interface",
"slimpy_base.Core.MutiProcessUtils",
"slimpy_base.Core.Runners",
"slimpy_base.Core.User",
"slimpy_base.Core.User.linop",
"slimpy_base.Core.User.Structures",

"slimpy_base.Environment",
"slimpy_base.setup",
"slimpy_base.SLIMmath",
"slimpy_base.test_SLIMpy",
"slimpy_base.test_SLIMpy.test_Core",
"slimpy_base.test_SLIMpy.test_Core.test_Command",
"slimpy_base.test_SLIMpy.test_Core.test_Command.test_Drivers",
"slimpy_base.test_SLIMpy.test_Core.test_Graph",
"slimpy_base.test_SLIMpy.test_Core.test_Graph.test_Builders",
"slimpy_base.test_SLIMpy.test_Core.test_Graph.test_Graph",
"slimpy_base.test_SLIMpy.test_Core.test_Interface",
"slimpy_base.test_SLIMpy.test_Core.test_MultiCore",
"slimpy_base.test_SLIMpy.test_Core.test_Plugins",
"slimpy_base.test_SLIMpy.test_Core.test_runners",
"slimpy_base.test_SLIMpy.test_Core.test_User",
"slimpy_base.test_SLIMpy.test_Core.test_User.test_linop",
"slimpy_base.test_SLIMpy.test_env",
"slimpy_base.test_SLIMpy.test_User",
"slimpy_base.test_SLIMpy.test_User.test_AugmentedMatrix",
"slimpy_base.test_SLIMpy.test_utils",
"slimpy_base.User",
"slimpy_base.User.AumentedMatrix",
"slimpy_base.utils", ]

slimpy_package = [ 'SLIMpy' ]

proj_packages = [
"slimproj_core",
"slimproj_core.builders",
"slimproj_core.slim_tools" ]

Utils_packages = [
"SLIMutils",
      ] 

modules = [ 'slimproj' ]
scripts_dir = join( "scripts" , "*")
scripts = glob( scripts_dir )
all_packages = slimpy_base_packages + slimpy_package + proj_packages + Utils_packages

#cmdclass={ 'install_man': install_man,
#           'install':     install_with_man,
#           'build' :      build_with_man  }      

from svninfo import tofile
try:
    tofile( "slimpy_base/info.py" )
except:
    print "Could not upate SLIMpy.__version__ from svn"
    


setup(
      name='SLIMpy',
      version='0.3',
      description='Python Interface to ANA',
      author = "Sean Ross-Ross",
      author_email='srossross@gmail.com',
      url='http://slim.eos.ubc.ca/SLIMpy' ,
      
      packages = all_packages,
      py_modules = modules,
      scripts=scripts,
#      cmdclass=cmdclass,      
     )

