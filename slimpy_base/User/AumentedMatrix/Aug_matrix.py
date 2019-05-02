"""
Augmented Utilites Toolbox
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


from slimpy_base.Core.User.Structures.serial_vector import Vector
from slimpy_base.Core.User.linop.linear_operator import LinearOperator, CompoundOperator
import numpy
from numpy import ndarray,array

class AugMatrix( object ):
    """
    base class for AugmentVector and  AugmentOperator
    """
    def __init__( self, mat ):
        self.matrix = numpy.matrix( mat )
        
    
    def getattrs( self, name ):
        A = self.matrix.A
        B = numpy.zeros_like( A )
        
        for i in range( len( A ) ):
            for j in range( len( A[i] ) ):
                if hasattr( A[i][j], name ):
                    B[i][j] = getattr( A[i][j], name )
        
        return B

    def callattrs( self, name, *args, **kargs ):
        
        A = self.getattrs( name )
        
        for i in range( len( A ) ):
            for j in range( len( A[i] ) ):
                if callable( A[i][j] ):
                    A[i][j] = A[i][j]( *args, **kargs )
        
        return A
    
    def __array__(self):
        return self.matrix.A

class aug_oper( LinearOperator, AugMatrix ):
    """
    Augmented operator class used to combine many operators into a 
    matrix of operators
    """
    def __init__( self, mat ):
        
        AugMatrix.__init__( self, mat )
        
        LinearOperator.__init__( self, self.domain(), self.range() )
        
    
    def __str__( self ):
        """
        Returns the operators name and attributes
        """
        msg = "Augmented Linear Operator:"
        
        spc = '\n'+" "*len( msg )
        mat = str( self.matrix )
        return msg + spc.join( mat.splitlines() )
        
    def getName( self ):
        
        return self.name + ( ( self.isadj and "Adj" ) or '' )
    
    def __repr__( self ):
        """
        Returns the operators name from operator_dict
        """
        return "aug_oper: "+self.matrix.__repr__()
        
    def domain( self ):
        return self.callattrs( "domain" )
        
    def range( self ):
        return self.callattrs( "range" )
    
    def copy( self ):
        """
        Perform shallow copy of self
        """
        return aug_oper( self.matrix )
    
    def adj( self ):
        """
        Returns the adjoint of all the enclosed operators
        and the transpose of this one
        """
        T = self.callattrs( "adj" )
        return aug_oper(T)
        
    def applyop( self, other ):
        """
        apply this operator to an augmented vector  
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix * other.matrix )
        
        if isinstance( other, aug_oper ):
            raise NotImplementedError
        else:
            raise TypeError( "this operator can only be called on a vector or another operator" )
        
    
    def getdim( self ):
        """
        Returns the dimensions of the operator. Usually not defined.
        """
        raise NotImplementedError
#        return [len( self.inSpace ), len( self.outSpace )]
    
        
    def norm( self ):
        """
        reutrns an AugOper that contains the norms of these operators
        """
        return aug_oper( self.callattrs( 'norm' ) )
    
    def normalize( self ):
        """
        reutrns an AugOper that containing Compound operators
        """
        A = self.matrix.A
        B = self.norm().matrix.A
        C = numpy.empty_like( A )
        
        
        for i in range( len( A ) ):
            for j in range( len( A[i] ) ):
                C[i][j] = CompoundOperator( [B[i][j], A[i][j]] )
                
        return aug_oper( C )
    
    def minvelconst( self, *args, **kargs ):
        """
        TODO: take minvelconst out of linear operator 
        """
        return numpy.mat( self.callattrs( 'minvelconst', *args, **kargs ) )
    
    
