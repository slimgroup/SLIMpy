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
Set of algorithms for seismic data processing.
'''
import os
import Steppers
import MultiPipe

def GenThreshLandweber(ForwardOper, AdjointOper,
	lambdaMax, lambdaMin, lambdaN, InnerN,
	DataIn, DataOut,
	TMPDIR=None, VERBOSE=False):
	'''
	Generalized Thresholded Landweber method using RSF commands.

	Requires:
		RSFROOT environment has to be specified, such that $RSFROOT/bin is the path
		to RSF commands. SLIM python modules: Steppers and MultiPipe
	Parameters:
		ForwardOper: list of strings containing complete definition of forward operator
		AdjointOper: list of strings containing complete definition of adjoint operator
			(For both above, each string has to be a complete RSF command
			working on the stdin and stdout.)
		lambdaMax: maximum lambda
		lambdaMin: minimum lambda
		lambdaN: number of steps in iteration from lambdaMax to lambdaMin
		InnerN: number of iterations for any lambda
		DataIn: RSF file with input data
		DataOut: RSF file for output data
	Keyword parameters (optional):
		TMPDIR: temporary directory (system default if not specified)
		VERBOSE: verbose if set to True
	Returns:
		0 if successful, positive number otherwise
	Notes:
		The function generates a number of temporary files that will have to be cleaned
		manually if it is forced to stop before it finishes.
	Bugs:
		None so far, but keep trying.
		It is not fool-proof. So, you have to know what you are doing;
		i.e., how to use RSF.
	'''

	if VERBOSE: print '%%%%%% into GenThreshLandweber'
	err = 0

	# check if RSFROOT exists
	try: RSFbin = os.environ['RSFROOT']+'/bin/'
	except:
		print 'FATAL: missing RSFROOT environment'
		return 1
	if VERBOSE: print 'RSF binaries in:',RSFbin

	# temporary files
	x = os.tempnam(TMPDIR,'x.')+'.rsf'
	xTmp = os.tempnam(TMPDIR,'xTmp.')+'.rsf'
	Coefs = os.tempnam(TMPDIR,'Coefs.')+'.rsf'
	if VERBOSE: print 'Temporary files:',x,xTmp,Coefs

	# define pipes
	MathOper = [RSFbin+'sfmath x=%s output="x-input"' % (Coefs),
			RSFbin+'sfmath x=%s output="input+x"' % (x)]
	pipeAFM = AdjointOper+ForwardOper+MathOper
	pipeF = ForwardOper
	pipeStmpl = [RSFbin+'sfsoftth thr=LAMBDA']
	pipeA = AdjointOper
	if VERBOSE:
		print 'Forward Operator:',pipeF
		print 'Adjoint Operator:',pipeA
		print 'Adjoint+Forward+Math:',pipeAFM
		print 'Soft Thresholding:',pipeStmpl
		print

	# set error code to good
	err = 0

	# prepare first guess
	if VERBOSE:
		print 'Initial guess:'
		print '<',DataIn,pipeF,'>',Coefs
	err += MultiPipe.FileInOut(DataIn,pipeF,Coefs)
	pipeS = []
	for line in pipeStmpl:
		dummy = line.replace('LAMBDA',str(lambdaMax))
		pipeS.append(dummy)
	if VERBOSE: print '<',Coefs,pipeS,'>',x
	err += MultiPipe.FileInOut(Coefs,pipeS,x)

	# execute loops
	if VERBOSE: print 'Executing loops:'
	for i in Steppers.OneDimStepN(lambdaMax,lambdaMin,lambdaN):
		for j in Steppers.OneDimStep1(1,InnerN):
			if VERBOSE:
				print ' lambda=',i,'j=',j
				print '<',x,pipeAFM,'>',xTmp
			err += MultiPipe.FileInOut(x,pipeAFM,xTmp)
			pipeS = []
			for line in pipeStmpl:
				dummy = line.replace('LAMBDA',str(i))
				pipeS.append(dummy)
			if VERBOSE: print '<',xTmp,pipeS,'>',x
			err += MultiPipe.FileInOut(xTmp,pipeS,x)

	if VERBOSE:
		print 'Final results:'
		print '<',x,pipeA,'>',DataOut
	err += MultiPipe.FileInOut(x,pipeA,DataOut)

	# remove temporary file
	try: os.remove(xTmp)
	except: pass
	try: os.remove(xTmp+'@')
	except: pass
	try: os.remove(Coefs)
	except: pass
	try: os.remove(Coefs+'@')
	except: pass
	try: os.remove(x)
	except: pass
	try: os.remove(x+'@')
	except: pass
	if VERBOSE: print
	if VERBOSE: print '%%%%%% out off GenThreshLandweber with error code=',err

	return err
