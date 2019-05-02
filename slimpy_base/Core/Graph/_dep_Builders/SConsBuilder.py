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
set of tools to output SCons script
"""

from slimpy_base.Core.Graph.Builders.SLIMBuilder import SLIMBuilder
        

class SconsFlow( object ):
    
    def __init__( self, globals ):
        
        self.glob = globals

        self.flags = dict( stdin=0, stdout=-1 )
        
        self.targets = set( [] )
        
        self.insource = None
        
        self.outtarget = None
        
        self.sources = set( [] )
        
    def setStdinSrc( self, src ):
            
        if src:
            
            self.insource = str( src )
            
            self.flags.pop( 'stdin', None )
            
            self.sources.discard( src )
        
    def setStdoutTgt( self, tgt ):
        
        if tgt:
        
            self.outtarget = str( tgt )
            
            self.flags.pop( 'stdout', None )
            
            self.targets.discard( tgt )
        
    def setTargets( self, Targets ):
    
        self.targets.update( Targets )
        self.targets.discard( self.outtarget )
        
    def setSources( self, sources ):
        
        self.sources.update( sources )
        
        self.sources.discard( self.insource )
        
    def setCommands( self, commlist ):
        
        self.commands = commlist
        
    def __str__( self ):
        tgts = self.prosessOut()
        srcs = self.prosessIn()
        command = self.prosessCommand()
        flags = self.prosessFlags()

        return "Flow( %(tgts)s , %(srcs)s , %(command)s %(flags)s )\n" %vars()

    def prosessCommand( self ):
        
        command =  " |\n\t".join( [ com.function.format( com.params, com.kparams ) for com in self.commands] )
        command = "\n\t\"\"\"\n\t%(command)s\n\t\"\"\"" %vars()
        
        for i , src in enumerate( self.sources ):

            if  self.insource:
                i += 1
            command = command.replace( src, '${SOURCES[%s]}'%i )

        for i , tgt in enumerate( self.targets ):
                                 
            if  self.outtarget:
                i += 1
            command = command.replace( tgt, '${TARGETS[%s]}'%i )
        return command

    def prosessFlags( self ):
        
        l = lambda k : "%s=%s" %k
        
        flags = self.flags.items()
        
        if flags:
            return ","+" , ".join( map( l, flags ) )
        else:
            return ""
        
    def prosessIn( self ):
        if self.insource:
            items = [self.insource] + list( self.sources )
            
            itm = "[ '" + "' , '".join( map( str, items ) ) + "' ]"

        elif self.sources:
            itm = "[ '" + "' , '".join( map( str, self.sources ) ) + "' ]"
        else:
            itm = 'None'
                        
        return itm

    def prosessOut( self ):
        
        if self.outtarget:
            items = [self.outtarget] + list( self.targets )
            
            itm = "[ '" + "' , '".join( map( str, items ) ) + "' ]"

        elif self.targets:
            itm = "[ '" + "' , '".join( map( str, self.targets ) ) + "' ]"
        else:
            itm = 'None'
                        
        return itm

class SConsBuilder( SLIMBuilder ):

    
    def __init__( self, g, sources, *targets ):
        
#        self.builder = PipeBuilder(g)
        
        self.lst = []
         
        for l in self.builder.lst:
            
            sf =  SconsFlow( {} )
            
            com = add( [ self.table[node] for node in l['Command'] ] )
            
            sf.setStdoutTgt( com.function.getTarget() )
            
            sf.setStdinSrc( com.function.getTarget() )
            
            sf.setCommands( com.function.getCmnd() )
            
            sf.setSources( set( [str( self.table[node] ) for node in l['Source'] ] ) )
            
            sf.setTargets( set( [str( self.table[node] ) for node in l['Target'] ] ) )
            
            self.lst.append( sf )
            
    def printSCons( self ):
        
        sconstruct = "from rsfproj import *\n\ndef make(  ):\n\n\t"
        
        import os 
        
        rsfroot = os.path.join( os.environ['RSFROOT'] , 'bin', 'sf' )
        
        curdir = os.path.abspath( os.curdir )
        
        for l in self.lst:


            f = str( l )
            
            f = f.replace( '\n', '\n\t' )
            f = f.replace( rsfroot , '' )
            f = f.replace( curdir +'/', '' )

            sconstruct += f
            
        return sconstruct 
    
    
def add( commands ):
    """
    add list of commands together using '+'
    """
    prev = commands.pop( 0 )
    while commands:
        next = commands.pop( 0 )
        prev = prev + next
        
    return prev
