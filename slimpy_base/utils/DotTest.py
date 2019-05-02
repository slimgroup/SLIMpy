"""
Todo doc
"""

from unittest import TextTestRunner
import sys
import new
import unittest
from numpy import ndarray,all,array

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


class DotTester( object ):
    
    __shared_state = {}
    opers = set()
    
    def __init__( self):
        
        self.__dict__ = self.__shared_state
    
    def clear( self ):
        self.__shared_state = {}
        
    def addLinearOp( self, linop ):
#        print "adding",  linop
#        set_trace()
        test = False
        for oper in self.opers:
            if isinstance(oper, ndarray) ^ isinstance(linop, ndarray):
                continue
            elif isinstance(oper, ndarray) and isinstance(linop, ndarray):
                test = all(oper == linop)
            else:
                test = bool( oper == linop )
                
        if test:
            return
        else:
            self.opers.add( linop )
        

    def buildTestSuite( self ,places=11):
        
        suite = unittest.TestSuite()
        testloader = unittest.TestLoader()
        loadtest = testloader.loadTestsFromTestCase
        
        for oper in self.opers:
            dottest = new.classobj( str( oper ), ( DotTestFixture, ), {'oper':oper,'places':places} )
            test = loadtest( dottest )
            suite.addTest( test )
            
        return suite
    
    def __str__( self ):
        ret =  ""
        msg = "Dottest:\n   +"

        for oper in self.opers:
            ret += "    +"+str( oper ) +'\n'
        
        return msg + ret
            
        
        
class DotTestFixture( unittest.TestCase ):

    def calcNorms( self, tmp1, tmp2 ):
        norm1 = tmp1.norm( 1 )
        norm2 = tmp2.norm( 1 )
        return norm1, norm2

    oper = None
    places = 11
    
    def setUp( self ):
        """

        """
        
        

        
    def tearDown( self ):
        
#        self.domainNoise.remove()
#        self.rangeNoise.remove()
#        
#        self.tmp1.remove()
#        self.tmp2.remove()
        pass
        

    def testLinearOperator( self ):
        """
        
        """
#        import pdb;pdb.set_trace( )
        print "-"*50
        print str( self.oper )
        if self.oper is None:
            raise NotImplementedError( 'The DotTestFixture class must be '
                                      'subclassed and the "oper" field sust be set' )
        
        A = self.oper.copy( )
        
        domain = A.domain()
        range = A.range()
        
        domainNoise = domain.noise()
        
        if domain.isReal() and range.isComplex():
            rangeNoise = A * domain.noise()
        else:
            rangeNoise = range.noise()

        msg = "\n\nInitial data is not in the domain of '%s' \n"
#        set_trace()
        self.assertTrue( domainNoise in A.domain( ) , msg %( A.domain() ) )
        msg = "\n\nInitial transformed data is not in the range of '%s' \n"
        self.assertTrue( rangeNoise in A.range() , msg %( A.range() ) )
        
        trans = A *   domainNoise
#        try:
        inv =   A.H * rangeNoise
#        except:
#            type, val, tb = sys.exc_info()
#            import pdb 
#            print
#            print type, val
#            print "launching post mortem"
#            pdb.post_mortem( tb )
#            raise
            
        
        norm1 = rangeNoise.H * trans
        norm2 = inv.H * domainNoise
        
        ratio = abs( norm1.item()/norm2.item() )
        
        # This is for multiple tests 
        if hasattr(self, 'ratio_list'):
            self.ratio_list.append(ratio)
        
        places = self.places
        
        msg = ("Linear Operator failed the dot test with ratio: "
               "%(ratio)s\n%(norm1)s != %(norm2)s "
               "failed within %(places)s places" %vars())
        
#        if type(norm2) == complex:
#            norm2 = norm2.real
#        if type(norm1) == complex:
#            norm1 = norm1.real
            
        self.assertAlmostEquals( ratio, 1 , places=places, msg=msg )
        print norm1.data, "==", norm2.data
        print "ratio:",ratio
        
    def generateNoisyData( self, space ):
        
        if space.isComplex():
            cspace = space.copy()
            
            cspace['data_type'] = 'float'
            
            cnoise = cspace.zeros().noise()
            rnoise = cspace.zeros().noise()
            
            from slimpy_base.api.functions.functions import cmplx
            
            noise = cmplx( rnoise, cnoise )
            
        else:
            noise = space.zeros().noise()
        #noise.flush()

        return noise
    
def DotTest( oper, percision=7, numtests=1, expected_mean=1 ):
    """
    Dottest a Linear Operator
    
    @details
    s.t. 
    @f$ 
    \langle Ay,x \rangle \approx \langle A^{H}x, y \rangle 
    @f$ 
    within @a percision digits.
    where @a A is in @a opers and x and y are created by 
    @ref slimpy_base.Core.User.Structures.VectorSpace.VectorSpace.noise "A.range.noise( )" 
    and 
    @ref slimpy_base.Core.User.Structures.VectorSpace.VectorSpace.noise "A.domain.noise( )"
    respectivly.
    
    @param opers may be a linear operator or a 
      list of linear operators
    @param percision the preceition to run the test at, determining a pass or a fail.   
    """
    
    suite = unittest.TestSuite()
    testloader = unittest.TestLoader()
    loadtest = testloader.loadTestsFromTestCase
        
    ratio_list = []
    for i in range(numtests): 
        dottest = new.classobj( str( oper ), ( DotTestFixture, ), {'oper':oper,'places':percision,'ratio_list':ratio_list} )
        test = loadtest( dottest )
        suite.addTest( test )
        
    testRunner = TextTestRunner( sys.stdout, 1, 1 )
    testRunner.run( suite )
    
    ratarray = array( ratio_list )
    avrat = sum( ratarray)/ len(ratarray)
    varrat = sum((ratarray-1)**2)
    avvar = (avrat-1)**2
    print "Summary: "
    print "  avg ratio: %(avrat).2e" %vars() 
    print "  avg var  : %(avvar).2e" %vars() 
    print "  varience : %(varrat).2e" %vars() 
    
    
    
    
