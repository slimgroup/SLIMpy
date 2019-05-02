"""
GraphBuilder CLASS
manages the graph,the pipe builder and the runner
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

from slimpy_base.Core.Graph.Graph.DiGraph import DiGraph
from slimpy_base.Core.Interface.ContainerBase import DataContainer
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Environment.Singleton import Singleton
#from slimpy_base.utils.Logger import Log
from slimpy_base.Core.Builders.PipeBuilder import PipeBuilder
from slimpy_base.Core.Runners.defaultRunner import defaultRunner
from slimpy_base.Core.Graph.GraphPrinter import GraphPrinter as printer 
from slimpy_base.utils.Profileable import note


class GraphManager( Singleton ):
    '''
    provides an interface to the graph class 
    '''
    
    def __new_instance__(self, name):
        """
        simalar to init but for singleton
        initializes the class when  a new instance is created
        """
        
        Singleton.__new_instance__(self, name)
        
#        self.log = Log()
        self.env = InstanceManager()
    
        self.graph = DiGraph()
        
        self.__breakpoints = set()
        self.__sources = set()
        self.__targets = set()
        
        self.runner = defaultRunner()
        self.builder = PipeBuilder()
    
    def __str__(self):
        
        i_name = self._instance_name
        srcs = len(self.sources)
        tgts = len(self.targets)
        bps = len(self.breakpoints)
        
        return "<graphmrg{%(i_name)s} %(srcs)s sources, %(tgts)s targets, %(bps)s bp>" %vars()
    
    def __repr__(self):
        return self.__str__()
    
    def getBreakpoints(self):
        'returns breakpoints'
        return self.__breakpoints

    def setBreakpoints(self, value):
        'set breakpoints'
        self.__breakpoints = value

    def getSources(self):
        'get sources'
        return self.__sources

    def setSources(self, value):
        'set sources'
        self.__sources = value

    def getTargets(self):
        'get target'
        return self.__targets

    def setTargets(self, value):
        'set target'
        self.__targets = value
    
    breakpoints = property(getBreakpoints, setBreakpoints, "Breakpoints should be a set of breakpoints")
    sources = property(getSources, setSources, "Sources's should be a set")
    targets = property(getTargets, setTargets, "Targets's should be a set")

    def add_breakpoint(self, bp):
        'adds a breakpoint to the set from a pyhton object'
        bp_id = id(bp)
        self.add_breakpoint_id(bp_id)

    def add_breakpoint_id(self, bp_id ):
        'adds a breakpoint to the set from a pyhton objects id'
        self.breakpoints.add( bp_id )

    def add_source(self, src):
        'adds a source to the set from a pyhton object'
        src_id = id(src)
        self.add_source_id(src_id)

    def add_source_id(self, src_id ):
        'adds a source to the set from a pyhton objects id'
        self.sources.add( src_id )

    def add_target(self, tgt):
        'adds a target to the set from a pyhton object'
        tgt_id = id(tgt)
        self.add_target_id(tgt_id)

    def add_target_id(self, tgt_id ):
        'adds a target to the set from a pyhton objects id'
        assert tgt_id in self.env['table']
        self.targets.add( tgt_id )
    
    def graphAppend( self, commpack ):
        """
        append to the graph all sources and targets found in 'command'
        plus Source and Target
        """
        
        nodelist = commpack.getNodeList()
        
        for i in range( len( nodelist )-1 ):
            self.graph.appendEdge( nodelist[i].getID(), nodelist[i+1].getID(), Etype=True, colour='black' )
        
        commandbeg = nodelist[0]
        commandend = nodelist[-1]
        
        [self.graph.set_node_info( node.id , type='command' ) for node in nodelist]
        
        if commpack.source:
            src_id = commpack.source_node.id
            self.graph.appendEdge( src_id , commandbeg.getID(), Etype=True, colour='red' )
            self.graph.set_node_info( src_id , type='data' )
        if commpack.target:
            tgt_id = commpack.target_node.id
            self.graph.appendEdge( commandend.getID() , tgt_id, Etype=True, colour='green' )
            self.graph.set_node_info( tgt_id, type='data' )
        
        source_set = set( commpack.getSources() )
        
        for source in  source_set:
            self.graph.appendEdge( source.getID(), commandbeg.getID() , colour='red' )
            self.graph.set_node_info( source.id, type='data' )
        
        target_set = set( commpack.getTargets() )
        for target in  target_set:
            self.graph.appendEdge( commandend.getID() , target.getID() , colour='green' )
            self.graph.set_node_info( target.id, type='data' )
            
            
    def get_graph( self ):
        """
        returns the current graph instance that contains the current data and command nodes
        """
        return self._graph
    
    def set_graph( self, graph):
        """
        Set the graph type,
        @pre: graph must be an instance of the SLIMDataStructure type or None
        """
        self._graph = graph
    
    graph = property( get_graph, set_graph)
        
    def set_builder( self, builder ):
        """
        replace the current builders with new ones
        """
        from slimpy_base.Core.Builders.BuilderBase import BuilderBase
        assert isinstance(builder, BuilderBase), "builerd must be an instance of BuilderBase"
        self._builder = builder
        
    def get_builder( self ):
        'return builder instance'
        return self._builder
    
    
    builder = property( get_builder, set_builder ) 
    
    def setRunner( self, runner ):
        """
        replace the current runner with a new one
        if runner is None the current runner becomes 
        the default runner of SLIMpy
        """
        from slimpy_base.Core.Runners.RunnerBase import Runner
        assert isinstance(runner, Runner), "runner must be a subclass of RunnerBase.Runner"
        self._runner = runner
        
    def get_runner(self):
        'returns the current runner instance'
        return self._runner
        
    runner = property( get_runner, setRunner)
        
#    def setBuildTargets( self, *targets ):
#        """
#        set a build target 
#        """
#        self.graph.setBuildTargets( *targets )
#        
#    def buildGraph( self, *targets ):
#        """
#        returns a new graph instance that is make from applying 
#        all builders in order to the current graph
#        """
#        graph = self.graph
#        
#        for builder in self.builders:
#            b = builder( graph , breakpoints=self.getBreakpoints() , *targets )
#            graph = b.toGraph()
#            
#        return graph
    @note("flush is not run in any profile. It is never called with dryrun")
    def flush( self, target ):
        """
        Complement to run , flush uses python objects instead of 
        object IDs to create a command chain
        also flush performs a clean after a graph run has been performed
        """
        
        log = self.env['record'](1, 'stat' )
        print >> log, "SLIMpy: Hold AST Build - Intermediate execution command 'flush' called"
        print >> log, "SLIMpy: Building intermediate target", target 
        print >> log, "SLIMpy: Executing commands ..."

