"""
defin an window/ cat operator
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


from slimpy_base.Core.User.linop.rclinOp import LinearOperator
from slimpy_base.User.AumentedMatrix.MetaSpace import MetaSpace
from slimpy_base.api.linearops.linear_ops import pad
from slimpy_base.User.AumentedMatrix.AugVector import AugVector
from slimpy_base.utils.permute import permute
from slimpy_base.api.functions.functions import cat
#from numpy import apply_along_axis
from numpy import array, all, clip, size,prod
from numpy import asarray, zeros, product
from slimpy_base.Core.User.linop.linear_operator import Identity



def scatter_gen( inspace, numblocks, overlap ):
    """
    genorator scatter_gen(inspace, numblocks, overlap)
    yeilds pairs of gather,scatter padding keywork arguments.
    
    where gather_kw is 
    """
    shape = inspace.shape
    
    numblocks = list( numblocks )
    overlap = list( overlap )
    
    #===============================================================================
    diff = len( shape ) - len( numblocks ) 
    assert diff >= 0 , "the parameter numblocks must be a list smaller than the shape of the vector"
    if diff > 0:
        # add size 1 blocks in the unset dimentions
        numblocks.extend( [1]*diff )
    #===============================================================================

    #===============================================================================
    diff = len( shape ) - len( overlap ) 
    assert diff >= 0 , "the parameter overlap must be a list smaller than the shape of the vector"
    if diff > 0:
        # add size 1 blocks in the unset dimentions
        overlap.extend( [0]*diff )
        
    overlap = array( overlap )
    #===============================================================================
    
    
    #===============================================================================
    for brk, ln in zip( numblocks, shape ):
        assert brk > 0 , "numblocks must be greater than zero: got %(brk)s" %vars()
        assert ln % brk == 0 , "the numblocks must divide without remainder the length of the data: got %(ln)s % %(brk)s" %vars()
    #===============================================================================
    
    w_size = array( shape ) / array( numblocks )
    assert all( w_size >= overlap )
    
    name_kw = lambda name, i, item : ( "%s%s"%( name, i+1 ), item )

    xblocksize = map( xrange, numblocks )
    enum_perm = lambda xbs: enumerate( permute( xbs ) ) 
    
    for i, block in enum_perm( xblocksize ):
        
        begin_tmp = block * w_size
        end_tmp = shape - ( begin_tmp + w_size )
        
        begin = begin_tmp - overlap/2
        end = end_tmp - overlap/2
        
        begin = clip( begin , 0, shape )
        end = clip( end   , 0, shape )
        
        kw = {}
        kw.update( [ name_kw( "beg", i, item ) for i, item in enumerate( begin ) ] )
        kw.update( [ name_kw( "end", i, item ) for i, item in enumerate( end ) ] )
        
        
        begin_diff = begin_tmp - begin
        end_diff =   end_tmp - end    
        overlap_kw = { }
        overlap_kw.update( [ name_kw( "beg", i, item ) for i, item in enumerate( begin_diff ) ] )
        overlap_kw.update( [ name_kw( "end", i, item ) for i, item in enumerate( end_diff ) ] )
        
#        print "begin_tmp",begin_tmp,"end_tmp",end_tmp
#        print "begin",begin,"end",end
#        print "begin diff",begin_diff,"end diff",end_diff
        yield overlap_kw, kw
    
    return
    
    
def Scatterf( inspace, numblocks, overlap ):
    '''
    Scatterf(inspace, numblocks,overlap) -> ol_list, padlst
    
    
    @param numblocks: number of blocks in each dimention, may be a list 
        no longer than space.shape  
    @type numblocks: list
    @param overlap: the total overlap for each adjasent block.
    @type overlap: list
    
    @return: ol_list: a list of key word arguments that may be used in a 
        gather operator to window the overlap for each block.
             padlst: a list of window operators that may operate on 
         the data.
    '''
    
    padlst = []
    ol_lst = []
    for overlap_kw, kw in scatter_gen( inspace, numblocks, overlap ):
        P = pad( inspace, adj=True, **kw )
        padlst.append( P )

#        O = pad(inspace,adj=True,**overlap_kw)
        ol_lst.append( overlap_kw )        
        
    return ol_lst, padlst


## Break apart a vector into numblocks
# @ingroup linop
class Scatter( LinearOperator ):
    """
    S = Scatter(inspace, blocksize=None, numblocks=None,overlap=None )
    
    Scatter a vector into an Aumented vector.
     
    """
    
    name = "scatter"
    ## Create a Scatter 
    # @return Identity if numblocks is 1 in all directions
    def __new__( cls, *params, **kparams ):
        if 'numblocks' in kparams:
            numblocks = array(kparams['numblocks'])
            if all(numblocks==1):
                return Identity( params[0] )
            
        return LinearOperator.__new__(cls, *params, **kparams)
        
        pass
    
    ## Constructor
    # @param inspace domain of this operator 
    # @param blocksize tuple of size of blocks to break vector into
    # @param numblocks tuple of number of blocks to break vector into
    # @pre only use numblocks or blocksize
    # @param overlap tuple of overlaps in each directions
    def __init__( self, inspace, blocksize=None, numblocks=None, overlap=None ):
        
        if not ( bool( blocksize ) ^ bool( numblocks ) ):
            raise TypeError( "must use either blocksize or numblocks, not both" )
        if not overlap:
            overlap = [ ]
             
        if blocksize:
            numblocks = []
            for block, lngth in zip( blocksize, inspace.shape ):
                
                if block == 0:
                    numblocks.append( 1 )
                else:
                    assert lngth % block == 0   
                    numblocks.append( lngth / block )
        
        overlap_kw, self.pad_operlist = Scatterf( inspace, numblocks, overlap )
        self.numblocks = numblocks
        self.is_identity = prod( self.numblocks ) == 1
        
        if self.is_identity:
            outspace = inspace
        else:
            
            outspace = MetaSpace( [[oper.range() for oper in self.pad_operlist]] ).T #IGNORE:E1101
            
            self.overlap_window = []
            for shard, kw in zip( outspace.ravel() , overlap_kw ):
                O = pad( shard , adj=True, **kw )
                self.overlap_window.append( O )
        
        LinearOperator.__init__( self, inspace, outspace )
        
        return

    def applyop( self, other ):
        if self.is_identity:
            return other
        
        if self.isadj:
            return self.applyop_adj( other )
        else:
            return self.applyop_fwd( other )

    def applyop_fwd( self, other ):
#        assert len(other) == len(self.pad_operlist)
        
        res = []
        push = res.append
        for P in self.pad_operlist:
            push( P.applyop( other ) ) 
        
        return AugVector( [res] ).T #IGNORE:E1101
            
    def applyop_adj( self, other ):
        
        assert len( other ) == len( self.overlap_window )
        
        windows = []
        other_array = array( other )
        for O, shard in zip( self.overlap_window, other_array.ravel() ):
            window = O*shard
            windows.append( window ) 
        
        windowed_array = array( windows )
        other_array = windowed_array.reshape( self.numblocks )
        
        dim = 0
        while len( other_array.shape ):
            dim += 1
            other_array = apply_along_axis( cat, 0, other_array, dim )
            
        return other_array.item()
        

def apply_along_axis( func1d, axis, arr, *args ):
    """ Execute func1d(arr[i],*args) where func1d takes 1-D arrays
        and arr is an N-d array.  i varies so as to apply the function
        along the given axis for each 1-d subarray in arr.
    """
    arr = asarray( arr )
    nd = arr.ndim
    if axis < 0:
        axis += nd
    if ( axis >= nd ):
        raise ValueError( "axis must be less than arr.ndim; axis=%d, rank=%d."
            % ( axis, nd ) )
    ind = [0]*( nd-1 )
    i = zeros( nd, 'O' )
    indlist = range( nd )
    indlist.remove( axis )
    i[axis] = slice( None, None )
    outshape = asarray( arr.shape ).take( indlist )
    i.put( indlist, ind )
    res = func1d( arr[tuple( i.tolist() )], *args )

    # we have a smaller output array
    
    outarr = zeros( outshape, asarray( res ).dtype )
    outarr[tuple( ind )] = res
    Ntot = product( outshape )
    k = 1
    
    while k < Ntot:
        # increment the index
        ind[-1] += 1
        n = -1
        while ( ind[n] >= outshape[n] ) and ( n > ( 1-nd ) ):
            ind[n-1] += 1
            ind[n] = 0
            n -= 1
        i.put( indlist, ind )
        res = func1d( arr[tuple( i.tolist() )], *args )
        outarr[tuple( ind )] = res
        k += 1
    return outarr


class EdgeUpdate( LinearOperator ):
    
    def __init__(self ,inspace, numblocks, overlap ):
        self.numblocks = numblocks
        self.overlap = overlap
        LinearOperator.__init__( self, inspace, inspace )
        
    
    def apply( self, other ):
        if self.isadj:
            return self.applyop_adj( other )
        else:
            return self.applyop_adj( other )
    
    
    def applyop_adj(self ,other ):
        
        other_array = other.reshape( self.numblocks )
        
        for dim in  range( other_array.ndims ): 
            
            other_array = apply_along_axis( edge_swap , dim, other_array ,dim )
    


def edge_swap( arry, dim ):
    
    lst = arry.tolist( )
    for i in range( len(lst) - 1 ) :
        a = lst[ i ]
        b = lst[ i+1 ]
        
        W1 = pad() 
        W2 = pad()
        
        anew = W1*a
        bnew = W2*b 
        
        res1 = cat( [anew, bnew], dim )
        
        W3 = pad( ) 
        W4 = pad( )
        
        anew = W3*b 
        bnew = W4*a 
        
        res2 = cat( [anew, bnew], dim )
        
        lst[ i ] = res1  
        lst[ i+1 ] = res2
        


