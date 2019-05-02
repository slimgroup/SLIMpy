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
from slimpy_base.Core.Command.Command import Command
from slimpy_base.Core.Command.Converter import MapFunctions as mf

NI = False

class MapFunctionsTester( TestCase ):

    def testtruefalseHelper( self ):
        
        command = Command( 'tag', None, this=True, that=False )
        
        command = mf.truefalseHelper( command, true='tt', false='ff' )
#        command, true='y', false='n'
        
        self.failUnlessEqual( command['this'],'tt')
        self.failUnlessEqual( command['that'],'ff')

    def testkeep( self ):
        
        command = Command( 'tag', None, this=True, that=False )
        
        command = mf.keep(command, ['this','foo'] )

        self.failIf( command.has_key('that') )
        
        self.failUnless( command.has_key('this') )

    def testsplit( self ):
        
        command = Command( 'tag', None, this=True, that=False )
        
        c1,c2 = mf.split(command)
        
        self.failUnlessEqual( c1, c2 )
        self.failIfEqual( id(c1), id(c2) )


    def testdiscard( self ):
        command = Command( 'tag', None, this=True, that=False )
        
        cmd = mf.discard(command, ['that'] )
        
        self.failUnless( cmd.has_key('this') )
        self.failIf( cmd.has_key('that') )
        
        
    def testkeywordmap( self ):
        
        command = Command( 'tag', None, this=True, that='False' )
        
        cmd = mf.keywordmap(command, {'that':'spam'} )
        
        self.failUnless( cmd.has_key('spam') )
        self.failUnlessEqual(cmd['spam'],  'False' )
        self.failIf( cmd.has_key('that') )


    def testpack( self ):
        
        raise NotImplementedError('not implemented')


def suite():
    return defaultTestLoader.loadTestsFromTestCase( MapFunctionsTester )

