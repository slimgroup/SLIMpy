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

from unittest import TestCase,defaultTestLoader

from slimpy_base.Core.Command.CommandPack import CommandPack
from slimpy_base.Core.Command.Command import Command
from slimpy_base.Core.Interface.node import Target
from slimpy_base.Core.Interface.node import Node
from slimpy_base.Core.Interface.node import Source

NI = False

class CommandPackTester( TestCase ):
    
#    def test_init( self ):
#        
#        cp = CommandPack(['comm'], 'in_cont', 'out_cont' )
#        cp.


    def testsetTarget( self ):
        
        cp = CommandPack(['comm'] )
        
        self.failUnlessEqual( cp.target , True )
         
        cp.target = 'tgt'
        self.failUnlessEqual( cp.target , 'tgt' )
        
        cmd = Command( 'tag', None )
        cp = CommandPack([ cmd ] , out_cont=None )
        self.failUnlessRaises( Exception , setattr, cp,'target' , 'tgt' )
        
        cmd = Command( 'tag', None, Target )
        cp = CommandPack([ cmd ] , out_cont=None )
        
        tgt = Target('tgt')
        cp.target = tgt 
        self.failUnlessEqual( cp.target , None )
        self.failUnlessEqual( cmd.getTargets() , [tgt] )
        

    def testgetNodeList( self ):
        
        cmd = Command( 'tag', None )
        
        node = Node(cmd )
        
        cp = CommandPack([ cmd ]  )
        
        nlist = cp.getNodeList( )
        
        self.failUnlessEqual(nlist, [node])

    def testsetSource( self ):
        
        cp = CommandPack(['comm'] )
        
        self.failUnlessEqual( cp.source , True )
         
        cp.source = 'tgt'
        self.failUnlessEqual( cp.source , 'tgt' )
        
        cmd = Command( 'tag', None )
        cp = CommandPack([ cmd ] , in_cont=None )
        self.failUnlessRaises( Exception , setattr, cp,'source' , 'src' )
        
        cmd = Command( 'tag', None, Source )
        cp = CommandPack([ cmd ] , in_cont=None )
        
        src = Source('tgt')
        cp.source = src 
        self.failUnlessEqual( cp.source , None )
        self.failUnlessEqual( cmd.getSources() , [src] )
        


    def testgetTargets( self ):
        
        t1 = Target('t1')
        t2 = Target('t2')
        cmd = Command( 'tag', None,  t1 )
        cmd2 = Command( 'tag', None,  t2=t2 )
        
        cp = CommandPack([ cmd,cmd2 ] )
        
        tset = set( cp.getTargets() )
        
        self.failUnlessEqual( tset , set([t1,t2]) )


    def testgetSources( self ):
        
        s1 = Source('t1')
        s2 = Source('t2')
        cmd = Command( 'tag', None,  s1 )
        cmd2 = Command( 'tag', None,  s2=s2 )
        
        cp = CommandPack([ cmd,cmd2 ] )
        
        tset = set( cp.getSources() )
        
        self.failUnlessEqual( tset , set([s1,s2]) )



def suite():
    return defaultTestLoader.loadTestsFromTestCase( CommandPackTester )
