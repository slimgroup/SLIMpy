"""
Vector Interface.

"""

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

# IMPORTS
from slimpy_base.Core.Interface.AbstractDataInterface import ADI
from slimpy_base.Core.Interface.node import Source
from slimpy_base.Core.User.Structures.Scalar import  Scalar
from slimpy_base.Environment.InstanceManager import InstanceManager
from slimpy_base.api.functions.vector_product import inner_product, outer_product
from os.path import join
from slimpy_base.api.functions import spboolean
from slimpy_base.Core.User.Structures.VectorType import VectorType
from slimpy_base.Core.User.Structures.VectorType import is_vector
from numpy import ndarray

# END OF IMPORTS

## Vector containing a data container
# @ingroup userclasses
class Vector( ADI ): 
    """
    When creating a SLIMpy Vector using the command 
    vector(filename) several variables are initialized.
    The only input that the user should need is `file` 
    corresponding to a file on disk. The other variables are mostly for internal use.
    If file is not None, creates a vector instance with a pointer to the file `file`.
    If create is given as a list on integers a vector with a temporary 
    name and the given size will be created.
    There are more easy to use functions such as zeros to create a file
    """
    ## for string
    name = "Vector"

    ## slimpy global variables
    env = InstanceManager()
    
    ## vector implements  VectorType
    __metaclass__ = VectorType
    
    
    def __new__( cls, *args ): #IGNORE
        if args and isinstance(args[0], ndarray):
            from slimpy_base.User.AumentedMatrix.AugVector import AugVector
            avec = AugVector( args[0] ).ravel()
            for idx, container in enumerate( avec):
                avec[idx] = Vector( container )
            return avec
        else:
            return object.__new__( cls, *args )
    
    ## Constructor form a data container
    def __init__( self, container ):
        """
        data - must be a data_container.
        
        """
        ADI.__init__( self, container )
        self.__transpose_flag = False
        self.__sorted_vector = None
        
    ##########################################################################
    ###                      OPERATOR OVERLOADS                            ###
    ##########################################################################
    
    def _get_transp_flag(self):
        return self.__transpose_flag
    def _set_transp_flag(self,val):
        self.__transpose_flag = bool(val)
    
    ## test if vector is transposed    
    is_transp = property( _get_transp_flag, _set_transp_flag )
     


    def __setitem__( self, index, item ):
        """
        Sets an item in the vector dictionary
        """
        raise Exception, "not implemented. Ask me to do it later"
    
    ## returns a @ref slimpy_base.Core.User.Structures.VectorSpace.VectorSpace "VectorSpace"  representing this vector
    def getSpace( self ):
        """
        returns a Space object that contains all of the information
        about this vector
        """
        from slimpy_base.Core.User.Structures.VectorSpace import VectorSpace
        
        return VectorSpace( self.getParameters( ) )
    
    ## getter property for getSpace  
    space = property( getSpace )
                
