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


from unittest import TestCase, defaultTestLoader
from slimpy_base.Core.Interface.PSpace import PSpace
from slimpy_base.Core.Interface.PSpace import UnknownValue


NI = True 
class PSpaceTester( TestCase ):

    def testis_sub_superspace( self ):
        
        sub = PSpace( 'adc' , a=1, b=2 )
        supr = PSpace( 'adc' , a=1 )
        
        self.failUnless( supr.is_superspace( sub ) )
        self.failUnless( sub.is_subspace( supr ) )

        self.failIf( sub.is_superspace( supr ) )
        self.failIf( supr.is_subspace( sub ) )
        
        self.failUnless( sub in supr )
        self.failIf( supr in sub )
        
#        sub = PSpace( 'adc' , a=1, b=2, c=UnknownValue )
#        self.failUnless( supr.is_superspace( sub, accept_unknown=False ) )
        
#        supr.is_subspace
        
    def testmakeContaner( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testpop( self ):
        
        space = PSpace( 'adc' , a=1 )
        
        a = space.pop('a')
        self.failUnlessEqual(a , 1 )
        
        self.failUnlessRaises(KeyError, space.pop , 'b' )
        
        if NI: raise NotImplementedError("test not implemented")


    def testhas_key( self ):
        
        space = PSpace( 'adc' , data_type='complex' )
        
        self.failUnless( space.has_key( 'data_type' ) )
        self.failIf( space.has_key( 'does not have this key' ) )

    def testhas_unknown( self ):
        
        space = PSpace( 'adc' , n1=UnknownValue )
        space2 = PSpace( 'adc' , n1=22 )
        
        self.failUnless( space.has_unknown() )
        self.failIf( space2.has_unknown() )
        

    def test_get_params( self ):
        
        space = PSpace( 'adc' , n1=UnknownValue, n2=33 )
        
        restrictions = space._get_params(keep_unknown=False )
        self.failUnlessEqual( restrictions, dict(n2=33) )

        restrictions = space._get_params(keep_unknown=True )
        self.failUnlessEqual( restrictions, dict(n2=33, n1=UnknownValue ) )
        
        


    def test_space_helper( self ):
        
        s1 = PSpace( 'adc' , n1=UnknownValue, n2=33, n3=33 )
        s2 = PSpace( 'adc' , n1=11, n2=22 , d1=0 )
        
        self.failUnlessRaises( Exception,  s1._space_helper, s2 , error=True )
        
        inter_space, dspace_s1, dspace_s2 = s1._space_helper( s2 , error=False )
        
        self.failUnlessEqual( inter_space.params, dict(n1=11) )
        self.failUnlessEqual( dspace_s1.params, dict(n3=33) ) 
        self.failUnlessEqual( dspace_s2.params, dict(d1=0) )

        s1 = PSpace( 'adc' , n1=11, n2=22, n3=33 )
        s2 = PSpace( 'adc' , n1=11, n2=22 , d1=0 )
        
        
        inter_space, dspace_s1, dspace_s2 = s1._space_helper( s2 , error=False )
        
        self.failUnlessEqual( inter_space.params, dict(n1=11,n2=22) )
        self.failUnlessEqual( dspace_s1.params, dict(n3=33) ) 
        self.failUnlessEqual( dspace_s2.params, dict(d1=0) )

    def test__init__( self ):
        
        
        if NI: raise NotImplementedError("test not implemented")


    def test_shape( self ):
        'test shape getters and setters'
        
        space = PSpace('adc', n1=10, n2=10 )
        
        self.failUnlessEqual(space.shape, [10,10])

        space = PSpace('adc', n1=10, n2=10 ,n3=1)
        
        self.failUnlessEqual(space.shape, [10,10])
        
        self.failUnlessEqual( space.size, 100 )
        self.failUnlessEqual( len(space), 100 )
        
        space.shape = [20,20]
        
        self.failUnlessEqual( space.shape , [20,20] )
        
        self.failUnlessEqual( space['n1'] , 20 )
        self.failUnlessEqual( space['n2'] , 20 )
        self.failIf( space.has_key('n3') )
        
        space = PSpace('adc' )
        self.failUnlessEqual( space.shape , () )

        space = PSpace('adc' ,n1=0 )
        self.failUnlessRaises(TypeError, getattr, space, 'shape')

        space = PSpace('adc' , n1=UnknownValue )
        
        self.failUnlessEqual( space.shape , [UnknownValue] )
        
        self.failUnlessEqual( space.size, None )
        


    def testcopy_eq( self ):
        
        space = PSpace('adc', n1=10, n2=10, data_type='float' )
        
        space_copy = space.copy()
        
        self.failUnlessEqual( space, space_copy )
        # test eq
        self.failUnlessEqual( space.plugin, space_copy.plugin )
        self.failUnlessEqual( space['n1'], space_copy['n1'] )
        self.failUnlessEqual( space['n2'], space_copy['n2'] )
        self.failUnlessEqual( space['data_type'], space_copy['data_type'] )
        
        self.failIfEqual( id(space), id(space_copy) )
        
        
        

    def testunion( self ):
        
        s1 = PSpace('adc', a=1)
        s2 = PSpace('adc', b=2)
        s3 = PSpace('adc', a=1, b=2)
        s4 = PSpace('adc', a=UnknownValue)

        self.failUnlessEqual( s1.union( s2 ), PSpace('adc') )
        
        self.failUnlessEqual( s1.union( s2, s3 ), PSpace('adc') )
        
        self.failUnlessEqual( s1.union( s3 ), s1 )
        
        self.failUnlessEqual( s1.union( s4 ), s1 )


    def testnewParameter( self ):
        if NI: raise NotImplementedError("test not implemented")


    def testequal_keys( self ):
        
        s1 = PSpace('adc', a=1)
        s3 = PSpace('adc', a=1, b=2)
        s4 = PSpace('adc', a=UnknownValue)
        
        self.failUnless( s1.equal_keys( s3, 'a') )
        self.failUnless( s1.equal_keys( s4, 'a', accept_unknown=True ) )
        self.failIf( s1.equal_keys( s4, 'a', accept_unknown=False ) )



    def testintersection( self ):
        
        
        s1 = PSpace('adc', a=1)
        s2 = PSpace('adc', b=2)
        s3 = PSpace('adc', a=1, b=2)
        s4 = PSpace('adc', a=UnknownValue)

        self.failUnlessEqual( s1.intersection( s2 ), s3 )
        
#        self.failUnlessEqual( s1.intersection( s2, s3 ), s3 )
        
        self.failUnlessEqual( s3.intersection( s1 ), s3 )
        
        self.failUnlessEqual( s1.intersection( s4 ), s1 )


def suite():
    return defaultTestLoader.loadTestsFromTestCase( PSpaceTester )
