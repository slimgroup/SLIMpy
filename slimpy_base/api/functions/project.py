## development only
#  @package slimpy_base.api.functions.project
#
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

from pdb import set_trace





def avoid_float_err(x, lamb):
    """
    threshhold to a value close to lamb to avoid a floating point error
    """
#    set_trace()
    xmax = x.max()
    ctr2 = 0
    while abs(xmax) > abs(lamb) * 10000 and xmax / 10000. > 1:
        r = xmax.item( )
        ctr2 += 1
        ctr = 0
        while r / 10000 > 1:
            r = r / 10
            ctr += 1
        
        r = int(r)
        r -= 1
        newxmax = r * ( 10** ctr )
        x = x.thr( newxmax )
        xmaxold = xmax
        xmax = x.max( )
        assert xmax > lamb
    return x

def thr_project(x,lamb=None):
    
    assert lamb is not None
    scal = x.scalar_reduction( 'project' ,lamb=lamb )
    return scal

def project( x,lamb=None ):
    
    if lamb == 0:
        return x.space.zeros() 
    
    csb = x.norm(1)
    if csb <= lamb:
        return x
     
    x = avoid_float_err(x, lamb)
        
    x.flush()
    
    sorted = x.sort( ascmode=False )
    tau = thr_project( sorted, lamb=lamb)
    
    if tau == -1:
        return x.space.zeros( )
    projected = x.thr( tau )
    
    projected.flush()
    return projected
    
