
"""
class uses functional closure to build and execute function
stores callable functions and arguments to be called
by the run method
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
from slimpy_base.Core.Interface.node import Source, Target, Node
from itertools import chain
from pdb import set_trace
from slimpy_base.Core.Command.Drivers.Unix_Pipes import gethostname
import re

from slimpy_base.Environment.InstanceManager import InstanceManager

class Command( object ):
    """
    Base command to be run by a SLIMDataStructure
    takes a function to be run, a tuple and a dict object
    on the run method being called will run the function with
    the given arguments
    """
    env = InstanceManager()
    
    def __init__( self, tag, adder, *params, **kparams ):
        """
        function is a given function to be called by run
        params and kparams are given to the function at 
        runtime
        """
        if isinstance(tag, str):
            self.tag = tag 
            self._func = None
        else:
            self.tag = str(tag)
            self.func = tag 
            
        self.params = list( params )
        self.kparams = kparams
        self._other_dependants = set()
        self.__adder = adder
        self._is_set = False
        
        self._state = dict()
        
        self.node_name = None
        self.tb_info = None
        self.runtime_map = None
        self.num_proc = 1
    
    def add_node_name_to_targets(self):
        """
        @todo explain this better
        """
        if self.command_type == 'multi_process':
            for target in self.target_containers:
                if hasattr(target, 'add_target_to_current'):
                    target.add_target_to_current( )
        else:
            for target in self.target_containers:
                target.add_node_name( self.node_name )
                
        return
    
    def copy_sources(self):
        if self.command_type == 'multi_process':
            for source in self.source_containers:
                source.node_copy( gethostname() )
        else:
            for source in self.source_containers:
                source.node_copy( self.node_name )
                pass
    
    def _get_cmdtype(self):
        return self._state.get('command_type',None)
    
    def _set_cmdtype(self, val):
        self._state['command_type'] = val
    
    command_type = property( _get_cmdtype, _set_cmdtype)
    
    def _set_function(self,val): 
        raise Exception
    
    function = property( fset=_set_function )
    
    def is_set(self):
        return self._is_set
    
    def _get_func(self):
        if not self.is_set( ):
            raise Exception("Function is not set")
        return self._func
    
    def _set_func(self,val): 
        self._is_set = True
        self._func = val
    
    func = property( _get_func, _set_func )
    
    def _get_tag(self):
        return self._tag
    def _set_tag(self,val):
        self._tag = val
    
    def _set_runtime_map( self, map_func ):
        self._state['runtime_map'] = map_func
    
    def _get_runtime_map(self):
        return self._state['runtime_map']
    
    runtime_map = property( _get_runtime_map, _set_runtime_map)
    
    def do_runtime_map(self):
        if self.runtime_map is None:
            params,kparams = self.params,self.kparams
        else:
            params,kparams = self.runtime_map( self )
            
        return params,kparams
        
    tag = property( _get_tag , _set_tag )
    
    def get_nodename(self):
        return self._state['node_name']
    
    def set_nodename(self,val):
        
        self._state['node_name'] = val
        
        if self.is_set() and hasattr( self.func, "node_name" ):
            self.func.node_name = val
        
    node_name = property(get_nodename ,set_nodename ) 
    
    def _get_tb_info(self):
        return self._state['tb_info']
    
    def _set_tb_info(self,val ):
        self._state['tb_info'] = val 
        
    tb_info = property( _get_tb_info, _set_tb_info )
    
    def __getitem__( self, item ):
        """
        return an item from kparams
        
        """
        return self.kparams[item]

    def __setitem__( self, item ,val):
        """
        return an item from kparams
        
        """
        self.kparams[item] = val

    
    def del_kw(self, item):
        del self.kparams[item]
        
    def del_par(self,idx):
        del self.params[idx]
    
    def pop_kw(self,item,*default):
        return self.kparams.pop(item,*default)

    def pop_par(self,*index):
        
        return self.params.pop(*index)
        
    def __contains__( self, k ):
        """
        returns True if the keyword arguments
        contain the key k
        """
        bl = self.kparams.has_key( k )
        return bl
        
    def add_other_dep(self,other):
        self._other_dependants.add(other)
        
    def has_key( self, key ):
        """
        returns True if the keyword arguments
        contain the key k
        """
        return self.kparams.has_key( key )
        
    def __repr__( self ):
        return self.__str__()
    
    def __str__( self ):
        name = self.tag
        
        join = ", ".join
        eq = lambda (a, b): '%s=%s' %( a, b )
        
        
        p_str = join( map(str,self.params) )
        k_str = join( map(eq, self.kparams.items() ) )
            
        if p_str:
            k_str = join( [p_str,k_str] )

        return '<SLIMpy.Command %(name)s %(k_str)s>' % vars()
    
    def _rplace_scalar_str(self, string):
        """
        replace strings representing scalars with the actual 
        value
        """
        re_saclar = re.compile( r'(\$\{SCALAR\[\d*\]\})' )
        scalars_map = self.env['table'].scalars_map
        
        all = re_saclar.findall( string )
        
        for scal in all:
#            print item
            if scal in scalars_map:
                scalar_val = str( scalars_map[scal] )
                string = string.replace(scal, scalar_val )
                
        return string
    
    def _format_params(self):
        if not ( self.params or self.kparams):
            return ""
        else:
            is_node  = lambda x: isinstance(x, Node)
            src_str  = lambda nd: is_node(nd) and str(nd.get()) or str(nd)
            eq       = lambda a,b:"%s=%s" %(a,b)
            ksrc_str = lambda (a,nd): eq(a,src_str(nd))
               
            join = ", ".join
            p = join( [src_str(p) for p in self.params] )
            k = join( [ ksrc_str(key_val) for key_val in  self.kparams.iteritems() ] )
            
            res = p and k and p+", "+k or p or k
            
            return "( %s )" %res
        
    def nice_str(self):
        re_bound_method = re.compile( "(<bound method type\.(.*) of <class '.*\.(.*)'>>)" )
        re_function     = re.compile( "(<function (.*) at .*>)" )        
        
        if self.is_set( ):
            if  'method driver.run' in str( self.func ):
                name = 'driver.run'
            else:
                name = self.func
        else:
            name = self.tag
        
        string = str(name)
        if re_bound_method.match( string ):
            old,meth,cls = re_bound_method.findall( string )[0]
            new = ".".join([cls,meth])
            string = string.replace(old, new)
            
        elif re_function.match( string ):
            old,new = re_function.findall( string )[0]
            string = string.replace(old,new)
        
        string += self._format_params( )
        
        string = self._rplace_scalar_str(string)
                
        return string
        
    def copy( self ):
        """
        returns an identical instance
        params and kparams are copied as well
        """
        com =  Command( self.tag, self.__adder, *self.params, **self.kparams )
        
        if self.is_set():
            com.func =self.func
        com._other_dependants = self._other_dependants.copy( )
        
        com._state = self._state.copy( )    
#        com.runtime_map = self.runtime_map
#        com.tb_info = self.tb_info
#        com.set_num_proc( self.get_num_proc() )
#        com.node_name = self.node_name
        
        
        return com
        
    def __eq__( self, other ):
        
        if isinstance( other, Command ):
            if not self.tag == other.tag:
                return False
            if not self.is_set() == other.is_set():
                return False
            if self.is_set():
                if not other.func == self.func:
                    return False
            if not other.params == self.params:
                return False
            if not other.kparams == self.kparams:
                return False
            
            return True
        else:
            return False
        
    
    def run( self ):
        """
        runs the function given to the command
        with the arguments given 
        """
        return self.func( *self.params, **self.kparams )
    
    def get_all_values(self):
        
        ch = chain( self.params, 
                      self.kparams.values(), 
                      self._other_dependants
                      )
        
        return ch
    
    all_values = property(get_all_values)
    
    
    def getTargets(self):
        'get all targets in this command'
        istarget = lambda args: isinstance( args, Target )
        targets = []
        push = targets.append
        
        for value in self.all_values:
            if istarget( value ):
                push( value )
        return targets
    
    def getSources(self):
        'get all sources in this command'
        issource = lambda args: isinstance( args, Source )
        
        sources = []
        push = sources.append
        
#        c_chain = chain( self.params, self.kparams, self._other_dependants)
        for value in self.all_values:
            
            if issource( value ):
                push( value )
        
        return sources
        
    def _get_target_cont(self):
        table = self.env['table']
        tgts = self.getTargets()
        return [ table[targ.id] for targ in tgts]

    def _get_source_cont(self):
        table = self.env['table']
        srcs = self.getSources()
        return [ table[src.id] for src in srcs]
    
    target_containers = property( _get_target_cont )
    source_containers = property( _get_source_cont )
    
    
    def get_source_spaces(self):
        return [cont.params for cont in self.source_containers if hasattr(cont , "params") ]
    
    def get_structure(self, item, default=None):
        'get a structure'
        if isinstance(item, int):
            src = self.params[item]
        else:
            src = self.kparams[item]
            
        table = self.env['table']
        return table[src.id]
        
    def has_unusedtarget( self ):
        """
        returns true if this command has an
        argument that is a Target class 
        """
        
        all_val = self.get_all_values()
        
        return bool( Target in all_val ) 
            
#        for i in range( len( self.params ) ):
#            if self.params[i] == Target: 
#                return True
#        for k in self.kparams.keys():
#            if self.kparams[k] == Target: 
#                return True
#        return False

    def has_unusedsource( self ):
        """
        returns true if this command has a 
        argument that is a Target class 
        """
        
        return bool( Source in self.all_values )
     
    
    def setunusedtarget( self, target ):
        """
        if this command contains an un-instanciated target class
        then replace it with @parameter: Target
        returns True if un-instanciated Source is found and false if not
        """
        

        if not isinstance( target, Node ):
            target = Target( target )
        
        for i in range( len( self.params ) ):
            if self.params[i] == Target: 
                self.params[i] = target
                return 
        
        for k in self.kparams.keys():
            if self.kparams[k] == Target: 
                self.kparams[k] = target
                return 
        
        if Target in self._other_dependants:
            
            self._other_dependants.remove( Target)
            self._other_dependants.add( target )
            return 
        
        raise Exception( 'No target to set' )
        

    def setunusedsource( self, source ):
        """
        if this command contains an un-instanciated target class
        then replace it with @parameter: Target
        returns True if un-instanciated Source is found and false if not
        """
#        is_str = lambda par: isinstance( par, str)
#        sus = "${SLIMPY_UNUSEDSOURCE}"
#        is_str_src = lambda par: ( is_str(par) and sus in par)

        if not isinstance( source, Node ):
            source = Source( source )
        
        for i,val in enumerate(self.params):
            if val == Source:
                self.params[i] = source
                return 
        
        if Source in self._other_dependants:
            self._other_dependants.remove( Source )
            self._other_dependants.add( source )
            return

        for k,val in self.kparams.iteritems():
            if val == Source: 
                self.kparams[k] = source
                return 
        
        raise Exception( 'No source to set' )
    
    def getAdder( self ):
        
        return self.__adder
    
    
    def setAdder( self, adder ):
        self.__adder = adder
    
    adder = property( getAdder, setAdder )
    
    def __add__( self, other ):
        
        return self.adder( self, other )

        
    def __radd__( self, other ):
        
        return self.adder( other, self )
    
    def _get_num_proc( self ):
        
        return self._state['num_proc']
    
    def _set_num_proc(self,val):
        self._state['num_proc'] = val
    
    num_proc = property( _get_num_proc, _set_num_proc )
     
