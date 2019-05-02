"""
Parameter class is equivalent to a header file for data
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


class _param( dict ):
    """
    parameter is a simple tracking method to pass Metadata without
    being bound to each specific datatype
    """
    
    def makeContaner( self, command=None ):
        """
        Make a new container from the current parameters
        
        """
        return self["plugin"]( parameters=self, command=command )
    
    def newParameter( self, **keys ):
        """
        Make a new parameter updated with the new keys, 'keys'
        """
        x = param( self )
        x.update( keys )
        return self.__class__( **x )
    
    def getParameters( self ):
        """
        for consistency returns this instance
        """
        return self
    
    def copy( self ):
        return param( dict.copy( self ) )
    
    def shape( self ):
        """
        Returns a list of the dimensions of the image of the underlying vector
        """
        shp = []
        
        N = 1
        while self.has_key( "n%s" %N ):
            val = self["n%s" %N]
            if val < 1:
                raise TypeError( "shape parameter does not conform to SLIMpy standard:\n"
                                "Should be an int greater than 0" )
            shp.append( val )
            N += 1
        
        if N is 1:
            raise TypeError( "space has no shape\n"
                            "Should contain values of n1, n2, etc." )
            
        i = len( shp ) -1
        while i > 1 and shp[i] is 1:
            shp.pop( -1 )
            i -= 1
            
        return shp
    

    def _get_size(self):
        mul = lambda x,y:x*y
        prod = lambda shape:reduce( mul, shape, 1 )
        shape = self.shape_
        if not shape:
            return 0
        else:
            return prod(shape)
        
    size = property( _get_size )
    
    def union(self,*E,**kw):
        '''
        par.union(par2 [, par3 ...] ,**kw ) --> param
        returns a new space that is a subspace of par and
        par2 ... and kw 
        '''
        if kw:
            new = self._unionhelper(kw)
        else:
            new =self
            
        for kw in E:
            new = new._unionhelper(kw)
            
        return new
    
    def _unionhelper( self, kw ):
        '''
        returns a new param that is  
        '''
        
        set_self = set(self.keys() )
        set_other = set(kw.keys() )
    
        
        union = set_self.union(set_other)
        diff1 = set_self.difference( set_other )
        diff2 = set_other.difference( set_self )
        
        new = param()
        for key in union:
            v1 = self[key];v2 = kw[key]
            if not self[key] == kw[key]:
                raise ValueError("item self[%(key)s] != other[%(key)s] ; %(v1)s != %(v2)s")
            new[key] = self[key]
            
        for key in diff1:
            new[key] = self[key]
        for key in diff2:
            new[key] = kw[key]
    
    def is_subspace(self,other ):
        
        key_set = set( self.keys() )
        key_set_other = set( other.keys() )
        
        
        issubset = key_set_other.issubset( key_set )
        
        if not issubset:
            return False
        
        for key in key_set_other:
            if not self[key] == other[key]:
                return False
            
        return True
