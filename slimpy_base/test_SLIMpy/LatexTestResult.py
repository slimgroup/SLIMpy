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

from os.path import split,splitext
from SLIMTestCaseLoader import SLIMResult,SLIMTextTestRunner
from unittest import TestResult 
from unittest import TestCase
from unittest import TextTestRunner
from string import Template
from pdb import set_trace
import traceback
import time
import re
import sys

class LatexTestResult(TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream ):
        TestResult.__init__(self)
        self.stream = stream
        self.unimplemented = []
        
        
        self.stream.writeln( "\\begin{tableiii}{l|l|l}{exception}{Test Method}{Test Case}{Result}" )
        
    def end(self):
        self.stream.writeln( "\\end{tableiii} ")
        
    def get_testMethodName(self,test):
        if hasattr( test, '_testMethodName'): # python2.5
            methname = getattr( test, '_testMethodName' ) 
        elif hasattr( test, '_TestCase__testMethodName' ): # python2.4
            methname = getattr( test, '_TestCase__testMethodName' )
        return methname

    def getDescription(self, test):
        method_name = self.get_testMethodName(test)
        module = type(test).__module__
        doc = getattr(type(test), method_name ).__doc__ or "No Doc for %(method_name)s" %vars() 
        doc = self.make_latex_safe(doc)
        return method_name,module,doc
#        descr = test.shortDescription() or str(test)
#        return self.make_latex_safe(descr)
    
    def startTest(self, test):
        TestResult.startTest(self, test)
#        set_trace()
        methname = self.get_testMethodName(test)
#        if hasattr( test, '_testMethodName'): # python2.5
#            methname = getattr( test, '_testMethodName' ) 
#        elif hasattr( test, '_TestCase__testMethodName' ): # python2.4
#            methname = getattr( test, '_TestCase__testMethodName' )
        methname = self.make_latex_safe( methname)
        
        case_file = sys.modules[type(test).__module__].__file__
        base,ext = splitext(case_file)
        case_file = "".join( [base, ext.replace('.pyc', '.py')] )
        
        
        case_name = self.make_latex_safe(type(test).__name__)
        
        self.stream.write("    \\lineiii{%(methname)s} {\\citetitle[%(case_file)s]{%(case_name)s}}" %vars() )
#            self.stream.write(" ... ")

    @classmethod
    def make_latex_safe(self,strn):
        strn = strn.replace('_' , '{\_}')
        return strn
    
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        self.stream.writeln( "{ok}" )

    def _addError(self, test, err):
        TestResult.addError(self, test, err)
        self.stream.writeln( "{ERROR}" )
        
    def addError(self, test, err):
        err_inst = err[1]
        if isinstance(err_inst, NotImplementedError):
            self.addUnimplementedTest( test )
        else:
            self._addError( test, err)

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        self.stream.writeln("{FAIL}")
        
    def addUnimplementedTest(self, test):
        self.unimplemented.append(test)
        self.stream.writeln("{Not Implemented}")
            
    def printErrors(self):
        
        if self.errors:
            self.stream.writeln()
            
            self.stream.writeln( "\\section{Errors}" )
            
            self.printErrorList('ERROR', self.errors)

            self.stream.writeln()
        if self.failures:
            self.stream.writeln( "\\section{Failures}" )

            self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        writeln = self.stream.writeln 
        
        for test, err in errors:
            writeln()
            mehtod_name,module,doc = self.getDescription(test)
            writeln("%(flavour)s: \\function{%(mehtod_name)s} in (\\method{%(module)s}) " %vars() )
#            ferr = self.latex_format_err(err)
            writeln( "\\begin{notice} [warning]" )
            writeln( "%s" % err )
            writeln("\\end{notice}")
#            print err
            writeln()

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next
        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            ftb = traceback.format_exception(exctype, value, tb, length)
        else:
            ftb = traceback.format_exception(exctype, value, tb)
            
        return self.latex_format_err(ftb)
    
    def latex_format_err(self,ftb):
        lines = []
        push = lines.append
        
        com = re.compile("File (.*), line (\d*), in (.*)" )
        push("\\textbf{%s}\n" %ftb[0].strip('\n '))
        push("\\begin{itemize}\n")
         
        for line in ftb[1:-1]:
            info,line = line.strip('\n ').split( '\n' )
            fname,lineno,method = [item.strip('"\n ') for item in com.findall(info)[0]]
            
#            ctitle = "\\citetitle[%(fname)s]{%(shrt)s}" %vars()
            push("\\item[File \\url{%(fname)s}, line %(lineno)s, in \\method{%(method)s}]\n" %vars() )
            push("\n\n " %vars() )
            push("\\code{%(line)s}\n" %vars() )
        
#        set_trace()
        push("\\end{itemize}\n")
        
        err_msg = [ item.strip("\n ") for item in ftb[-1].split(':', 1) ]
        
        if len(err_msg) == 2:
            err,msg = err_msg
            push('\\textbf{%(err)s:} "%(msg)s"\n' %vars())
        elif len(err_msg) == 1:
            err = err_msg
            push('\\textbf{%(err)s}\n' %vars())
        else:
            push('\\textbf{Exception Unknown}\n' %vars())
            
        return " ".join(lines)


class LatexTextTestRunner( TextTestRunner ):
    
    def _makeResult(self):
        return LatexTestResult(self.stream)
    
    def run(self,test):
        write = self.stream.write
        writeln = self.stream.writeln
        "Run the given test case or test suite."
        self.stream.writeln("\\section{Tests}")
        result = self._makeResult()
        startTime = time.time()
        test(result)
        result.end()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        
        
        result.printErrors()        

        run = result.testsRun
        nid = len(result.unimplemented)
        self.stream.writeln("\\section{Summary}")
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run - nid, run != 1 and "s" or "", timeTaken))
        
        self.stream.writeln('\n')
        
        if not result.wasSuccessful():
            writeln("\\begin{notice} [warning]")
            write("\\emph{FAILED} (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.write(")")
            writeln("\\end{notice}\n\n")
        else:
            self.stream.write("\\emph{OK}")
        
        if nid:
            tests_run = result.testsRun - nid
            perc = 100. * tests_run/result.testsRun
            writeln("\\begin{notice} [note]")
            writeln( "only %(perc).1f{\%%} of Test Suite was run, %(nid)d tests not implemented" %vars() )
            writeln("\\end{notice}\n\n")
#            self.stream.write( "" %tests_run )
        else:
            self.stream.writeln( "\n" )
        

        return result

