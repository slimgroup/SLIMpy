## @package OrientationEstimation
# This is a package which estimates gradient orientations with the linear structure tensor.
# 
# Below, pieces of the actual code are shown in sequence, with a brief description of what
# the code does preceding the corresponding code snippet.
#
# First, we give the proper usage for this module.
# \par
# @code
# usage="\nOrientationEstimation.py target=theta.rsf datafile=data.rsf" 
# @endcode
# 
# Then we import the SLIMpy, Numpy, rsf and slimproj packages into current module.
# @code
# from SLIMpy import *
# import numpy as np
# import rsf as sf
# from slimproj import *
# @endcode
# 
# Set the default value for the input filename containing the initial gradient estimate of the image
# @code
# defaults = {
# 'inputgrad_filename':'marmousi_grad.rsf',     #Input data as y
# }
# @endcode
# 
# The new_average_bldr function is a builder function 
# which takes the image to which we wish to apply
# the sliding average window (z) as its first argument
# and the size of the averaging window (filtersize) as
# its second argument.
# @code
# def new_average_bldr( vectors ):
#     \"""
#     use our new averaging operator
#     \"""
#     z = vectors[0]
#     filtersize = vectors[1]
# @endcode
# Initialize averaging filters in x and y directions
# (both are the same in this case)
# @code
#     averagefilterx = np.ones((1,filtersize))/filtersize
#     averagefiltery = np.ones((1,filtersize))/filtersize
# @endcode
#
# Allocate the output (averaged) image    
# @code 
#     (M,N) = z.shape
#     x = np.zeros((M,N),'f')
# @endcode
# 
#     First average along each row, and then along each column.  
#     This is equivalent to taking the average in a rectangular
#     (in this case square) window across the image.
#     @code
#     for i in range(0,M):
#        x[i,:] = np.convolve(z[i,:],np.ones(filtersize)/filtersize,mode='same')
# 
#     for j in range(0,N):
#        x[:,j] = np.convolve(x[:,j],np.ones(filtersize)/filtersize,mode='same') 
#     @endcode
# 
#     Return the image computed by taking windowed averages.
#     @code
#     return x
#     @endcode
#  
# 
#    Read in input image.
#    @code
# def OrientationEstimation( target, source, env ): 
#    inputfilename = source[0]
#    inputimage = sf.Input(source[0])
#    @endcode
# 
#    M is the number of rows and N is the number of columns in image 
#    @code
#    M = inputimage.int("n2")
#    N = inputimage.int("n1")
#    @endcode
# 
#    Read in previously computed partial derivative in x direction
#    @code
#    Jx = np.zeros((M,N),'f')
#    noisyinputgradx_filename = source[1]
#    noisyinputgradxrsf = sf.Input(noisyinputgradx_filename)
#    noisyinputgradxrsf.read(Jx)
#    @endcode
# 
#    Read in previously computed partial derivative in y direction
#    @code
#    Jy = np.zeros((M,N),'f')
#    noisyinputgrady_filename = source[2]
#    noisyinputgradyrsf = sf.Input(noisyinputgrady_filename)
#    noisyinputgradyrsf.read(Jy)
#    @endcode
# 
#    Allocate space for elements of structure tensor and initialize to zero.
#    @code 
#    Jtensorxx = np.zeros((M,N))
#    Jtensorxy = np.zeros((M,N))
#    Jtensoryy = np.zeros((M,N))
#    @endcode
# 
#    Form elements of structure tensor (Outer product of gradient vector with itself).
#    @code
#    Jtensorxx = Jx*Jx
#    Jtensorxy = Jx*Jy
#    Jtensoryy = Jy*Jy
#    @endcode
# 
#    Replace each pixel's structure tensor with a local average of the structure tensor around
#    the pixel.
#    @code
#    averagefilterwidth = 5 
#    Jtensorxx = new_average_bldr([Jtensorxx,averagefilterwidth])
#    Jtensorxy = new_average_bldr([Jtensorxy,averagefilterwidth])
#    Jtensoryy = new_average_bldr([Jtensoryy,averagefilterwidth])
#    @endcode
#   
#    Estimated gradient orientation is in the same direction
#    as the eigenvector corresponding to the largest eigenvalue
#    of the structure tensor.
#    @code
#    Jtensoreig = np.zeros((2,M,N),'f')
#    Jmag = np.zeros((M,N),'f')
#    tempJ = np.zeros((2,2),'f')
#    for i in range(0,M):
#       for j in range(0,N):
#          tempJ[0,0] = Jtensorxx[i,j]
#          tempJ[0,1] = Jtensorxy[i,j]
#          tempJ[1,0] = Jtensorxy[i,j]
#          tempJ[1,1] = Jtensoryy[i,j]
#          tempJeigs = np.linalg.eig(tempJ)
#          if (tempJeigs[0][0] > tempJeigs[0][1]):
#             Jtensoreig[0][i][j] = tempJeigs[1][0][0]
#             Jtensoreig[1][i][j] = tempJeigs[1][0][1]
#          else:
#             Jtensoreig[0][i][j] = tempJeigs[1][1][0]
#             Jtensoreig[1][i][j] = tempJeigs[1][1][1]
#          Jmag[i][j] = np.sqrt(tempJeigs[0][0]+tempJeigs[0][1]) 
#    @endcode
#  
#    Compute the gradient angle from the elements of the gradient vector.
#    @code 
#    theta = np.array((M,N),'f') 
#    theta = np.arctan(Jtensoreig[1,:,:]/Jtensoreig[0,:,:])+np.pi/2
#    @endcode
# 
#    Write the estimated gradient orientation to the RSF File specified by target.
#    @code
#    output = sf.Output(target)
# 
#    output.put("n1",N)
#    output.put("n2",M)
#    output.write(theta)
#    @endcode
# 
#    End the current function.
#    @code
#    End()
#    @endcode
# 
# Finally, export the OrientationEstimation function so that it can be used by other programs.
# @code
# __all__ = ['OrientationEstimation']
# from slimproj_core.builders.CreateBuilders import add_to_slim_env
# add_to_slim_env("OrientationEstimation",OrientationEstimation)
# @endcode
# 

