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
Module to execute a pipe chain.

Execute 'python /path_to_module/MultiPipe.py' to see the examples.
'''

import pipes

VERBOSE=False

def FileIn(fin,cmds):
	'''
	Function to process a file through a shell pipe.
	FileIn(fin,cmds)
		fin - string holding name of the input file
		cmds - list of strings representing commands in the pipe
	Returns 0 if successful.
	'''
	cnt = len(cmds)
	strm = cnt*['--']
	pip = []
	t=pipes.Template()
	if cnt:
		strm[cnt-1]=strm[cnt-1][0]+'.'
		for i in range(cnt):
			pip.append([cmds[i],strm[i]])
			t.append(cmds[i],strm[i])
	if VERBOSE: print pip,'<',fin
	return t.copy(fin,'')

def FileOut(cmds,fout):
	'''
	Function to save the output from a shell pipe to a file.
	FileOut(cmds,fout)
		cmds - list of strings representing commands in the pipe
		fout - string holding name of the output file
	Returns 0 if successful.
	'''
	cnt = len(cmds)
	strm = cnt*['--']
	pip = []
	t=pipes.Template()
	if cnt:
		strm[0] = '.'+strm[0][1]
		pip.append([cmds[0],strm[0]])
		t.prepend(cmds[0],strm[0])
		for i in range(1,cnt):
			pip.append([cmds[i],strm[i]])
			t.append(cmds[i],strm[i])
	if VERBOSE: print pip,'>',fout
	return t.copy('',fout)

def FileInOut(fin,cmds,fout):
	'''
	Function to process a file through a shell pipe and save the output to another file.
	FileInOut(fin,cmds,fout)
		fin - string holding name of the input file
		cmds - list of strings representing commands in the pipe
		fout - string holding name of the output file
	Returns 0 if successful.
	'''
	cnt = len(cmds)
	strm = cnt*['--']
	pip = []
	t=pipes.Template()
	for i in range(cnt):
		pip.append([cmds[i],strm[i]])
		t.append(cmds[i],strm[i])
	if VERBOSE: print pip,'<',fin,'>',fout
	return t.copy(fin,fout)

##########################
if __name__ == '__main__':
	print __doc__

	print 80*'-'
	print FileOut.__doc__
	print "FileOut(['ps -xl','tail -7','head -5'],'/tmp/ps-xl0')"
	FileOut(['ps -xl','tail -7','head -5'],'/tmp/ps-xl0')
	print 'Result:\n',open('/tmp/ps-xl0').read()

	print 80*'-'
	print FileInOut.__doc__
	print "FileInOut('/tmp/ps-xl0',['head -3','tail -1'],'/tmp/ps-xl1')"
	FileInOut('/tmp/ps-xl0',['head -3','tail -1'],'/tmp/ps-xl1')
	print 'Result:\n',open('/tmp/ps-xl1').read()

	print 80*'-'
	print FileIn.__doc__
	print "FileIn('/tmp/ps-xl0',['wc'])"
	print 'Result:\n'
	FileIn('/tmp/ps-xl0',['wc'])

	print 80*'-'