class aug_vec( Vector, AugMatrix ):
    """
    Augmented vector class used to combine many operators into a 
    matrix of operators
    """    
    def __init__( self, mat ):
        
        AugMatrix.__init__( self, mat )
        
    def __str__( self ):
        return "augmented vector:\n" + str( self.matrix )
    
    def __repr__( self ):
        return "aug_vec:\n" + str( self.matrix )
        
    def __getitem__( self, index ):
        """
        If index is a string: Returns an item from one of the dictionaries. Checks the vector dictionary first.
        If index is a number: Returns a number at index from the binary file.
        """
        return self.matrix.__getitem__( (index, 0) )

    def __setitem__( self, index, item ):
        """
        Sets an item in the vector dictionary
        """
        self.matrix.__setitem__( (index, 0), item ) 
        return 
    
        
    
    def getSpace( self ):
        """
        returns a Space object that contains all of the information
        about this vector
        """
        return self.callattrs( "getSpace" )
                
    # Overloads [i:j] Returns a __numarray array from index i to j from the binary file
    def __getslice__( self, start, stop, step=1 ):
        """
        Returns a numarray array from index i to j from the binary file.
        If j is less than i or i is greater than the length of the vector, returns a numarray array of zero elements. 
        Otherwise it behaves like a list.
        """
        return self.matrix.__getslice__( self, start, stop, step=1 )
        
    # Overloads [i:j] Writes a __numarray array from index i to j to the binary file
    def __setslice__( self, i, j, data ):
        """
        Writes a numarray array from index i to j to the binary file corresponding to the data_container.
        """
        return self.matrix.__setslice__( self, i, j, data )

                            
    # Overload the '+' __operator if other can be a scalar or another vector
    # for self + other invokes math()
    def __add__( self, other ):
        """
        vec1.__add__(vec2) <==> vec1 + vec2
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix.A + other.matrix.A )
        else:
            return aug_vec( self.matrix.A + other )
        


    # Overload the '+' __operator for other + self
    def __radd__( self, other ):
        """
        vec1.__radd__(vec2) <==> vec2 + vec1
        vec2 may be a scalar or a vector
        """
        return self.__add__( other )
        

    # Overload the '-' __operator if other can be a scalar or another vector
    def __neg__( self ):
        """
        vec1.__neg__() <==> -vec1
        """
        return aug_vec( self.callattrs( "__neg__" ) )

    # Overload the '-' __operator if other can be a scalar or another vector
    def __sub__( self, other ):
        """
        vec1.__sub__(vec2) <==> vec1 - vec2
        vec2 may be a scalar or a vector
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix.A - other.matrix.A )
        else:
            return aug_vec( self.matrix.A - other )
            
    # Overload the '-' __operator
    # if other can be a scalar or another vector for other - self
    def __rsub__( self, other ):
        """
        vec1.__rsub__(vec2) <==> vec2 - vec1
        vec2 may be a scalar or a vector
        """
        return aug_vec( self.matrix.A + other )

    # Overload the '/' __operator if other can be a scalar or another vector
    def __div__( self, other ):
        """
        vec1.__div__(vec2) <==> vec1 / vec2
        vec2 may be a scalar or a vector
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix.A / other.matrix.A )
        else:
            return aug_vec( self.matrix.A / other )
        

    # Overload the '/' __operator if other can be a scalar or another vector
    def __rdiv__( self, other ):
        """
        vec1.__rdiv__(vec2) <==> vec2 / vec1
        vec2 may be a scalar or a vector
        """
        return aug_vec( other / self.matrix.A )


    # Overload the '*' __operator if other can be a scalar or another vector
    def __mul__( self, other ):
        """
        vec1.__mul__(vec2) <==> vec1 * vec2
        vec2 may be a scalar or a vector
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix.A * other.matrix.A )
        else:
            return aug_vec( self.matrix.A * other )

    # Overload the '*' __operator if other can be a scalar or another vector
    def __rmul__( self, other ):
        """
        vec1.__rmul__(vec2) <==> vec2 * vec
        """
        return aug_vec( self.matrix.A * other )


    # Overload the '**' __operator if other can be a scalar or another vector
    def __pow__( self, other ):
        """
        vec1.__pow__(vec2) <==> vec1 ** vec2
        vec2 may be a scalar or a vector
        """
        if isinstance( other, aug_vec ):
            return aug_vec( self.matrix.A ** other.matrix.A )
        else:
            return aug_vec( self.matrix.A ** other )

    # Overload abs() 
    def __abs__( self ):
        """
        Vector.__abs__(vec2) <==> abs(vec1)
        vec2 may be a scalar or a vector
        """
        return aug_vec( self.callattrs( "__abs__" ) )
                    
    def rms( self ):
        """    Returns the root mean square"""
        return self.callattrs( "rms" ) 
        
    def max( self ):
        """    Returns the maximum value"""
        return self.callattrs( "max" ).max()
        
    def min( self ):
        """    Returns the minimum value"""
        return self.callattrs( "min" ).min()
        
    def mean( self ):
        """    Returns the mean value"""
        return self.callattrs( "mean" ).mean( axis=2, dtype=None )
        
    def var( self ):
        """    Returns the variance"""
        return self.callattrs( "var" ).var( axis=2 )
        
    def sdt( self ):
        """    Returns the root"""
        return self.callattrs( "sdt" )

        
    def norm( self, lval=2 ):
        """    Returns the lval norm of the vector """
        return numpy.linalg.norm( self.callattrs( "norm", lval=lval ), lval )
    

    # REAL
    def real( self ):
        """
        Returns a vector containing the real component of a complex vector.
        """
        return aug_vec( self.callattrs( "real" ) )
        
    # IMAGINARY
    def imag( self ):
        """
        Returns a vector containing the imaginary component of a complex vector.
        """
        return aug_vec( self.callattrs( "real" ) )

    # THRESHOLD
    def thr( self, obj, mode='soft' ):
        """
        Returns a thresholded vector.
        obj - may be a scalar or a vector.
        mode - may be 'soft', 'hard' or 'nng'
        """
        if isinstance( obj, aug_vec ) or hasattr( obj, "__iter__" ):
            array_obj = array( obj )
            array_obj.resize( self.matrix.shape )
            A = self.getattrs( 'thr' )
            
            for i in range( len( A ) ):
                for j in range( len( A[i] ) ):
                    if callable( A[i][j] ):
                        A[i][j] = A[i][j]( array_obj[i,j],mode=mode )
        
