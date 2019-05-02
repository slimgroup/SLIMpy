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

#
#"""
#
#
#"""
#
#
#from numpy import ndarray,array
#from slimpy_base.Core.User.linop.linear_operator import linearop
#
#class aug_matrix(object):
#	"""
#	the augmented matrix class is used to append linear operators
#	or vectors togeter to create a larger vector or operator
#	
#	"""
#	def __init__(self,x):
#		
#		self.x = array(x)
#		
#		self.N = len(self.x[0])
#		self.M = len(self.x)
#		
#	
#	
#	def transp(self):
#		return aug_matrix( self.x.transpose() )
#		
#	def __mul__(self,other):
#		return aug_matrix( self.x.__mul__(other) )
#	
#	def __add__(self,other):
#		return aug_matrix( self.x.__add__(other) )
#	
#	def __radd__(self,other):
#		return aug_matrix( self.x.__radd__(other) )
#	def __sub__(self,other):
#		return aug_matrix( self.x.__sub__(other) )
#	def __rsub__(self,other):
#		return aug_matrix( self.x.__rsub__(other) )
#	def __pow__(self,other):
#		return aug_matrix( self.x.__pow__(other) )
#	
#	def __abs__(self):
#		return aug_matrix( self.x.__abs__() )		
#
#	def __len__(self):
#		return aug_matrix( self.x.__len__() )
#
#
#class aug_oper(aug_matrix,linearop ):
#	"""
#	The reason for sub classing the aug_oper is to define how it acts when it is applied. ie. the '*' symbol.
#	aug_oper overloads '*' to perform matrix multiplication on the other aug_matrix
#	"""
#	def __init__(self,x):
#		aug_matrix.__init__(self,x)
#	def __mul__(self,other):
#		if not isinstance(other, aug_matrix):
#			return self.elementop(other,'__mul__')
#			
#		if self.N is not other.M:
#			raise Exception
#
#		result = aug_matrix.create(other.N,self.M)
#		for i in range(0,other.N):
#			for j in range(0,self.M):
#				result[j][i] = __sum(__prod( self.row(j), other.coloum(i) ))
#				
#		return aug_matrix(result)
#
#class aug_vec(aug_matrix):
#	"""
#	The default * operation for aug_vec is to perform an element wise operation on the vectors
#	contained within.
#	"""
#	def __init__(self,x):
#		aug_matrix.__init__(self,x)
#	
#
#		
#
#	
#	
