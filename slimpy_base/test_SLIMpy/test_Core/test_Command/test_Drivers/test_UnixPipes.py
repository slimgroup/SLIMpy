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
from slimpy_base.Core.Command.Drivers.Unix_Pipes import Unix_Pipes

from slimpy_base.Environment.InstanceManager import InstanceManager


class Unix_PipesTester( TestCase ):


    def testprepend_datapath(self):
        env = InstanceManager()

        local_dp  = 'local_dp'
        tmp_global_dp = 'tmp_global_dp'
        global_dp = 'global_dp'
        env['slimvars']['localtmpdir']  = local_dp
        env['slimvars']['globaltmpdir'] = tmp_global_dp
        env['slimvars']['datapath']  = global_dp
        
        itr = [ [(None,None), None],
                [(False,None), None],
                [(True,None), None],
                
                [(None,True), None],
                [(True,True), local_dp],
                [(False,True), tmp_global_dp],

                [(None,False), global_dp ],
                [(True,False), global_dp],
                [(False,False), global_dp],
                
              ]
        for (is_loc, is_tmp), ans in itr:
            
            res = Unix_Pipes.prepend_datapath( is_loc, is_tmp, 'com' )
            if ans is None:
                self.assertFalse( "DATAPATH" in res , "expected no datapath" )
            else:
                self.assertTrue( ans in res , "expected %(ans) got %(res)s" )
        
#    def testsub( self ):
#        'sub should'
#        Unix_Pipes.sub(targ)
##        raise NotImplementedError("test not implemented")
#
#
#    def testpipe_join( self ):
#        raise NotImplementedError("test not implemented")
#
#
    def teststdout_join( self ):
        res = Unix_Pipes.stdout_join('cmd', 'foo' )
        ans = "cmd 1> foo"
        self.assertEqual( res, ans )



    def testCreateComand( self ):
        
        # (cmdlist, node_name, source, target,err ), ans
        items = [
        ( ( (['cmdlist'],), { 'node_name':'localhost', 
                          'source':'source', 'target':'target','err':'err'} ), 
            '< source cmdlist > target 2> err',),

        ( ( (['c1 r="p"','c2'],), { 'node_name':'foo', 
                          'source':'source', 'target':'target','err':None} ), 
            'ssh foo "< source c1 r=\\"p\\" | c2 > target"',),

        ( ( (['c1'],), { 'source':'source',} ), 
            '< source c1',),
            
              ] 
        
        for (pars,kw),ans in items:
            res = Unix_Pipes.CreateComand( *pars, **kw)
            self.assertEquals( res, ans )
        
        
#        raise NotImplementedError("test not implemented")


#    def testJOIN_PIPE( self ):
#        
#        Unix_Pipes.JOIN_PIPE()
#        raise NotImplementedError("test not implemented")


    def teststdin_join( self ):
        res = Unix_Pipes.stdin_join('foo', "cmd")
        ans = "< foo cmd"
        self.assertEqual( res, ans )


    def teststderr_join( self ):
        res = Unix_Pipes.stderr_join('cmd', 'foo' )
        ans = "cmd 2> foo"
        self.assertEqual( res, ans )




    def testreplace_quotes( self ):
        init = '"foo"'
        i2 = '\\"foo\\"'
        i3 = '\\\\\\"foo\\\\\\"'
        
        res = init
        for ans in [init,i2,i3]:
            self.assertEquals( res, ans )
            res = Unix_Pipes.replace_quotes(res)
        


def suite():
    return defaultTestLoader.loadTestsFromTestCase( Unix_PipesTester )

