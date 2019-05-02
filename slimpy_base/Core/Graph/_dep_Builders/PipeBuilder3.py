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

"""
Main class for pipe Optimization
"""

from slimpy_base.Core.Graph.Builders.SLIMBuilder import SLIMBuilder
from slimpy_base.Core.Graph.Graph.DiGraph import DiGraph



class PipeBuilder( SLIMBuilder ):
    """
    Build the graph into a new graph where all 
    the commands are represented as tuples
    """

    
    def __init__( self, g, *targets, **k ):
        
        for t in targets:
            assert t in g, "target %(t)s not in graph %(g)s " %vars()
        
        self.sourcesFlag = k.get( 'useSources', True )
        self.breakpoints = k.get( 'breakpoints', set() )
        self.G = g
        self.lst = []
        self.done = {}
        
        # build up the working set to include all of the targets
        workingSet = set( targets )
        workingSet.update( self.G.getBuildTargets() )
        
        self._colour = dict.fromkeys( workingSet, 'black' )
        
        self.workingSet = workingSet

        self.build()
        
    
    def colour_grey(self,node):
        self._colour[node] = 'grey'
    
    def colour_white(self,node):
        self._colour[node] = 'white'
        
    def colour( self, node ):
        """
        get the colour of the node
        """

        sf = self.G.isSource( node ) and self.sourcesFlag
        
        if sf or self._colour.get( node, 'white' ) == 'grey':
            return 'grey'
        else:
            return 'white'
    
            
 
    
    def dynHelper( self, alpha ):
        
        beta = None
        depFlag = False
        delta = []
        
        edgeColour = self.G.getEdgeColour
        edgeType = self.G.getEdgeType
        for prev in self.G.invAdj( alpha ):
            
            #flag if the edge type Etype 'stdin' is true
            stdinFlag = edgeType( alpha, prev )

            
            
            if stdinFlag and not beta:
                beta = prev
                depFlag = len( self.G.adj( prev ) ) <= 1
                
            else:
                delta.append( prev )
            #
            # the depflag is 
            # beta: that there is a stdin previous object
            # depflag: there is only one object in total before alpha
            # and that beta is not already registered in the working set
        depFlag = beta and depFlag and not beta in self.workingSet
        
        # if there is a stdin but not used and it is a command -> data relationship
        if beta and ( not depFlag ) and edgeColour( beta, alpha ) == 'green':
            # Ignore the command and add the data to the working set
            depFlag = 'b1'

        if not beta and ( not depFlag ) and delta and edgeColour( delta[0] , alpha ) == 'green':
            depFlag = 'b2'

        # nxt is the forward if the edgecolour is green ( i.e. command -> data )
        nxt = [ node for node in self.G.adj( alpha ) if edgeColour( alpha, node ) != 'red' ]
        
        if beta in self.breakpoints:
            depFlag = False
            
        
        
        return depFlag, beta , delta , nxt 
    
    
    def nxtupdate( self, nxt, TSC ):
        
        nxt = set( nxt )
        
        nxt.difference_update( TSC['Command'] )
            
        nxt.difference_update( TSC['Target'] )
        
        return nxt
        
    def build ( self ):
        """
        main method to assemble the pipe into the useable structure
        """
        workingSet = self.workingSet

        
        # while the working set is not empty
        # we pop one off and use it 
        # TODO: this loop is to add all of the pipe
        TSC = None
        while workingSet:
            
            # alph is the main node to work on in the loop

            print >> self.log( 10, 'pipebuilder' ), 'Working set: %(workingSet)s' %vars()
            
            alpha = workingSet.pop()
            
            print >> self.log( 10, 'pipebuilder' ), 'alpha = %(alpha)s' %vars()          
            # if this node is marked as processed then we
            # go on to use the next one
            if self.colour( alpha ) == 'grey':
                continue
            # set the node to used status
            self.colour_grey(alpha)
            
            # to keep track off all the dependencies
            # we use a dict containing the targets sources and Command
            # where the command is a list of the pipeable object
            
            TSC =  {'Target':[alpha], 'Command':[alpha], 'Source':[]}
            
            # record the TSC into a permanent structure
            self.lst.insert( 0, TSC )
            
            
            pipeFlag = True
            # this next loop is to add all of the pipeable
            # objects to the TSC['command']
            while pipeFlag:
                print >> self.log( 10, 'pipebuilder' ), '\nwhile pipeFlag: alpha=%(alpha)s' %vars()
                # use the dynHelper on alph to get the pipeable newxt command
                # if there is one
                # delta the none stdin sources of alpha and
                # pipeFlag the flag to stop the loop if there we do not want
                # to continue with the current pipe
                pipeFlag , beta , delta , nxt  = self.dynHelper( alpha )
                if not ( pipeFlag or beta or delta or nxt ):
                    #TODO: make a better way to do this!
                    print >> self.log( 10, 'pipebuilder' ), '\Adding %(alpha)s to the source of the pipe' %vars()
                    TSC['Source'].append( alpha )


                
                print >> self.log( 10, 'pipebuilder' ), '\tpipeFlag=%(pipeFlag)s , beta=%(beta)s , delta=%(delta)s , nxt=%(nxt)s' %vars()

                
                # update nxt to remove any items in the pipe or are already a target
                nxt = self.nxtupdate( nxt, TSC )
                
                TSC['Target'].extend( nxt )
                if nxt: 
                    print >> self.log( 10, 'pipebuilder' ), '\taddind %(nxt)s to Targets' %vars()
                    
                    if not self.G.getEdgeColour( alpha, list( nxt )[0] ) == 'red'  :
                        if TSC['Target'].count(alpha):
                            TSC['Target'].remove( alpha )
                        print >> self.log( 10, 'pipebuilder' ), '\removing %(alpha)s from Targets' %vars()
                
                
                # in the case that alpha is data and beta is a command that
                # produces two outputs
                if pipeFlag == "b1":
                    
                    TSC['Source'].append( alpha )
                    print >> self.log( 10, 'pipebuilder' ), '\tappending alpha to source' %vars()            


