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
from slimpy_base.Core.Interface.Structure import Structure
from slimpy_base.Core.Command.Command import Command
from slimpy_base.Environment.InstanceManager import InstanceManager

_env = InstanceManager()
NI = True
class StructureTester( TestCase ):
    
    def testgenerate_command( self ):
        
        struct = Structure()
        
        _env['slimvars']['keep_tb_info'] = False
        
        c1 = struct.generate_command( 'cmnd', a1=11 )
        
        c2 = Command( 'cmnd',None, a1=11)
        
        self.failUnlessEqual( c1,c2)
        self.failUnlessEqual( c1.tb_info , None )
        
        _env['slimvars']['keep_tb_info'] = True
        
        c1 = struct.generate_command( 'cmnd', a1=11 )
        self.failUnless( isinstance(c1.tb_info, str) )
        

    def testgenerateNewWithSpace( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testAppendToGraph( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testapply_command( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testdependant( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testflush( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test__nonzero__( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testgenerateNew( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testaddBreakPoint( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testsource_or_num( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testtestCommand( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testgenData( self ):
        if NI: raise NotImplementedError("test not implemented")


    def test__repr__( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testgenScalar( self ):
        if NI: raise NotImplementedError("test not implemented")


def suite():
    return defaultTestLoader.loadTestsFromTestCase( StructureTester )

