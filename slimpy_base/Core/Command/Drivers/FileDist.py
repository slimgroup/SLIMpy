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

import random

def PrintSortedHash(name,table):
	'''
	Prints hash elements ordered by sorted keys.
	'''
	print name+':'
	keys=table.keys()
	keys.sort()
	for key in keys:
		print '\t',key,table[key]

def even_dist(nodes,files,VERBOSE=False):
	'''
	DESCRIPTION:
		even_dist finds unique node to file assignment
		and attempts to minimize the number of necessary
		copy operations.

	TAKES:
		nodes: list of nodes
		files: list of data container objects
	RETURNS:
		the tuple ordered as files with either:
			target - if file is at the right position
			(source,target) - if file is to be copied
				from source to target
	'''
	if VERBOSE: print '\n* Into even_dist'

	nfiles=len(files)
	assert(nfiles==len(nodes))
	unodes = list(set(nodes))
	unodes.sort()
	unodes = tuple(unodes)
	unlen = len(unodes)
	if VERBOSE: print 'unodes: ',unlen,unodes

	ncount = {}
	for node in unodes: ncount[node] = nodes.count(node)
	npool = {}
	fpool = {}
	for file in files:
		for node in file.nodenames:
			if npool.has_key(node): npool[node].append(file.data)
			else: npool[node]=[file.data]
			if fpool.has_key(file.data): fpool[file.data].append(node)
			else: fpool[file.data]=[node]
	for key in npool: npool[key].sort()
	for key in fpool: fpool[key].sort()
	if VERBOSE:
		PrintSortedHash('ncount',ncount)
		PrintSortedHash('npool',npool)
		PrintSortedHash('fpool',fpool)

	copy = {}
	ndone = {}
	for elm in unodes: ndone[elm]=[]

	# find unique files
	if VERBOSE: print '\n* Finding unique files'
	for i in xrange(unlen):
		if not npool.has_key(unodes[i]): continue
		dummy = set(npool[unodes[i]])
		for j in xrange(unlen):
			if j!=i and npool.has_key(unodes[j]): dummy=dummy-set(npool[unodes[j]])
		dummy = list(dummy)
		dummy = dummy[:ncount[unodes[i]]]
		for elm in dummy:
			ndone[unodes[i]].append(elm)
			ncount[unodes[i]] = ncount[unodes[i]] - 1
			copy[elm]=(None,unodes[i])
			for key in npool:
				if npool[key].count(elm): npool[key].remove(elm)
			del fpool[elm]
	if VERBOSE:
		PrintSortedHash('ncount',ncount)
		PrintSortedHash('npool',npool)
		PrintSortedHash('fpool',fpool)
		PrintSortedHash('ndone',ndone)
		PrintSortedHash('copy',copy)

	# find files already on the owner node
	if VERBOSE: print '\n* Finding files already on the owner node'
	for i in xrange(unlen):
		if not npool.has_key(unodes[i]): continue
		dummy = npool[unodes[i]][:ncount[unodes[i]]]
		for elm in dummy:
			ndone[unodes[i]].append(elm)
			ncount[unodes[i]] = ncount[unodes[i]] - 1
			copy[elm]=(None,unodes[i])
			for key in npool:
				if npool[key].count(elm): npool[key].remove(elm)
			del fpool[elm]
		ndone[unodes[i]].sort()
	if VERBOSE:
		PrintSortedHash('ncount',ncount)
		PrintSortedHash('npool',npool)
		PrintSortedHash('fpool',fpool)
		PrintSortedHash('ndone',ndone)
		PrintSortedHash('copy',copy)

	if VERBOSE: print '\n* Find files to be copied'
	for i in xrange(unlen):
		while ncount[unodes[i]] > 0:
			fdummies = fpool.keys()
			fdummy = random.sample(fdummies,1)[0]
			ndummies = fpool[fdummy]
			ndummy = random.sample(ndummies,1)[0]
			ndone[unodes[i]].append(fdummy)
			ncount[unodes[i]]=ncount[unodes[i]]-1
			copy[fdummy]=(ndummy,unodes[i])
			for key in npool:
				if npool[key].count(fdummy): npool[key].remove(fdummy)
			del fpool[fdummy]
	if VERBOSE:
		PrintSortedHash('ncount',ncount)
		PrintSortedHash('npool',npool)
		PrintSortedHash('fpool',fpool)
		PrintSortedHash('ndone',ndone)
		PrintSortedHash('copy',copy)

	# check uniqueness
	if VERBOSE: print '\n* Check uniqueness'
	for i in xrange(unlen):
		dummy = set(ndone[unodes[i]])
		dummies = set()
		for j in xrange(unlen):
			if j!=i: dummies=dummies|set(ndone[unodes[j]])
		unique = dummies&dummy
		if len(unique) > 0: raise 'Nonounique File Assignment for', (unodes[i],list(unique))

	# check existence
	if VERBOSE: print '\n* Check Existence'
	for idx in xrange(nfiles):
		file = files[idx].data
		if not copy.has_key(file): raise 'Unresolved File@Node Assignment', file
		if copy[file][0]:
			# exists at the source
			if list(files[idx].nodenames).count(copy[file][0]):
				if VERBOSE: print file, '->', copy[file], ': source OK'
			else:
				if VERBOSE: print file, '->', copy[file], ': source error'
				raise 'Nonexistent File at the source', (file,copy[file])
			# already at the target
			if list(files[idx].nodenames).count(copy[file][1]):
				if VERBOSE: print file, '->', copy[file], ': target error'
				raise 'Obsolete File copy', (file,copy[file])
			else:
				if VERBOSE: print file, '->', copy[file], ': target OK'
		else:
			# exists at the target
			if list(files[idx].nodenames).count(copy[file][1]):
				if VERBOSE: print file, '->', copy[file], ': target OK'
			else:
				if VERBOSE: print file, '->', copy[file], ': target error'
				raise 'Nonexistent File at the target', (file,copy[file])

	# create return result
	if VERBOSE: print '\n* Make result:'
	result = []
	for idx in xrange(nfiles):
		file = files[idx].data
		if copy[file][0]: result.append(copy[file])
		else: result.append(copy[file][1])

	if VERBOSE: print '\n* Done even_dist\n'
	return tuple(result)

