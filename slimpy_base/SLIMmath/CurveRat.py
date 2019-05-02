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


from numpy import ceil

def curverat(curvec1,curvec2,cutv):
    """
    --latex
    This approach is based on rescaling the weighting vectors ( $w_{1}$
    or $w_{2}$ ) in such a way that after the application of the rescaled vectors for soft 
    thresholding a certain percentage (the n relatively largest coefficients) remain in 
    the thresholded vector per scale or globally.
    The operation is based on the following steps:
    \\begin{enumerate}
    \\item Initialize a vector of the size of the to be thresholded and thresholding 
    vector 
    \\item Calculate the ratio ( rat = curvec1 / curvec2 ) over the total vector.
    \\item Sort rat in descending order to evaluate for the coefficients mainly con- 
    tributing to curvec1 
    \\item Take the value of the sorted rat vector defined by an initial percentage of 
    values you want to keep cutv.
    \\end{enumerate}
    """
    temp = curvec1 / curvec2
    sorted_temp = abs(temp).real().sort()
    cutoff = int( ceil(len(sorted_temp.getSpace())*cutv) )
    scaling=sorted_temp[cutoff]

    return scaling

