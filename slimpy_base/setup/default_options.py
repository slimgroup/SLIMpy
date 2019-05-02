"""
define a dict of Option objects for the option parser to use
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


from optparse import Option

from slimpy_base.setup.option_callbacks import builder_callback
from slimpy_base.setup.option_callbacks import runner_callback
from slimpy_base.setup.option_callbacks import optest
from slimpy_base.setup.option_callbacks import opts_callback

#from slimpy_base.setup.DEFAULTS import DEFAULTS as slimvars

options = dict( 
    
    
    verbose=Option( "-v", "--verbose", 
                      metavar="VERB", 
                      dest="verbose", 
#                      default=slimvars['verbose'], 
                      help="print various outputs to "
                           "stderr 0 to 10 [default=1]" ), 
    
    memsize=Option( "-m", "--memsize", 
                      metavar="MEM", 
                      dest="memsize", 
#                      default=slimvars['memsize'], 
                      help="memory size to pass to out-of-core"
                           " functions in MB [default 500]" ), 
    
    quiet=Option( "-q", "--quiet", 
                      action="store_false", 
                      dest="verbose", 
                      metavar="VERB", 
                      help="print no output to stderr" ), 
    
    check_paths=Option( "-c", "--check-paths", 
                      action="store_true", 
                      dest="check_path", 
#                      default=slimvars['check_path'], 
                      help="check executable paths before running programs" ), 
    
    strict_check=Option( "--strict-check", 
                      metavar="SC", 
                      type="int", 
#                      default=slimvars['strict_check'], 
                      dest="strict_check", 
                      help="check spaces for correctness "
                            "can be 0,1 or 2. "
                            "SC=0 no spaces are checked and error are caught only by executables, "
                            "SC=1 spaces are checked for correctness, "
                            "SC=2 spaces are checked for correctness and no voidSpaces are accepted "
                            ), 
    
    no_check_paths=Option( "--no-check-paths", 
                      action="store_false", 
                      dest="check_path", 
                      help="do not check executable paths "
                           "before running programs [default] " ), 
    
#    tmpdir=Option( "-t", "--tmpdir", 
##                   default=slimvars['tmpdir'], 
#                   help="Temporary directory to store "
#                        "header information" ), 
                                          
#    tmpdatapath=Option( "--tmpdatapath", 
#                       dest="tmpdatapath", 
#                       metavar="TDP", 
##                       default=slimvars['tmpdatapath'], 
#                       help="Directory to store temporary binary data" ), 
                      
    globaltmpdir=Option( "-t", "--tmpdir","--globaltmpdir", 
#                         default=".", 
                         metavar="GTD", 
                         dest='globaltmpdir',
                         help="Global temporary directory. Directory to store temporary data"
                              "In parallel computation it is used to share data." ), 
                      
    localtmpdir=Option(  "--localtmpdir", 
#                       default='/var/tmp', 
                       metavar="LTD", 
                       dest='localtmpdir',
                       help="Local SLIMpy temporary data directory."
                       "In parallel computation it is used to work locally." ), 
                      
    eps=Option( "--eps", 
#                default=slimvars['eps'], 
                help="Parallel only. Domain decomposition overlap"
                     " parameter. Common across all dimensions." ), 
                      
    nwin=Option( "--nwin", 
#                 default=str( slimvars['nwin'] ), 
                 help="Parallel only. Defines domain decomposition across "
                       "all dimensions. 2-digit values for each" 
                       "dimension are given together, i.e. --nwin=020407 "
                       "gives 2 windows along the 1st dimension, 4 along"
                       " the 2nd, 7 along the 3rd" ), 
    
    scons=Option( "--scons",
                 action='callback', 
                 callback=runner_callback, 
                 help="""output a scons file to stdout\n NOT MAINTAINED""" ), 
    
    dot=Option( '-d', "--dot", 
               action='callback', 
               callback=runner_callback, 
               help="""output a dot file to stdout""" ), 
               
    dottest=Option( "--dottest", 
                   action='callback', 
                   callback=runner_callback, 
                   help="dryrun the script and run dotests on all"
                        "linear operators that were defined" ), 
    
    multicore=Option( '-j',"--jobs", 
                   action='callback', metavar='N', 
                   type=int,
                   nargs=1,
                   callback=runner_callback,
                   help="Allow N jobs at once" ), 
    
    no_pipe=Option( "--no-pipe", 
                   action='callback',
                   callback=builder_callback,
                   help="do not chain commands into pipe" ), 
    
    dryrun=Option( "-n", "--dryrun", 
                  action='store_const', 
                  const="dryrun", 
                  dest='runtype', 
                  help="print output only do not run commands" ), 
    
    no_del=Option( "--no-del", 
                      action="store_true",
                      dest="no_del",
#                      default=False,
                      help="Does not perform cleaning during, cleans tmp variables at end." ),            
           
    log=Option( "-l", "--log", 
               dest='logfile', 
#               default=None, 
               metavar="FILE", 
               help="log file to write all output to, view with SLIMpy's record_viewer" ), 
    
    debug=Option( "-o","--debug", 
                   dest='debug', 
                   action='append',
    #                   default='nodebug',
                   help="print output only relative to "
                        "crertain debug types:\n"
                        "cleaner\ndisplay\nsolver" ), 
    
    mpi=Option( "--mpi","--enable-mpi" ,
                   dest='mpi', 
#                   default=slimvars['mpi'],
                   action="store_true", 
                   help="enable mpi" ), 
    
    dist=Option( "--dist","--distributed" ,
                   dest='dist',
                   type=str, 
                   nargs=1,
                   action='callback',
                   callback=runner_callback, 
                   help="enable distributed slimpy" ), 
    
    walltime=Option( "--walltime" ,
                   dest='walltime', 
#                   default=slimvars['walltime'],
                   type=int, 
                   help="time-out in seconds for each command" ), 
    
    
    no_mpi=Option( "--no-mpi","--disable-mpi" ,
                   dest='mpi', 
                   action="store_false", 
                   help="enable mpi" ), 
    
    
    mpi_run=Option( "--mpi-run", 
                   dest='MPIRUN', 
#                   default=slimvars['MPIRUN'],
                   help="mpi executable" ),
    
    mpi_flags=Option( "--mpi-flags", 
                   dest='MPIFLAGS', 
#                   default=slimvars['MPIFLAGS'],
                   help="mpi flags" ),    
          
    test=Option( "--test", 
                 action='callback', 
                 callback=optest, 
                 help="run a test suit to test "
                      "the slimpy framework and exit" ), 
    
    #    version=Option( "--version", 
    #                    action='callback', 
    #                    callback=printversion, 
    #                    help="Print the current SLIMpy version and exit" ), 
    
    opts=Option( "--options", 
                action='callback', 
                callback=opts_callback, 
                help="Iternal use for shell script completion" ), 
)