#        import pdb
#        pdb.set_trace()
        target_id = set([ id(target) ]) 
        
        
        graph = self.builder.build( self.graph, target_id, self.sources, self.breakpoints )
        runner = self.runner
        runner.set_graph( graph )
        runner.run()
        
        new_sources = runner.get_new_sources()
        self.sources.update( new_sources )
        
        print >> log, "SLIMpy: Done executing commands"
        print >> log, "SLIMpy: Resuming Building AST"
        
    def addBreakPoint( self, container ):
        """
        @type container: DataContainer
        add container to set of breakpoints
        @precondition: container is in the graph
        @postcondition: the container will always
        be built even if it breaks a pipe
         
        """
        self.__breakpoints.add( id( container ) )
                
    def __clean__( self ):
        """
        for each item in the graph try to remove its data
        """
#        table = self.env['table']
##        for node in self.graph:
##            node = table[node]
##            # if the node is a data container try to remove it 
##            if isinstance( node , DataContainer ):
##                # note: that the remove call only removes
##                # data that are there and not temporary
##                node.remove()
##        
#        #empty the hash of all objects
#        table.clear()
#        
#        from slimpy_base.utils.DotTest import DotTester
#        dt = DotTester()
#        dt.clear()

#        self.log = Log()

    
        self.graph = DiGraph()
        
        self.__breakpoints = set()
        self.__sources = set()
        self.__targets = set()
        
    def Execute(self):
        return self.End( )
    
    def End( self ):
        """
        end  all current slimpy ativity
        runs the graph and cleans all nodes in the
        graph and hash table
        """
        record = self.env['record']
        log = record(1, 'stat' )
        print >> log, "SLIMpy: Done building AST"
        print >> log, "SLIMpy: Executing commands ..."
        
        import time
        
        graph = self.builder.build( self.graph , self.targets, self.sources, self.breakpoints )
        
        record.graph = graph
        
        runner = self.runner
        runner.set_graph( graph )
        
        record.stat( )
        
        numberran = runner.run()
        
        record.stat_done( )
        
        new_sources = runner.get_new_sources()
        self.sources.update( new_sources )
        
        end = time.time( )
        
        disp_log = self.env['record']( 10, 'display' )
        
        # display the command
        print >> disp_log , "Display:"
        print >> disp_log , "\tCode ran in : %5.5s seconds" % time.clock()
        print >> disp_log , "\tComplexity  : %5.5s nodes" % len( self.graph )
        print >> disp_log , "\tRan         : %5.5s commands" % numberran
        print >> disp_log , "GraphBuilder.cleanAll called"    
        
#        if hasattr(runner, 'center'):
#            runner.center.display_stats()
            
#        self.cleanAll()
#        self.env.del_instance( self.env.current_env )
        print >> log, "SLIMpy: Done executing commands"
        return numberran

#    def addSource( self, container ):
#        """
#        add a source to the graph
#        can be a hash value or a container
#        """
#        
#        
#        # in the case that the con
#        if isinstance( container, int ):
#            self.graph.addSource( container )
#        elif isinstance( container, DataContainer ):
#            self.env['table'].addSource( id(container) )
#            # if the container is not full
#            # it can not be a source
#            if not container.isfull():
#                pass #raise TypeError, "%(container)s in not a source" %vars()
#            self.graph.addSource( id( container ) )
#            
#        else:
#            raise TypeError, "%(container)s must be either a container or an integer" %vars()

#    def isSource( self, val ):
#        """
#        test if a value is a source uses the 
#        adc.isfull method
#        @raise KeyError: if val is not in the HashTable
#        """
#        # try and get the value from the hash
#        table = self.env['table']
#        try:
#            val =  table[val]
#        except KeyError:
#            return False
#        
#        if isinstance( val, DataContainer ):
#
#            return val.isfull()
#
#        return False
    
    def printAdj( self, v ):
        """
        prints graph instance
        """
        from slimpy_base.Core.Interface.AbstractDataInterface import ADI
        
        if isinstance( v, ADI ):
            v = v.getContainer()
        if isinstance( v, DataContainer ):
            v = id( v )
        
        return printer.printAdj( self.graph, v )
    
    def printInvAdj( self, v ):
        """
        prints graph instance
        """
        from slimpy_base.Core.Interface.AbstractDataInterface import ADI
        
        if isinstance( v, ADI ):
            node = v.container()
        if isinstance( v, DataContainer ):
            node = id( v )
        else:
            node = v
        return printer.printInvAdj( self.graph, node )
        
    def printDep( self ):
        """
        prints graph instance
        """
        return printer.printDep( self.graph )
    
    def printInvDep( self ):
        """
        prints graph instance
        """
        return printer.printInvDep( self.graph )

    def toDot( self ):
        """
        prints a dot file
        """
        printer.toDot( self.graph )

