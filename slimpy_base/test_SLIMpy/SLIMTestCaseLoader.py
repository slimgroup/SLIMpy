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


from unittest import TextTestRunner,_TextTestResult
import time
 
class SLIMTextTestRunner( TextTestRunner ):
    
    def _makeResult(self):
        return SLIMResult(self.stream, self.descriptions, self.verbosity)
    
    def run(self,test):
        "Run the given test case or test suite."
        result = self._makeResult()
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        nid = len(result.unimplemented)
        
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run - nid, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            self.stream.write("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.write(")")
        else:
            self.stream.write("OK")
        
        if nid:
            perc = 100. * nid/result.testsRun
            tests_run = result.testsRun - nid
            self.stream.writeln( "      ( 'not implemented'=%d , %.1f%% of TestSuite not run )" %(nid,perc) )
#            self.stream.write( "" %tests_run )
        else:
            self.stream.writeln( "" )
        

        return result

class SLIMResult( _TextTestResult ):
    
    def __init__(self,stream, descriptions, verbosity):
        _TextTestResult.__init__(self,stream, descriptions, verbosity)
        self.unimplemented = []
    
    def _get_num_ran(self):
        return self._testsRun
    def _set_numran(self, val):
        return self._testsRun
    
    def addUnimplementedTest(self, test):
        self.unimplemented.append(test)
        if self.showAll:
            self.stream.writeln("Not Implemented")
        elif self.dots:
            self.stream.write('N')

    
    def addError(self, test, err):
        err_inst = err[1]
        if isinstance(err_inst, NotImplementedError):
            self.addUnimplementedTest( test )
        else:
            _TextTestResult.addError(self, test, err)

if __name__ == '__main__':
        
    from unittest import TestCase,TestLoader,defaultTestLoader
    class Foo(TestCase):
        def test_t(self):
            raise NotImplementedError
        def test_r(self):
            pass
        
    
    suite = defaultTestLoader.loadTestsFromTestCase(Foo)
    
    tr = SLIMTextTestRunner()
    
    tr.run(suite)
