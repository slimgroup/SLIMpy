__copyright__ = """
Copyright 2008 Henryk Modzelewski
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

'''
Module with number of iterable objects (steppers).

Execute 'python /path_to_module/Steppers.py' to see the examples.

NOTE: Subclassing those objects was not tested.
'''

def Sign (a):
	'''
	Module-internal sign function.
		Returns sign(a).
	'''
	if a >= 0: return 1
	else: return -1

def SignDiff (a,b):
	'''
	Module-internal sign function.
		Returns sign(b-a).
	'''
	if b >= a: return 1
	else: return -1

class OneDimStep1:
	'''
	One-dimensional stepper w/ abs(increment)=1.
	Object holds integer values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,start,stop):
		self.__sign = SignDiff(start,stop)
		self.__start = start
		self.__val = -1
		self.__end = (stop - start) * self.__sign
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		index = self.__start + self.__val * self.__sign
		return index

class OneDimStepF:
	'''
	One-dimensional stepper w/ float abs(increment)
	Object holds float values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,start,stop,incr):
		self.__sign = SignDiff(start,stop)
		self.__start = start
		self.__incr = abs(incr)
		self.__val = -1
		self.__end = int(float(stop - start)/float(abs(incr))) * self.__sign
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		index = self.__start + self.__val * self.__incr * self.__sign
		return index

class OneDimStepN:
	'''
	One-dimensional stepper w/ fixed number of elements
	Object holds float values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,start,stop,cnt):
		self.__sign = SignDiff(start,stop)
		self.__start = start
		self.__incr = abs(float(stop-start)/float(abs(cnt)-1))
		self.__val = -1
		self.__end = abs(cnt)-1
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		index = self.__start + self.__val * self.__incr * self.__sign
		return index

class MultiDimStep1:
	'''
	Multi-dimensional stepper w/ abs(increments)=1.
	Object holds lists of integer values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,limits):
		self.__lngth = len(limits)
		self.__starts = []
		self.__signs = []
		self.__sizes = []
		for limit in limits:
			if len(limit) != 2:
				print 'Fatal error: wrong limits', limit, 'in', limits
				raise TypeError
				return
			self.__starts.append(limit[0])
			self.__signs.append(SignDiff(limit[0],limit[1]))
			self.__sizes.append(SignDiff(limit[0],limit[1])*(limit[1]-limit[0])+1)
		self.__val = -1
		self.__end = 1
		for size in self.__sizes:
			self.__end *= size
		self.__end -= 1
		self.__divs = self.__sizes[1:]
		for i in range(self.__lngth-3,-1,-1):
			self.__divs[i]*=self.__divs[i+1]
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		indxs = []
		val = self.__val
		for div in self.__divs:
			indx = val / div
			indxs.append(indx)
			val  = val % div
		indxs.append(val)
		for i in range(0,self.__lngth):
			indxs[i] = self.__starts[i] + indxs[i] * self.__signs[i]
		return indxs

class MultiDimStepF:
	'''
	Multi-dimensional stepper w/ float abs(increments).
	Object holds lists of float values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,limits):
		self.__lngth = len(limits)
		self.__starts = []
		self.__signs = []
		self.__incrs = []
		self.__sizes = []
		for limit in limits:
			if len(limit) != 3:
				print 'Fatal error: wrong limits', limit, 'in', limits
				raise TypeError
				return
			self.__starts.append(limit[0])
			self.__signs.append(SignDiff(limit[0],limit[1]))
			self.__incrs.append(abs(limit[2]))
			self.__sizes.append(SignDiff(limit[0],limit[1])*int(float(limit[1]-limit[0])/limit[2])+1)
#		print self.__lngth, self.__starts, self.__signs, self.__sizes
		self.__val = -1
		self.__end = 1
		for size in self.__sizes:
			self.__end *= size
		self.__end -= 1
		self.__divs = self.__sizes[1:]
		for i in range(self.__lngth-3,-1,-1):
			self.__divs[i]*=self.__divs[i+1]
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		indxs = []
		val = self.__val
		for div in self.__divs:
			indx = val / div
			indxs.append(indx)
			val  = val % div
		indxs.append(val)
		for i in range(0,self.__lngth):
			indxs[i] = self.__starts[i] + indxs[i] * self.__incrs[i] * self.__signs[i]
		return indxs

class MultiDimStepN:
	'''
	Multi-dimensional stepper w/ fixed number of elements.
	Object holds lists of float values to be used only in
	'for * in [Stepper]:' loop.
	'''
	def __init__(self,limits):
		self.__lngth = len(limits)
		self.__starts = []
		self.__signs = []
		self.__incrs = []
		self.__sizes = []
		for limit in limits:
			if len(limit) != 3:
				print 'Fatal error: wrong limits', limit, 'in', limits
				raise TypeError
				return
			self.__starts.append(limit[0])
			self.__signs.append(SignDiff(limit[0],limit[1]))
			self.__incrs.append(abs(float(limit[1]-limit[0])/float(abs(limit[2])-1)))
			self.__sizes.append(abs(limit[2]))
		self.__val = -1
		self.__end = 1
		for size in self.__sizes:
			self.__end *= size
		self.__end -= 1
		self.__divs = self.__sizes[1:]
		for i in range(self.__lngth-3,-1,-1):
			self.__divs[i]*=self.__divs[i+1]
	def __iter__(self):
		return self
	def next(self):
		if self.__val == self.__end:
			raise StopIteration
		self.__val += 1
		indxs = []
		val = self.__val
		for div in self.__divs:
			indx = val / div
			indxs.append(indx)
			val  = val % div
		indxs.append(val)
		for i in range(0,self.__lngth):
			indxs[i] = self.__starts[i] + indxs[i] * self.__incrs[i] * self.__signs[i]
		return indxs

##########################
if __name__ == '__main__':
	print __doc__

	print 80*'-'
	print OneDimStep1.__doc__
	print 'Example: OneDimStep1(',0,',',-3,')'
	print 'iterates through:'
	Ns = OneDimStep1(0,-3)
	for n in Ns:
		print '\t',n

	print 80*'-'
	print OneDimStepF.__doc__
	print 'Example: OneDimStepF(',0.1,',',0.35,',',0.1,')'
	print 'iterates through:'
	Ns = OneDimStepF(0.1,0.35,0.1)
	for n in Ns:
		print '\t',n

	print 80*'-'
	print OneDimStepN.__doc__
	print 'Example: OneDimStepN(',0.1,',',0.35,',',6,')'
	print 'iterates through:'
	Ns = OneDimStepN(0.1,0.35,6)
	for n in Ns:
		print '\t',n

	print 80*'-'
	print MultiDimStep1.__doc__
	limits = [[0,1],[4,2]]
	print 'Example: MultiDimStep1(',limits,')'
	print 'iterates through:'
	NNs = MultiDimStep1(limits)
	for nn in NNs:
		print '\t',nn

	print 80*'-'
	print MultiDimStepF.__doc__
	limits = [[0,1,0.5],[4,2,0.6]]
	print 'Example: MultiDimStepF(',limits,')'
	print 'iterates through:'
	NNs = MultiDimStepF(limits)
	for nn in NNs:
		print '\t',nn

	print 80*'-'
	print MultiDimStepN.__doc__
	limits = [[0,1,3],[4,2,2]]
	print 'Example: MultiDimStepN(',limits,')'
	print 'iterates through:'
	NNs = MultiDimStepN(limits)
	for nn in NNs:
		print '\t',nn

	print 80*'-'
