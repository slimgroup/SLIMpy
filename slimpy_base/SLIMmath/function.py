"""
Functions that do not directly need SLIMpy infastructure
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


def vector_max( obj1, obj2 ):
    """
    obj1 can be either a scalar or a vector. obj2 must be a vector
    max(obj1,obj2) will return a vector the same size as obj2 with the 
    largest elements taken from obj1 or obj2.
    """
    obj2_trh = obj2.thr( obj1 )
    return obj2_trh + obj1


def cpt( c, A ):
    """
    --latex
    CurveLet Phase Weighting for thresholding.
    \\textit{c} is a SLIMpy vector instance.
    \\textit{A} is a SLIMpy fdct lnear operator instance with Sizes file defined.
    Recall that curvelet coefficients come in pairs, one for sine and one for cosine, 
    or equivalently at angles $\\theta$ and $\\theta$ + $\\pi$, corresponding to the 'phase rotation'.
    Call $\\phi_{\\mu,a}$ and $\\phi_{\\mu,b}$ two curvelets that only differ by this phase rotation operation.
    Then $w_{\\mu,a}$ and $w_{\\mu,b}$ should be the same and defined from
    \\begin{equation}
    \\label{cpt}
    sqrt( {|c_{\\mu,a}|^2 + |c_{\\mu,b}|^2} )
    \\end{equation}
    instead of $c_{\\mu,a}$, resp. $c_{\\mu,b}$.
    Here all the $c_{\\mu}$ are obtained from pred($s_{2}$). 
    It makes sense if you consider the following situation: $c_{\\mu,a}$ may be zero,
    for some non-essential reason (cancellations happen), but $c_{\\mu,b}$ is huge. 
    Then the penalty on primaries should not depend on whether the prediction of the multiples is of type 
    'cosine' or type 'sine' independent of phase rotation.
    Therefore a and b should be treated on the same footing.
    """
    # Create a vector the same length of c 
    cSpace = c.getSpace() 
    v = cSpace.zeros()
    v.flush()

    # get the scales and angles
    #TODO: make space.angles
    an=cSpace.angles()
    

    # copy the first (angleless) scale into the now vector
    v[:an[0][0][0]] = abs( c[:an[0][0][0]] )

    # For each set of angles on a given scale
    for scale in an:
        j = len( scale )/2
        # For half the number of angles on the scale
        for i in range( 0, j ):
        
            # read in an angle
            a1 = c[scale[i][0]-1:scale[i][1]]
            # read in the opposite angle
            a2 = c[scale[i+j][0]-1:scale[i+j][1]]
            
            # Perform the Phase correction
            a3 = ( ( abs( a1 )**2 +abs( a2 )**2 ) )**.5
            
            # Write out the corrected value to each scale in the new vector
            v[scale[i][0]-1:scale[i][1]] = a3
            v[scale[i+j][0]-1:scale[i+j][1]] = a3
            
    return v

