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

def mk2( g ):

    g.appendEdge( "socks", "shoes" )
    g.appendEdge( "undershorts", "socks" )
    g.appendEdge( "undershorts", "pants" )
    g.appendEdge( "pants", "shoes" )
    g.appendEdge( "pants", "jacket" )
    g.appendEdge( "pants", "belt" )
    g.appendEdge( "shirt", "belt" )
    g.appendEdge( "shirt", "tie" )
    g.appendEdge( "belt", "jacket" )
    g.appendEdge( "tie", "jacket" )
    return g

def mk3( g ):
    g.appendEdge( 'd1', 'c1' , True, 'red' )
    g.appendEdge( 'c1', 'd2' , True, 'green' )
    g.appendEdge( 'd1', 'c2' , True, 'red' )
    g.appendEdge( 'c2', 'd3' , True, 'green' )
    g.appendEdge( 'd2', 'c3' , True, 'red' )
    g.appendEdge( 'd3', 'c3' , False, 'red' )
    g.appendEdge( 'c3', 'd4' , True, 'green' )
    g.setBuildTargets( 'd4' )
    return g



def mk3cycle( g ):
    g.appendEdge( 'data', 'fdct' , True, 'red' )
    g.appendEdge( 'fdct', 'sizes' , False, 'green' )
    g.appendEdge( 'sizes', 'fdctInv' , False, 'red' )
    g.appendEdge( 'fdct', 'newdata' , True, 'green' ) 
    g.appendEdge( 'newdata', 'fdctInv' , True, 'red' )
    g.appendEdge( 'fdctInv', 'final' , True, 'green' )
    g.setBuildTargets( 'final' )
    return g
    

def lw1( g ):
    """
    None < ['sfmath output=0 n2=10 type=complex n1=6', 'sfput n1_fft=10'] > tmp.cMLwY2.rsf  
    tmp.cMLwY2.rsf < ['sffft1 opt=n inv=y sym=y', 'sffft1 opt=n inv=n sym=y'] > tmp.MXrCe6.rsf  
    None < ['sfmath output=0 n2=10 type=float n1=10', 'sfput ', 'sffft1 opt=n inv=n sym=y', 'sfmath output="input-vec" vec=tmp.MXrCe6.rsf', 'sfmath output="vec+input" vec=tmp.cMLwY2.rsf', 'sfthr mode=soft thr=0.007'] > x.rsf  
    """
    g.appendEdge ( "sfput  ID:20193104"  , "KfiGxq"                                   , True , "green" )
    g.appendEdge ( "sfmath output='input-vec' vec=MXrCe6 ID:20213968"  , "S1CVC3"     , True , "green" ) 
    g.appendEdge ( "sfmath output=0 n2=10 type=float n1=10 ID:20193136"  , "sfput  ID:20193104"   , True , "green" )
    g.appendEdge ( "sfmath output='vec+input' vec=cMLwY2 ID:20217232"  , "RFL5yr"     , True , "green" )
    g.appendEdge ( "sffft1 opt=n inv=n sym=y ID:20217264"  , "G820lD"                 , True , "green" )
    g.appendEdge ( "sfthr mode=soft thr=0.007 ID:20217808"  , "x"                     , True , "green" )
    g.appendEdge ( "sfput n1_fft=10 ID:20217424"  , "cMLwY2"                          , True , "green" )
    g.appendEdge ( "sfmath output=0 n2=10 type=complex n1=6 ID:20217456"  , "sfput n1_fft=10 ID:20217424" , True , "green" ) 
    g.appendEdge ( "sffft1 opt=n inv=y sym=y ID:20217584"  , "m6XWZK"                 , True , "green" ) 
    g.appendEdge ( "sffft1 opt=n inv=n sym=y ID:20217648"  , "MXrCe6"                 , True , "green" )
    
    
    g.appendEdge ( "m6XWZK"  , "sffft1 opt=n inv=n sym=y ID:20217648"                 , True )
    g.appendEdge ( "G820lD"  , "sfmath output='input-vec' vec=MXrCe6 ID:20213968"     , True )
    g.appendEdge ( "KfiGxq"  , "sffft1 opt=n inv=n sym=y ID:20217264"                 , True )
    g.appendEdge ( "cMLwY2"  , "sffft1 opt=n inv=y sym=y ID:20217584"                 , True )
    g.appendEdge ( "cMLwY2"  , "sfmath output='vec+input' vec=cMLwY2 ID:20217232"     , False ) 
    g.appendEdge ( "MXrCe6"  , "sfmath output='input-vec' vec=MXrCe6 ID:20213968"     , False ) 
    g.appendEdge ( "RFL5yr"  , "sfthr mode=soft thr=0.007 ID:20217808"                , True ) 
    g.appendEdge ( "S1CVC3"  , "sfmath output='vec+input' vec=cMLwY2 ID:20217232"     , True ) 

    g.setBuildTargets( "x" )
    
    
    




