"""

For parsing commandline values
into a dictionary

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


from slimpy_base.Environment.InstanceManager import InstanceManager
from optparse import OptionParser, OptionGroup
from sys import argv, modules
from slimpy_base.setup.default_options import options


def make_version( ):
    '''
    return a nicely formatted version string
    '''
    import slimpy_base
    main = modules["__main__"]
    
    lines = []
    push = lines.append
    if hasattr( main, "__version__" ):
        push( main.__version__ )
    push( slimpy_base.__version__ )
    push( slimpy_base.__license__ )
    
    return "\n".join(lines)
    
class SlimOptionParser( OptionParser ):
    """
    a subclass for optparse.OptionParser
    """
    
    def __init__( self ,*arg, **kw):
        '''
        
        '''
        new_kw = dict( version=make_version() )
        new_kw.update(kw)
        
        OptionParser.__init__(self, *arg, **new_kw )
        
        self._required = set()
        
        self._types = {}
        self._defaults = {}
        self._prog_args = []
        
        self.env = InstanceManager()
        
        self.add_all_slim_options( )
        
        from slimpy_base.setup.DEFAULTS import DEFAULTS
        
        self.set_defaults( **DEFAULTS )
        
    def Types(self, *E, **kw):
        '''
        set the type for a prameter
        parse retuns values from type as Type[key]
        '''
        
        self._types = dict(*E, **kw)
        
    def Parameters(self, *args):
        """
        set parameters for 
        """
        self._prog_args = list(args)
        
    def Defaults(self,  *E, **kw):
        self._defaults = dict( *E, **kw )
    
    def new_group(self, title, doc, *opts):
        '''
        add a group of title and with 'doc' to the parser 
        @param title:
        @type title: str
        @param doc:
        @type doc: str
        '''
        title += ":\n  " + "="*len(title) 
        group = OptionGroup(self, title, doc)
        for opt in opts:
            group.add_option( options[opt] )
        self.add_option_group( group )
        
        return
        
    def add_the_rest(self):
        """
        add any options that are not in a group
        """
        for option in options.values():
            opt_str = option.get_opt_string()
            if self.has_option(opt_str):
                pass
            else:
                self.add_option( option )
    
    def _getit(self, par):
        'helper function'
        ret = self._defaults.get( par, self._types.get(par,'X') )
        return par, hasattr(ret, "__name__") and "'%s'"%ret.__name__ or ret

    def _set_usage( self ):
        '''
        sets usage parameter of parser with data
        collected from the '__main__' module 
        '''
        maintmp = modules['__main__']
        
        if self._prog_args:
            strs = [ "%s=%s" %self._getit(par) for par in self._prog_args ]    
            opstr =", ".join( strs ) #IGNORE:W0612@UnusedVariable
            usage="python %%prog [ options ] [ %(opstr)s ]" %vars()
                
#            self.set_usage("python %prog [options] [program parameters]")
        
        elif hasattr( maintmp, 'usage' ):
            usage = maintmp.usage
#            parser = OptionParser( usage=maintmp.usage+maintmp.__doc__ )
        else:
            usage = "python %prog [slim options] [program options]"
            
        if maintmp.__doc__:
            spacer = '\n' + "-"*(len(usage)+10)
            usage+=spacer+"\n"+maintmp.__doc__.strip("\n ")+spacer
        
        OptionParser.set_usage(self, usage)

    def add_all_slim_options(self):
        '''
        add options from default_options module
        '''
        # Add Options in groups
        self.new_group("MPI Utilities", "mpi related functions",
                       "mpi","no_mpi","mpi_run","mpi_flags",
                       )

        self.new_group('Distributed',"helper funcs for '--dist' option "
                       "(see Runners)",
                        'eps','nwin')
        
        self.new_group('Data-path', "direct data flow",
                        'localtmpdir', 'globaltmpdir')
        
        self.new_group( "Output", "control the output" ,
                        'verbose', 'quiet' ,'log','debug')
        
        self.new_group("Runners", 
                       "runners determine what SLIMpy does with the comands and data",
                       'scons','dot','dottest','dryrun','multicore' ,'test' ,'dist')
        
        self.new_group("Sanity Checks", "Determines how much checking is done at 'compile time'",
                       'check_paths','strict_check','no_check_paths','walltime')
        
        self.add_the_rest()

    
    def parse( self , *args):
        """
        parse all slimpy options into global vars and return 
        a list of all commandlist parameters not used in the option
        parse.
        """
        log = self.env['record'](1, 'stat' )
        
        print >> log, "SLIMpy: Building AST ..."

        self.set_defaults( runtype='normal' )
        
        self._set_usage()

        # Parse Args
        opts , args = self.parse_args( *args )
        
        ib = lambda b: int(bool(b))
        tot = ib(opts.jobs) + ib(opts.mpi) + ib(opts.mpi)
        
        if tot > 1: # more that one option selected
            self.error( "options -j/--jobs, --mpi and --dist "
                        "are mutualy excusive\n"
                        "please choose only one option\n" )
        
        globcpar = opts.__dict__

        self.env['slimvars'].setglobal( **globcpar )
        
        
        cpar = self.clp( *args )
        
        self._check_required( cpar)
        
        cpar_and_defaults = self.set_types(cpar)
             
        return cpar_and_defaults
    
    def set_types(self, cpar):
        '''
        convers the string values in cpar to the 
        corresponding type in self._types
        
        retuns defaults updated with new typed cpar 
        '''
        if self._types:
            for atype in self._types:
                if cpar.has_key(atype):
                    try:
                        cpar[atype] = self._types[atype]( cpar[atype] )
#                        print atype, cpar[atype]
                    except Exception, exc: #IGNORE:W0703
                        type_name = self._types[atype].__name__ #IGNORE:W0612@UnusedVariable
                        value = cpar[atype] #IGNORE:W0612@UnusedVariable
                        exc_type = exc.__class__#IGNORE:W0612@UnusedVariable
                        msg=( "could not convert arg '%(atype)s' with value '%(value)s' to type '%(type_name)s'\n"
                              "got - %(exc_type)s: %(exc)s" %vars() )
                        self.error( msg )
        
        _defaults = dict(self._defaults)
        
        _defaults.update( cpar )
        
        return _defaults
     
    def check_required( self, *args ):
        '''
        add parameter to be checked when parse args is called
        if more that one arg then will check that only
        one of the arguments from args exists
        '''
        if len(args) == 1:
            arg = args[0]
            self._required.add( arg)
        elif len(args) > 1:
            self._required.add( args )
            
        return
        
    def _check_required(self, pars):
        '''
        raise an exception if a key specified in 
        pars is not in pars
        
        @param pars:
        @type pars: dict
        '''
        
        for par in self._required:
            if isinstance(par, tuple):
                pars_set = set( pars )
                par_set = set( par )
                if len(pars_set.intersection(par_set)) < 1:
                    opstr ="= | ".join( par )+"=" #IGNORE:W0612@UnusedVariable
                    self.error("at least one of [ %(opstr)s ] "
                                      "parameters must be supplied\n" %vars())
            
            elif par not in pars:
                self.error("parameter '%s=' not supplied\n" %par)
        
    def clp( self, *arg ):
        """
        parse the comand line *args is a list of keys as of file
        """
        if len( arg ) is 0:
            arg = argv
        par = {}
        for i in range( 0, len( arg ) ):
            
            spl = arg[i].split( "=" )
            if len( spl ) is 2:
                if spl[1] is 'None':
                    par[spl[0]] = None 
                else:
                    par[spl[0]] = spl[1]
        return par

#===============================================================================
# end
#===============================================================================