#!/usr/bin/env python 
#"""
#DESCRIPTION:
#   Calculate gradient orientation of input image with a method robust to noise
#   using the Linear Structure Tensor
#
#PARAMETERS:
#   datafile: The noisy input for which we desire to calculate the gradient directions
#   Jx: x-component of gradient of input image 
#   Jy: y-component of gradient of input image
#   Jmag: Gradient magnitude image
#   confthetafile: Filename where confidence in orientation estimation is stored
#
#REQUIREMENTS:
#   - Madagascar
#   - SLIMpy
#
#Author:
#   Reza Shahidi
#	Seismic Laboratory for Imaging and Modeling (SLIM)
#	Department of Earth & Ocean Sciences (EOS)
#	University of British Columbia (UBC)
#
#You may use this code only under the conditions and terms of the
#license contained in the file LICENSE provided with this source
#code. If you do not agree to these terms you may not use this
#software.
#"""
#

usage="\nOrientationEstimation.py target=theta.rsf datafile=data.rsf" 

from SLIMpy import *
import numpy as np
import rsf as sf
from slimproj import *

# Set default values
defaults = {
'inputgrad_filename':'marmousi_grad.rsf',     #Input data as y
}

def new_average_bldr( vectors ):
    """
    use our new averaging operator
    """
    z = vectors[0]
    filtersize = vectors[1]
    averagefilterx = np.ones((1,filtersize))/filtersize
    averagefiltery = np.ones((1,filtersize))/filtersize

    (M,N) = z.shape
    x = np.zeros((M,N),'f')
    for i in range(0,M):
       x[i,:] = np.convolve(z[i,:],np.ones(filtersize)/filtersize,mode='same')

    for j in range(0,N):
       x[:,j] = np.convolve(x[:,j],np.ones(filtersize)/filtersize,mode='same') 

    return x

