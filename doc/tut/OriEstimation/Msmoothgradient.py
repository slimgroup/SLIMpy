##@package Msmoothgradient
# Return gradient of input image with smoothing orthogonal to gradient direction
# 
# @code
# import rsf as sf
# import numpy as np
# @endcode
# Import RSF and NumPy packages as they will be used later in the code
# 
# @code
# from Sadiabatic import *
# @endcode
# Sadiabatic is a package containing a function of the same name used for
# padding the boundaries of the image with repetition (Neumann boundary conditions)
# 
# Get the RSF parameters for this function
# @code
# par = sf.Par()
# @endcode
# 
# Get the name of the file for which we want to calculate the gradients from the RSF input.
# As well, output1 is the name of the RSF file to which we write the gradient values in the
# x direction, and output2 is the RSF filename for writing the gradient values in the y
# direction.
# @code
# input  = sf.Input()
# output1 = sf.Input(par.string("dx_outputfilename"))
# output2 = sf.Input(par.string("dy_outputfilename"))
# @endcode
# 
# n1 is the width of the image and n2 is the height of the image
# @code
# n1 = input.int("n1")
# n2 = input.int("n2")
# @endcode
# 
# Make sure the input is 2-D.  Otherwise, the gradients cannot be calculated with this code.
# @code
# ni = input.size(2)
# assert ni == 1,"sfsmoothgradient needs 2D input"
# @endcode
# 
# Read in the input image
# @code
# inputimage = np.zeros((n1,n2),'f')
# input.read(inputimage)
# @endcode
# 
# Pad the input image with repetition so that gradients can be calculated on the boundaries.
# @code
# input_padded = Sadiabatic(inputimage)
# @endcode
# 
# Used for indexing of image for computation of gradient
# @code
# I = array(range(1,n1+1))
# J = array(range(1,n2+1))
# @endcode
# 
# Calculate gradient in x direction
# @code
# Imx = (3*input_padded[I+1][:,J-1]+10*input_padded[I+1][:,J]+3*input_padded[I+1][:,J+1]-3*input_padded[I-1][:,J-1]-10*input_padded[I-1][:,J]-3*input_padded[I-1][:,J+1])/32
# @endcode
# 
# Calculate gradient in y direction
# @code
# Imy = (3*input_padded[I-1][:,J+1]+10*input_padded[I][:,J+1]+3*input_padded[I+1][:,J+1]-3*input_padded[I-1][:,J-1]-10*input_padded[I][:,J-1]-3*input_padded[I+1][:,J-1])/32
# @endcode
# 
# Write directional gradients (in x and y directions) to appropriate output files
# @code
# output1.put("n1",n1)
# output1.put("n2",n2)
# output1.write(Imx)
# 
# output2.put("n1",n1)
# output2.put("n2",n2)
# output2.write(Imy)
# @endcode

#!/usr/bin/env python
# Author: R. Shahidi
#         Seismic Laboratory for Imaging and Modeling
#         Department of Earch & Ocean Sciences
#         The University of British Columbia
#         
# Date  : July, 2008 

#  Copyright (C) 2008 The University of British Columbia at Vancouver
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import rsf as sf
import numpy as np
import sys
from PadAdiabatic import *

par = sf.Par()

input  = sf.Input()
print>>sys.stderr,par
print>>sys.stderr,par.string("dx_outputfilename")
print>>sys.stderr,par.string("dy_outputfilename")
output1 = sf.Output(par.string("dx_outputfilename"))
output2 = sf.Output(par.string("dy_outputfilename"))

n1 = input.int("n1")
n2 = input.int("n2")
ni = input.size(2)
assert ni == 1,"sfsmoothgradient needs 2D input"

inputimage = np.zeros((n1,n2),'f')
input.read(inputimage)
input_padded = PadAdiabatic(inputimage)

# Used for indexing of image for computation of gradient
I = array(range(1,n1+1))
J = array(range(1,n2+1))

# Gradient in x direction
Imx = (3*input_padded[I+1][:,J-1]+10*input_padded[I+1][:,J]+3*input_padded[I+1][:,J+1]-3*input_padded[I-1][:,J-1]-10*input_padded[I-1][:,J]-3*input_padded[I-1][:,J+1])/32

# Gradient in y direction
Imy = (3*input_padded[I-1][:,J+1]+10*input_padded[I][:,J+1]+3*input_padded[I+1][:,J+1]-3*input_padded[I-1][:,J-1]-10*input_padded[I][:,J-1]-3*input_padded[I+1][:,J-1])/32

# Write directional gradients to output files
output1.put("n1",n1)
output1.put("n2",n2)
output1.write(Imx)

output2.put("n1",n1)
output2.put("n2",n2)
output2.write(Imy)
