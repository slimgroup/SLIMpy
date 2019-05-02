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
Test Log class
"""


#from slimpy_base.utils.Logger import Log
from os import remove
from os.path import isfile
import unittest


class TestLog(unittest.TestCase):
    """
    Test the loging class for SLIMpy
    """
    
    def setUp(self):
        """
        create log instances
        """
        self.log1 = Log()
        self.log2 = Log()
        self.filename     = "logtest_tempfile1"
        self.nullfilename = "logtest_tempfile2"
        
    def tearDown(self):
        """
        removes temproary log files
        """
        del self.log1
        del self.log2
        
        self.rmfiles()
    
    def rmfiles(self):
        """
        removes temproary log files
        """
        if isfile(self.filename):
            remove(self.filename)
        if isfile(self.nullfilename):
            remove(self.nullfilename)
            
    def test_init(self):
        """
        test that the log is a singleton instance
        and the defaults are set properly
        """
        self.assertEqual( self.log1.verbose, self.log2.verbose )
        self.log1.setVerbose(3)
        self.assertEquals( self.log1.verbose, 3 )
        self.assertEqual( self.log1.verbose, self.log2.verbose )
    
    def test_linit(self):
        """
        init is for internal use only. use setter funtions to promote
        consistancy.
        """
        file1 = open(self.filename,"w")
        file2 = open(self.nullfilename,"w")
        
        self.log1.init( file1, file2, 12 )
        
        self.assertEquals( self.log1.verbose, 12 )
        self.assertEquals( self.log2.verbose, 12 )

        self.assertEquals( self.log1.logFile, file1)
        self.assertEquals( self.log2.logFile, file1)
        
        self.assertEquals( self.log1.nullOut, file2)
        self.assertEquals( self.log2.nullOut, file2)
    
        
    def test_nullout(self):
        """
        test that output can be written to null out
        """
        l1 = self.log1
        try:
            print >> l1(22), "null null null"
            
        except Exception, exptn:
            assert(False,"Trouble printinig to null out")


#    def test_write(self):
#        """
#        write to file
#        """
#        msg1 = "this is msg1"
#        msg2 = "this is msg2"
#        
#        l1 = self.log1
#        
#        l1.init(self.filename, self.nullfilename, 1)
#        
#        print >> l1(1), msg1,
#        print >> l1(22), msg2,
#        
#        l1.logFile.flush()
#        l1.nullOut.flush()
#        
#        f1 = open(self.filename,"r").read()
#        f2 = open(self.nullfilename,"r").read()
#        
#        self.assertEqual(f1.strip(),msg1,"did not print properly to file\n"
#                                 "%(f1)s != %(msg1)s" %vars() )
#        
#        self.assertEquals(f2,msg2,"did not print properly to null out\n"
#                                  "%(f2)s != %(msg2)s" %vars() )
#        
#        self.rmfiles()
        
#    def test_abridge(self):
#        """
#
#        """
#
#        slimvars.updateAbridgeMap({ "this":"that"})
#        msg1 = "this is this msg"
#        msg2 = "that is that msg"
#        
#        l1 = self.log1
#        l1.setLogFile(self.filename)
#        print >> l1(1), msg1,
#        l1.logFile.flush()
#        
#        f1 = open(self.filename,"r").read()
#        
#        self.assertEqual(f1,msg2)
#        
#        slimvars['abridgeMap'] = {}
#        self.rmfiles()

        
        
        
        
def suite():
    """
    return Log TestSuite
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestLog)