#                    print 'Source append -' , alpha, TSC

                    #TODO: Make 'Target' include all the targets
                    TSC =  {'Target':[alpha], 'Command':[alpha], 'Source':[]}
                    print >> self.log( 10, 'pipebuilder' ), '\tCreating new pipe %(TSC)s' %vars()            
                    # record the TSC into a permanent structure
#                    self.Colour[alpha] = 'grey'
                    self.colour_grey(alpha)
                    self.lst.insert( 0, TSC )
                    
                    ab = set( self.G.adj( beta ) )
                    ab.symmetric_difference_update( TSC['Target'] )
                    TSC['Target'].extend( ab )
                    if ab: 
                        print >> self.log( 10, 'pipebuilder' ), '\tadding ab - %(ab)s to target of new pipe' %vars()            
                    
                    
                # this is in the case that a data dose have a non
                # stdin dependency data must be discarded
                if pipeFlag == 'b2':
#                    print 'b2 spotted' , alpha,beta ,delta
                    if len( TSC['Command'] ) == 1:
                        if len(delta) == 1:
                            if self.colour(delta[0]) == 'grey':
                                self.lst.remove(TSC)
                                pipeFlag = None
                            else:
                                TSC['Command'] = delta
                                alpha = delta[0] 
                                delta = []
                        else:
                            print >> self.log( 10, 'pipebuilder' ), '\tremoving pipe %(TSC)s' %vars()
                            self.lst.remove( TSC ) 
                            pipeFlag = None
                            print >> self.log( 10, 'pipebuilder' ), '\tsetting pipeFlag to None' %vars()
                    else:
                        TSC['Source'].extend( [alpha] )
#                        self.lst.insert( 0, TSC )
#                        TSC = {'Target':[alpha], 'Command':[delta[0]], 'Source':[]}
                        workingSet.add( alpha )
#                        self.Colour[alpha] = 'white'
                        self.colour_white(alpha)    
                        delta = []
                        pipeFlag = None
                        print >> self.log( 10, 'pipebuilder' ), '\tsetting pipeFlag to None' %vars()
                    
                
                # add all of the current dependencies to the working set
                workingSet.update( delta )
                if delta: print >> self.log( 10, 'pipebuilder' ), '\tupdate the working set with %(delta)s' %vars()
                # and to the sources of the current command
                TSC['Source'].extend( delta )
                if delta: print >> self.log( 10, 'pipebuilder' ), '\tadding %(delta)s to the source of pipe' %vars()
                # if there is a beta add it to the command
                if beta:
                    # 
#                    if alpha:
#                        TSC['Command'].insert(0, alpha)
#                        alpha = None
                    
                    TSC['Command'].insert( 0, beta )
                    print >> self.log( 10, 'pipebuilder' ), '\tadding %(beta)s to the beginning of command' %vars()
                    alpha = beta
                    
                    
                    if self.colour( beta ) == 'grey':
                        print >> self.log( 10, 'pipebuilder' ), '\t%(beta)s is grey changing pipeFalse to False' %vars()
                        pipeFlag = False
                        
                    
                    if not pipeFlag:
                        workingSet.add( beta )
                        print >> self.log( 10, 'pipebuilder' ), '\tadding %(beta)s to working set' %vars()
                    else:
                        # if beta is added to the working set 
                        # it can not be set to grey
#                        self.Colour[beta] = 'grey'    
                        self.colour_grey(beta)

                print >> self.log( 10, 'pipebuilder' ), '\tTSC: %(TSC)s\n' %vars()
                        
            
            if beta:
                print >> self.log( 10, 'pipebuilder' ), 'adding %(beta)s to source of pipe\n' %vars()
                TSC['Source'].append( beta )
                
    
    
    def toGraph( self ):
        """
        return graph representation of built object
        """
        g = DiGraph()
        
        for l in self.lst:
            if l['Source'] == l['Command'] == l['Target']:
                continue
            s_diff = list(set(l['Source']).intersection( set(l['Target']) ))
            if s_diff:
                
                l['Source'].remove( s_diff[0] )
                l['Target'].remove( s_diff[0] )
            for source in l['Source']:
                g.appendEdge( source, tuple( l['Command'] ) )
            for target in l['Target']:
                g.appendEdge( tuple( l['Command'] ), target )
        
        g.setBuildTargets( *self.G.getBuildTargets() )
        
        
        return g

