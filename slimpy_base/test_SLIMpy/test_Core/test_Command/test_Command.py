"""
"""
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.Core.User.Structures.Scalar import Scalar
import unittest
from slimpy_base.Core.Command.Command import Command
from slimpy_base.Core.Interface.node import Source , Target


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
test case for Command class
"""


env = InstanceManager()

NI = False

def testFunc( *p, **k ):
    """
    returns arguments given
    """
    return p, k

class CommandTest( unittest.TestCase ):
    """
    Test Command Class
    """
    def setUp( self ):
        """
        create commands
        """
        self.sourceOf1 = Source( 1 )
        self.sourceOfBob = Source( 'bob' )
        
        self.targetOf2 = Target( 2 )
        self.targetOfFoo = Target( 'foo' )
        
        self.c1 = Command( 'testFunc', '__adder', 1, a=2 )
        self.c2 = Command( 'testFunc', '__adder', 3, b=Source )
        self.c3 = Command( 'testFunc', '__adder', self.sourceOf1, self.sourceOfBob )
        self.c4 = Command( 'testFunc', '__adder', self.targetOfFoo, self.targetOf2 )
        
#        for cmd in [self.c1,self.c2,self.c3,self.c4]:
        self.c1.func = testFunc
        
    
    def tearDown( self ):
        """
        clears the Hashtable singleton class 
        """
        env['table'].clear()

        
    def testCopy( self ):
        """
        test that the copy method works
        """
        c3 = self.c1.copy()
        
        self.assertEqual( c3, self.c1, "%s != %s" %(c3,self.c1) )
        
        self.assertNotEqual( id( c3 ), id( self.c1 ) )

    
    def testRun( self ):
        """
        test the run method
        """
        ran = self.c1.run()

        self.assertEqual( ran , ( ( 1, ), {'a':2} ) )

        ran = self.c1.run()
        #test that the same function works twice
        self.assertEqual( ran , ( ( 1, ), {'a':2} ) )
        
        # if the function is not set then the command can not run
        self.assertRaises( Exception, self.c2.run )
    
    def testGetSources( self ):
        """
        test that the getSources method returns all of 
        the Source class instances contained within
        the Command 
        """
        sources = self.c3.getSources()
        
        self.assertEqual( len( sources ) , 2 , "returned more sources than are in the command" )
        
        self.assertTrue( self.sourceOf1 in sources , "missing source of 1" )
        
        self.assertTrue( self.sourceOfBob in sources , "missing source of bob" )
        
        noSources = self.c1.getSources()
        
        self.assertEqual( len( noSources ) , 0 , "returned more sources than are in the command" )
        
    def testGetTargets( self ):
        """
        test that the getTargets method returns all of 
        the Target class instances contained within
        the Command 
        """
        targets = self.c4.getTargets()
        
        self.assertEqual( len( targets ) , 2 , "returned more targets than are in the command" )
        
        self.assertTrue( self.targetOf2 in targets , "missing target of 1" )
        
        self.assertTrue( self.targetOfFoo in targets , "missing target of bob" )
        
        noTargets = self.c1.getTargets()
        
        self.assertEqual( len( noTargets ) , 0 , "returned more targets than are in the command" )
        
        

    def test_params( self ):
        """
        test the Command.params manipulation functions
        """
        
        c1 =self.c1.copy( )
         
        c1.del_par( 0 )
        
        self.failUnlessEqual( c1.params, [] )
        
        self.failUnlessRaises(IndexError, c1.del_par, 0 )
        self.failUnlessRaises(IndexError, c1.del_par, 99 )
        
        c2 = self.c2.copy( )

         
        par = c2.pop_par( 0 )
        
        self.failUnlessEqual( par, 3 )
        self.failUnlessEqual( c1.params, [] )
        
        self.failUnlessRaises(IndexError, c1.del_par, 0 )
        self.failUnlessRaises(IndexError, c1.del_par, 99 )

#        if NI: raise NotImplementedError("test not implemented")


    def test_adder( self ):
        
        if NI: raise NotImplementedError("test not implemented")


    def testhas_unusedtarget( self ):
        
        cmd = Command( 'foo', None, Target )
        
        self.failUnless( cmd.has_unusedtarget() )
        
        cmd = Command( 'foo', None, t=Target )
        
        self.failUnless( cmd.has_unusedtarget() )
        
        cmd = Command( 'foo', None )
        cmd.add_other_dep(Target)
        self.failUnless( cmd.has_unusedtarget() )
        
        self.failIf( self.c1.has_unusedtarget( ) )
        

    def testsetunusedtarget( self ):
        
        foo_tgt = Target( 'foo' )
        
        cmd = Command( 'foo', None, Target )
        
        cmd.setunusedtarget( foo_tgt )
        
        targets = cmd.getTargets( )
        
        self.failUnlessEqual(targets, [foo_tgt] )
        
        self.failUnlessRaises(Exception, cmd.setunusedtarget, foo_tgt )

        cmd = Command( 'foo', None, Source )
        
        self.failUnlessRaises(Exception, cmd.setunusedtarget, foo_tgt )
        
        cmd.add_other_dep( foo_tgt )
        self.failUnlessEqual(targets, [foo_tgt] )
        
    def testgetTargets( self ):
        
        foo_tgt = Target( 'foo' )
        bar_tgt = Target( 'bar' )
        spam_tgt = Target( 'spam' )
        spam_src = Source( 'eggs' )
        
        c1 = Command('foo', None ,  foo_tgt, x=bar_tgt, ssc=spam_src )
        c1.add_other_dep(spam_tgt)
        
        targets = c1.getTargets()
        
        self.failUnless( foo_tgt in targets )
        self.failUnless( bar_tgt in targets )
        self.failUnless( spam_tgt in targets )
        
        self.failIf( spam_src in targets )

        c1 = Command('foo', None )
        targets = c1.getTargets()
        self.failUnlessEqual( targets , [] )

        

    def test_set_func( self ):
        
        c1 = Command( 'foo', 'my_adder', 'Target' ,t='t' )
        
        self.failIf( c1.is_set() )
        
        c1.func = lambda x:x
        self.failUnless( c1.is_set() )


    def test_init( self ):
        
        c1 = Command( 'foo', 'my_adder', 'Target' ,t='t' )
        
        self.failUnlessEqual(c1.tag, 'foo')
        
        self.failIf( c1.is_set( ) )
        
        self.failUnlessEqual(c1.adder,'my_adder', 'foo')
        
        self.failUnlessEqual(c1.params,['Target'], 'foo')
        
        self.failUnlessEqual(c1.kparams,{'t':'t'}, 'foo')


    def test_format_params( self ):
        
        c1 = Command('foo', None, 'a','b',c='c' )
        
        form = c1._format_params( )
        
        ans = "( a, b, c=c )"
        self.failUnlessEqual(form, ans)

    def test_kw_params( self ):
        
        c1 = Command('foo', None, 'a','b',c='c' )
        
        # test has_key
        self.failUnless( c1.has_key('c') )
        self.failIf( c1.has_key('d') )
        
        self.failUnlessEqual( c1['c'] ,'c' )
        
        c1['c'] = 'd'
        
        self.failUnlessEqual( c1['c'] ,'d' )
        
        c1.del_kw('c')
        
        self.failIf( c1.has_key('c') )
        
        

    def test_get_target_cont( self ):
        
        foo_tgt = Target( 'foo' )
        bar_tgt = Target( 'bar' )
        spam_src = Source( 'spam' )
        
        c1 = Command('foo', None ,  foo_tgt, x=bar_tgt, src=spam_src )
        
        
        tc = c1.target_containers
        
        self.failUnlessEqual(len(tc), 2 )
        
        self.failUnless( 'foo' in tc)
        self.failUnless( 'bar' in tc)
        
        self.failIf( 'spam' in tc)

    def testcopy( self ):

        foo_tgt = Target( 'foo' )
        bar_tgt = Target( 'bar' )
        spam_src = Source( 'spam' )

        c1 = Command('foo', None ,  foo_tgt, x=bar_tgt, src=spam_src )
        
        c2 = c1.copy()
        
        self.failUnlessEqual(c1, c2 )
        
        self.failIfEqual(id(c1), id(c2) )
        
        func = lambda x:x
        
        c2.func = func
        
        self.failIfEqual( c1, c2 )
        
        c1.func = func

        self.failUnlessEqual(c1, c2 )

    def test_rplace_scalar_str( self ):
        
        scal = Scalar(  )
        
        ss = scal.data
        scal.set( 3 )
        c1 = Command('foo', None )
        
        snew = c1._rplace_scalar_str( ss )
        
        self.failUnlessEqual(snew, '3', )
        

    def testgetSources( self ):
        
        foo_src = Source( 'foo' )
        bar_src = Source( 'bar' )
        spam_src = Source( 'spam' )
        spam_tgt = Target( 'eggs' )
        
        c1 = Command('foo', None ,  foo_src, x=bar_src, ssc=spam_tgt )
        c1.add_other_dep(spam_src)
        
        sources = c1.getSources()
        
        self.failUnless( foo_src in sources )
        self.failUnless( bar_src in sources )
        self.failUnless( spam_src in sources )
#        print sources
        self.failIf( spam_tgt in sources )

        c1 = Command('foo', None )
        targets = c1.getSources()
        self.failUnlessEqual( targets , [] )


    def testget_structure( self ):
        
        if NI: raise NotImplementedError("test not implemented")


    def test_get_source_cont( self ):
        
        foo_src = Source( 'foo' )
        bar_src = Source( 'bar' )
        spam_tgt = Target( 'spam' )
        
        c1 = Command('foo', None ,  foo_src, x=bar_src, src=spam_tgt )
        
        
        sc = c1.source_containers
        
        self.failUnlessEqual(len(sc), 2 )
        
        self.failUnless( 'foo' in sc)
        self.failUnless( 'bar' in sc)
        
        self.failIf( 'spam' in sc)


    def testhas_unusedsource( self ):
        
        cmd = Command( 'foo', None, Source )
        
        self.failUnless( cmd.has_unusedsource() )
        
        cmd = Command( 'foo', None, t=Source )
        
        self.failUnless( cmd.has_unusedsource() )
        
        cmd = Command( 'foo', None )
        cmd.add_other_dep(Source)
        self.failUnless( cmd.has_unusedsource() )
        
        self.failIf( self.c1.has_unusedsource( ) )

    def testsetunusedsource( self ):
        
        foo_src = Source( 'foo' )
        
        cmd = Command( 'foo', None, Source )
        
        cmd.setunusedsource( foo_src )
        
        sources = cmd.getSources()
        
        self.failUnlessEqual(sources, [foo_src] )
        
        self.failUnlessRaises(Exception, cmd.setunusedsource, foo_src )

        cmd = Command( 'foo', None, Target )
        
        self.failUnlessRaises(Exception, cmd.setunusedsource, foo_src )
        
        cmd.add_other_dep( foo_src )
        self.failUnlessEqual(sources, [foo_src] )
        

    def testget_all_values( self ):
        
        c1 = Command('tag', 'adder', 1,2, a=3, b=4 )
        c1.add_other_dep( 5 )
        
        all_vals = c1.all_values
        set_all = set( all_vals)
        
        self.failUnlessEqual( set_all, set(range(1,6)) )
        
            


def CommandTestSuite():
    """
    returns a testsuite intstance
    """
    tcm = unittest.TestLoader().loadTestsFromTestCase( CommandTest )
    return tcm

def suite():
    """
    returns a testsuite intstance
    """
    return CommandTestSuite()
    
    
    
