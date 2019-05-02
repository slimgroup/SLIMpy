##@package PadAdiabatic
#    Pads image adiabatically (Neumann conditions, that is repeating boundary conditions)
#
# PadAdiabatic is the padding function. 
# We first allocate space for padded image.
# @code
# def PadAdiabatic(A):
# 
# # Subroutine for Neumann adiabatic extension along the boundary,
# 
# # Input : gray image A of n x m;
# # Output: an expanded image (across four boundary edges)
# 
#  (n, m) = A.shape
#  Ae = np.zeros((n+2, m+2), 'f')
# 
# @endcode
#
# Copy over the original image into the interior
# of the padded image that will be returned by the function.
# @code
#  for i in range(1,n+1):
#     for j in range(1,m+1):
#        Ae[i][j] = A[i-1][j-1]
# @endcode
#
# Copy over each boundary to the boundary of the padded image,
# so that the padded image has values repeated at its boundaries
# @code 
#  #the four boundary edges
#  for j in range(1,m+1):
#     Ae[0][j] = A[0][j-1]
#     Ae[n+1,j] = A[n-1][j-1]
# 
#  for i in range(1,n+1):
#     Ae[i][0]=A[i-1][0]
#     Ae[i][m+1]=A[i-1][m-1]
# @endcode
#
# Also copy over the corners from the original image to the padded image.
# @code 
#  Ae[0][0]=A[0][0]
#  Ae[0][m+1]=A[0][m-1]
#  Ae[n+1][0]=A[n-1][0]
#  Ae[n+1][m+1]=A[n-1][m-1]
# @endcode
#
# Return the padded image.
# @code
#  return Ae
# @endcode

#!/usr/bin/env python
"""
DESCRIPTION:
   Pad image adiabatically (Neumann conditions)

PARAMETERS:
   A: The image to be padded

REQUIREMENTS:
   - Python

Author:
   Reza Shahidi
        Seismic Laboratory for Imaging and Modeling (SLIM)
        Department of Earth & Ocean Sciences (EOS)
        University of British Columbia (UBC)

You may use this code only under the conditions and terms of the
license contained in the file LICENSE provided with this source
code. If you do not agree to these terms you may not use this
software.
"""

import numpy as np
from numpy import *

def PadAdiabatic(A):
    """
    @param A	    The input image which we wish to pad
    """


    # Subroutine for Neumann adiabatic extension along the boundary,
    
    # Input : gray image A of n x m;
    # Output: an expanded image (across four boundary edges)
    
    (n, m) = A.shape
    Ae = np.zeros((n+2, m+2), 'f')
   
    #define the interior of the extended
    for i in range(1,n+1):
       for j in range(1,m+1):
          Ae[i][j] = A[i-1][j-1]
   
    #the four boundary edges
    for j in range(1,m+1):
       Ae[0][j] = A[0][j-1]
       Ae[n+1,j] = A[n-1][j-1]
   
    for i in range(1,n+1):
       Ae[i][0]=A[i-1][0]
       Ae[i][m+1]=A[i-1][m-1]
   
    #the four corners             
    Ae[0][0]=A[0][0]
    Ae[0][m+1]=A[0][m-1]
    Ae[n+1][0]=A[n-1][0]
    Ae[n+1][m+1]=A[n-1][m-1]
   
    return Ae