# Overloads [i:j] Returns a __numarray array from index i to j from the binary file
#    def __getslice__(self,start,stop,step=1):
#        """
#        Returns a numarray array from index i to j from the binary file.
#        If j is less than i or i is greater than the length of the vector, returns a 
#        numarray array of zero elements. 
#        Otherwise it behaves like a list.
#        """
#        s = slice(start,stop,step)
#        
#        return self.genScalar('getslice',s)
        #raise Exception , "not implemented. Ask me to do it later"

    # Overloads [i:j] Writes a __numarray array from index i to j to the binary file
    
    ## set a slice of this data inplace
    def __setslice__( self, i, j, data ):
        """
        Writes a numarray array from index i to j to the binary 
        file corresponding to the data_container.
        """
        raise Exception , "not implemented. Ask me to do it later"

    ## @name Vector Transformation Operations
    # 
    # @{

    ## Overload the '+' __operator if other can be a scalar or another vector
    # for self + other invokes math()
    def __add__( self, other ):
        """
        vec1.__add__(vec2) <==> vec1 + vec2
        """
        if other is 0:
            return self
        if other is self:
            return self *2
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'add', vec=par )
        else:
            par = self.source_or_num( par )
            return self.generateNew( 'add', par )
        
    ## Overload the '+' __operator for other + self
    def __radd__( self, other ):
        """
        vec1.__radd__(vec2) <==> vec2 + vec1
        vec2 may be a scalar or a vector
        """
    
        return ( self + other )

    ## Overload the '-' __operator if other can be a scalar or another vector
    def __neg__( self ):
        """
        vec1.__neg__() <==> -vec1
        """
        return self.generateNew( 'neg' )

    ## Overload the '-' __operator if other can be a scalar or another vector
    def __sub__( self, other ):
        """
        self..__sub__(other) <==> self - other
        vec2 may be a scalar or a vector
        """
        if other is 0:
            return self
        if other is self:
            return self.space.zeros()
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'sub', vec=par )
        else:
            par = self.source_or_num( par )
            return self.generateNew( 'sub', par )
            
    ## Overload the '-' __operator
    # if other can be a scalar or another vector for other - self
    def __rsub__( self, other ):
        """
        vec1.__rsub__(vec2) <==> vec2 - vec1
        vec2 may be a scalar or a vector
        """
        
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'rsub', vec=par )
        else:
            par = self.source_or_num( par )

            return self.generateNew( 'rsub', par )

    ## Overload the '/' __operator if other can be a scalar or another vector
    def __div__( self, other ):
        """
        vec1.__div__(vec2) <==> vec1 / vec2
        vec2 may be a scalar or a vector
        """
        if other is 1:
            return self
        if other is self:
            return self.space.ones() 
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'div', vec=par )
        else:
            par = self.source_or_num( par )

            return self.generateNew( 'div', par )

    ## Overload the '/' __operator if other can be a scalar or another vector
    def __rdiv__( self, other ):
        """
        vec1.__rdiv__(vec2) <==> vec2 / vec1
        vec2 may be a scalar or a vector
        """
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'rdiv', vec=par )
        else:
            par = self.source_or_num( par )
            return self.generateNew( 'rdiv', par )

    ## Overload the '*' __operator if other can be a scalar or another vector
    def __mul__( self, other ):
        """
        vec1.__mul__(vec2) <==> vec1 * vec2
        vec2 may be a scalar or a vector
        """
        if other is 0:
            return 0
        if other is 1:
            return self
        if other is self:
            return self ** 2
        
        par = other
        if isinstance( other, Vector ):
            
            if self.is_transp ^ other.is_transp:
                if self.is_transp:
                    return inner_product( self, other )
                else:
                    return outer_product( self, other )
                
            par = Source( other.getContainer() )
            return self.generateNew( 'mul', vec=par )
        else:
            par = self.source_or_num( par )

            return self.generateNew( 'mul', par )
        
    ## Overload the '*' __operator if other can be a scalar or another vector
    def __rmul__( self, other ):
        """
        vec1.__rmul__(vec2) <==> vec2 * vec
        """
        return self.__mul__( other )

    ## Overload the '**' __operator if other can be a scalar or another vector
    def __pow__( self, other ):
        """
        vec1.__pow__(vec2) <==> vec1 ** vec2
        vec2 may be a scalar or a vector
        """
        if other is 1:
            return self
        par = other
        if isinstance( other, Vector ):
            par = Source( other.getContainer() )
            return self.generateNew( 'pow', vec=par )
        else:
            par = self.source_or_num( par )

            return self.generateNew( 'pow', par )

    ## Overload abs() 
    def __abs__( self ):
        """
        Vector.__abs__(vec2) <==> abs(vec1)
        vec2 may be a scalar or a vector
        """
        return self.generateNew( 'abs' )

    ##########################################################################
    # Boolean comparison operators 
    ##########################################################################
    
    ## boolean comparison
    def __or__(self, other):
        """
        vec1 | vec2 -> vec3
        """
        return spboolean.or_( self, other )
    
    ## boolean comparison
    def __and__(self,other):
        "vec1 & vec2 -> vec3"
        return spboolean.and_( self, other )
    
    ## boolean comparison
    def __lt__(self,other):
        """
        vec1.__lt__(vec2) <==> vec1 < vec2
        """
        return spboolean.less_than( self, other )

    ## boolean comparison
    def __gt__(self,other):
        """
        vec1.__gt__(vec2) <==> vec1 > vec2
        """
        return spboolean.greater_than( self, other )

    ## boolean comparison
    def __le__(self,other):
        """
        vec1.__le__(vec2) <==> vec1 <= vec2
        """
        return spboolean.less_than_eq(self, other)
    
    ## boolean comparison
    def __ge__(self,other):
        """
        vec1.__lt__(vec2) <==> vec1 >= vec2
        """
        return spboolean.greater_than_eq(self, other)

    ## boolean comparison
    def __eq__(self,other):
        """
        vec1.__eq__(vec2) <==> vec1 == vec2
        """
        return spboolean.equal(self, other)
    
    ## boolean comparison
    def __ne__(self,other):
        """
        vec1.__ne__(vec2) <==> vec1 != vec2
        """
        return spboolean.not_equal( self, other )

    ## thresholding operation
    # @param obj can be a Scalar or vector
    # @param mode one of 'soft', 'hard' or 'nng'
    def thr( self, obj, mode='soft' ):
        """
        Returns a thresholded vector.
        obj - may be a scalar or a vector.
        mode - may be 'soft', 'hard' or 'nng'
        """
        par = obj
        if isinstance( obj, Vector ):
            par = Source( obj.getContainer() )
            return self.generateNew( 'thr' , mode=mode, fthr=par )
        else:
            par = self.source_or_num( par )

            return self.generateNew( 'thr' , mode=mode, thr=par )

    ## hard thresholding
    def thrhard( self, obj ):
        """
        Returns a thresholded vector.
        obj - may be a scalar or a vector.
        Same as vector.sort(obj,'hard')
        """
        return self.thr( obj, mode='hard' )

    def garrote( self, obj ):
        """
        Returns a garroted vector.
        obj - may be a scalar or a vector.
        Same as vector.sort(obj,'nng')
        """
        return self.thr( obj, mode='nng' )        


    ## Sort a vector by absolute values
    # @param ascmode sort in ascending or descending order 
    # @param memsize define memory size of system 
    def sort( self, ascmode=False, memsize=None ):
        """
        Returns a vector with a sorted data set.
        """
        if memsize is None:
            memsize = self.env['slimvars']['memsize']
        
        return self.generateNew( "sort", memsize=memsize, ascmode=ascmode )

    ## real part of vector 
    def __real__( self ):
        """
        Returns a vector containing the real component of a complex vector.
        """
        if self.space.isComplex():
            return self.generateNew( 'real' )
        else:
            return self
       
    ## imaginary part of vector
    def __imag__( self ):
        """
        Returns a vector containing the imaginary component of a complex vector.
        """
        return self.generateNew( 'imag' )
    

    ## @}

    real =  __real__ 
    imag =  __imag__ 
    
    ##########################################################################
    ###                  END OF OPERATOR OVERLOADS                         ###
    ##########################################################################
    
    ## @name Scalar Reduction Operations
    # 
    # @{
    
    def __getitem__( self, index ):
        """
        If index is a string: Returns an item from one of the dictionaries. 
        Checks the vector dictionary first.
        If index is a number: Returns a number at index from the binary file.
        """
        
        if isinstance( index, (int,Scalar) ):
            ind = self.source_or_num(index)
            return self.scalar_reduction( 'getitem', ind )
        
        elif isinstance( index, str ):
            raise Exception, "not implemented. Ask me to do it later"
        
        elif isinstance( index, slice ):
            
            l = len( self.getSpace() )
            ind = index.indices( l )
            return self.scalar_reduction( 'getslice', ind )
        else:
            raise TypeError , "expected int or string got %s" % type( index )

    ## root mean square of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def rms( self ):
        """    Returns the root mean square"""
        return self.scalar_reduction( 'rms' )

    ## maximum element of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def max( self ):
        """    Returns the maximum value"""
        return self.scalar_reduction( 'max' )

    ## minimum element of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def min( self ):
        """    Returns the minimum value"""
        return self.scalar_reduction( 'min' )

    ## mean value of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def mean( self ):
        """    Returns the mean value"""
        return self.scalar_reduction( 'mean' )

    ## variance of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def var( self ):
        """    Returns the variance"""
        return self.scalar_reduction( 'var' )
    
    ## standard deviation of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    def sdt( self ):
        """    Returns the standard deviation"""
        return self.scalar_reduction( 'std' )

    ## lval-norm of vector
    # @return a slimpy_base.Core.User.Structures.Scalar.Scalar object
    # @param lval power of the norm
    def norm( self, lval=2 ):
        """    Returns the lval norm of the vector """
        return self.scalar_reduction( 'norm', lval )
   
    ## ith order statistic of the vector (ith smallest element),
    # @param i index within size of vector
    def orderstat( self, i ):
        """
        Returns the ith order statistic of the vector (ith smallest element), 
        i.e. i=0 is smallest, i=1 second smallest, etc.)
        Negative indexing starts with the largest element, i.e. i=-1 is largest, 
        i=-2 second largest, etc.
        """
        if not 'sorted' in self.__dict__:
            self.sorted = self.sort( ascmode=False )
                    
        if i<0:
            i = len( self.getSpace() ) + i
        
        return self.sorted[i]            

    ## @}
    # 
    

    
    #===============================================================================
    # DEPRECATED    
    #===============================================================================
    
    ## @name Deprecated
    # these functions have been replaced by linear operators
    # @{
     
    def conj( self ):
        """
        return vector conjugate of data
        """
        if self.space.isComplex():
            return self.generateNew( 'conj' )
        else:
            return self
    
    ## gradient of the vector
    def grad( self ):
        """
        Returns a vector containing the gradient of the vector.
        """
        #return __comp([self.generateNew('halfderiv'),self.generateNew('halfderiv')])
        return self.generateNew( 'grad' )

    # NOISE
    def noise( self, mean=0, seed=None ):
        """
        Returns vector with added random noise.
        mean - noise mean
        seed - noise seed
        """
        param = dict( mean=mean, seed=seed )
        if seed is None:
            param.pop( 'seed', None )
        
        return self.generateNew( 'noise', **param )

    ## TRANSP
    # @TODO: Move transp to image
    # @deprecated  
    def transp( self, a1=1, a2=2, memsize=100 ):
        """
        transpose a dataset
        """
        if a1 == a2:
            return self

        return self.generateNew( 'transp', plane=( a1, a2 ), memsize=memsize )

    ## @}
    
            
    
    def _transpose(self):
        vec = Vector( self.container )
        vec.is_transp = not vec.is_transp
        return vec
    
    ## symbolic transpose of the vector 
    # @warning does not transpose underlying image  
    T = property( _transpose )

    def _conj_transp(self):
        
        vec = Vector(self.container).conj( )
        vec.is_transp = not self.is_transp
        return vec
    
    H = property( _conj_transp )
    
    ## sets the name of the file on disk
    def setName( self, name, path=None ):
        """
        set the name of this vector. Makes it non persistent.
        """
        if not path is None:
            name = join( path, name )
            
        container = self.getContainer()
        
        container.setName( name , path=None )
        self.env['graphmgr'].add_target( container )
        
        return self 
    
    ## plot vector 
    # @todo: should not be a vector method  
    def plot( self, command=None, plotcmd=None ):
        """
        calls plot method of this vectors container
        """
        try:
            self.flush()
        except:  #IGNORE:W0704
            pass #IGNORE:W0702
        self.container.plot( command=command, plotcmd=plotcmd )
    
    ## reshape underlying image
    # @todo: should not be a vector method
    def reshape(self, *shape):
        if len(shape) is 1 and isinstance(shape[0], (list,tuple)):
            shape = shape[0]
            
        return self.generateNew( "reshape" , shape=shape )
    

isvector = lambda obj : isinstance( obj, Vector )