#        return aug_vec( self.callattrs( "thr", obj, mode='soft' ) )
        return aug_vec( A )
    

    # NOISE
    def noise( self, mean=0 ):
        """
        Returns vector with added added random noise.
        mean - noise mean
        """
        return aug_vec( self.callattrs( "noise" , mean=mean ) )

    # SORT
    def sort( self, ascmode=False, memsize=None ):
        """
        Returns a vector with a sorted data set.
        """
        raise NotImplementedError
            
    # ORDER STATISTIC
    def orderstat( self, i ):
        """
        Returns the ith order statistic of the vector (ith smallest element), i.e. i=0 is smallest, i=1 second smallest, etc.)
        Negative indexing starts with the largest element, i.e. i=-1 is largest, i=-2 second largest, etc.
        """
        raise NotImplementedError

    # TRANSP
    #TODO: Move adj to image
    # removes the file
    def adj( self, a1=1, a2=2, memsize=100 ):
        """
        adjose a dataset
        """
        return aug_vec( self.callattrs( "adj" , a1=a1, a2=a2, memsize=memsize ) )
    
    def setName( self, name, path=None ):
        """
        Set the name of all of the vectors in this 
        aug_vec instance.
        appends the position of the vector to the end of its name for example:
        a 1x1 aug_vec 
            v.setname( 'v')
        is equivalent to 
            v[0,0].setname( 'v00')
        """
        A = self.matrix.A
        if isinstance(name, (list,tuple,ndarray)):
#            name_array = array( name )
            assert len(name) == len( A ), "%s != %s" %(len(name),len( A ))
#            assert A.shape == name_array.shape, "%s != %s" %(A.shape, name_array.shape) 
            it = iter(name)
            name_gen = lambda i,j: it.next()
        else:
            name_gen = lambda i,j: name+"%(i)s%(j)s" %vars()
            
        for i in range( len( A ) ):
            for j in range( len( A[i] ) ):
                ij_name = name_gen(i,j)
                if hasattr( A[i][j], "setName" ):
                    A[i][j].setName( ij_name, path=path )
    
    
    
    
    
    
    
    