def OrientationEstimation( target, source, env ): 
   """
   Takes the image specified by source, and writes the gradient direction angle
   for the source image (lying between -pi and pi) to the RSF file specified by target.
   """

   # Read in file for which we want to compute the gradient direction
   inputfilename = source[0]
   inputimage = sf.Input(source[0])

   # Number of rows and columns in image 
   M = inputimage.int("n2")
   N = inputimage.int("n1")
 
   # Read in previously computed partial derivatives of input with noise added
   # Partial derivative in x direction
   noisyinputgradx_filename = source[1]
   noisyinputgradxrsf = sf.Input(noisyinputgradx_filename)
   Jx = np.zeros((M,N),'f')
   noisyinputgradxrsf.read(Jx) 

   # Partial derivative in y direction
   noisyinputgrady_filename = source[2]
   noisyinputgradyrsf = sf.Input(noisyinputgrady_filename)
   Jy = np.zeros((M,N),'f')
   noisyinputgradyrsf.read(Jy) 

   Jtensorxx = np.zeros((M,N))
   Jtensorxy = np.zeros((M,N))
   Jtensoryy = np.zeros((M,N))

   # Form structure tensor elements
   Jtensorxx = Jx*Jx
   Jtensorxy = Jx*Jy
   Jtensoryy = Jy*Jy

   # Apply 5x5 averaging window on each of the computed structure tensor elements
   averagefilterwidth = 5 
   Jtensorxx = new_average_bldr([Jtensorxx,averagefilterwidth])
   Jtensorxy = new_average_bldr([Jtensorxy,averagefilterwidth])
   Jtensoryy = new_average_bldr([Jtensoryy,averagefilterwidth])
  
   # Estimated gradient orientation is in the same direction
   # as the eigenvector corresponding to the largest eigenvalue
   # of the structure tensor  
   Jtensoreig = np.zeros((2,M,N),'f')
   Jmag = np.zeros((M,N),'f')
   tempJ = np.zeros((2,2),'f')
   for i in range(0,M):
      for j in range(0,N):

         # Form 2x2 Structure Tensor for Current Pixel
         tempJ[0,0] = Jtensorxx[i,j]
         tempJ[0,1] = Jtensorxy[i,j]
         tempJ[1,0] = Jtensorxy[i,j]
         tempJ[1,1] = Jtensoryy[i,j]

         # Find Eigenvalues of Structure Tensor
         tempJeigs = np.linalg.eig(tempJ)

         # Choose Eigenvector of Structure Tensor Corresponding to Larger Eigenvalue
         if (tempJeigs[0][0] > tempJeigs[0][1]):
            Jtensoreig[0][i][j] = tempJeigs[1][0][0]
            Jtensoreig[1][i][j] = tempJeigs[1][0][1]
         else:
            Jtensoreig[0][i][j] = tempJeigs[1][1][0]
            Jtensoreig[1][i][j] = tempJeigs[1][1][1]

         # Estimated Gradient Magnitude
         Jmag[i][j] = np.sqrt(tempJeigs[0][0]+tempJeigs[0][1]) 
  
   theta = np.array((M,N),'f') 

   # Theta is the estimated gradient orientation
   theta = np.arctan(Jtensoreig[1,:,:]/Jtensoreig[0,:,:])

   # Write out theta to file
   output = sf.Output(target)

   # Write the original multiples to RSF File
   output.put("n1",N)
   output.put("n2",M)
   output.write(theta)

   End()

__all__ = ['OrientationEstimation']
from slimproj_core.builders.CreateBuilders import add_to_slim_env
add_to_slim_env("OrientationEstimation",OrientationEstimation)
