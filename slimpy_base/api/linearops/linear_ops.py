"""
Generic Single Linear operator functions
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


from slimpy_base.Core.User.linop.rclinOp import linearop_r as LinearOperatorStruct
from slimpy_base.Core.User.linop.linear_operator import Identity
from slimpy_base.Core.Interface.node import Source
import re

## Pad the underlying image of a vector 
## @ingroup linop
class pad( LinearOperatorStruct ):
    """
    P = pad( space, beg#, end# n# , n#out,adj, )
    Pad a dataset with zeros
    """
    
    def __new__(cls, *inSpace, **kparams):
        
        if inSpace or kparams:
            all_zeros = True
            for nN, val in kparams.iteritems():
                if nN.startswith('end') or nN.startswith('beg'):
                    if val != 0:
                        all_zeros = False
                        break
                    
            if all_zeros:
                return Identity(inSpace[0])
            
        return LinearOperatorStruct.__new__( cls, *inSpace, **kparams )
    
    name = "pad"
    
    def __init__(self,inSpace,adj=False,**kparams):
        """
        nN is the number of N's that are given to the functions.
        Note: n1,n2 and n1out,n2out are the same.  beg1.end1 - beg2,end2 adds padding to the dataset.
        """
        
        for nN in kparams:
            if not re.match('(^beg\d+$|^end\d+$|^n\d+$|^adj$|^n\d+out$)',nN):
                raise TypeError,"Invalid Parameter, must be n# or n#out, beg# or end#."
        
#        kparams['adj'] = False
        LinearOperatorStruct.__init__(self,inSpace,adj=adj,**kparams)

## Taper image 
# @ingroup linop
class Taper( LinearOperatorStruct ):
    """
    Cos Taper image on all sides with 2*eps
    """
    name = 'taper'
    def __init__(self,domain,eps,adj=False):
        """
        Initialize the operator.
        """
        LinearOperatorStruct.__init__(self,domain,adj=False,eps=eps)
    
## Cos Tapering
# @ingroup linop
class costaper( LinearOperatorStruct ):
    """
    Cos Tapering
    """
    name = "costaper"
    def __init__(self,inSpace,**kparams):
        """
        Initialize the operator.
        """
        LinearOperatorStruct.__init__(self,inSpace,adj=False,**kparams)
        
        
## @ingroup linop
class dipfilter( LinearOperatorStruct ):
    """
    Dip Filter operation, assume the data is in the Fourier Domain.
    """
    name = "dipfilter"
    def __init__( self, inSpace, ang1=None, ang2=None, ang3=None, ang4=None, ang=None, angle='n', dim=2, adj=False, **kparams ):
        """
        Takes parameters dim=[2/3], pass=[y/n], ang[1-4]=
        """
        for nN in kparams:
            if not re.match( '(^v\d*$|^pass$)', nN ):
                raise TypeError, "Invalid Parameter, must be v# or pass."
        
        if ang != None:
            ang = 90-ang
            kparams = dict( kparams, 
                        adj=adj, 
                        angle=angle, 
                        dim=dim,
                        ang1=-ang, 
                        ang2=-0.9*ang, 
                        ang3=0.9*ang, 
                        ang4=ang )
        else:
            kparams = dict( kparams, 
                        adj=adj, 
                        angle=angle, 
                        dim=dim,
                        ang1=ang1, 
                        ang2=ang2, 
                        ang3=ang3, 
                        ang4=ang4 )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )
        

## Perform a simulation and migration
# @ingroup linop
class mig( LinearOperatorStruct ):
    """
    R/T Migration-Demigration
    Perform a simulation and migration of the RSF mig operator.
    """
    name = "mig"
    def __init__( self, inSpace, dataSpace, que='y', adj=False, **kparams ):
        """
        inp and out are the input and output's of the file.
        The que='n' param sets the default mig script to force run in environment.
        """
        
        # This parameter sets the default mig script to force run in environment.
        kparams.update( modelSpace=inSpace, dataSpace=dataSpace, adj=adj, que=que )
        
        LinearOperatorStruct.__init__( self, inSpace, **kparams )


## @ingroup linop
class multpred( LinearOperatorStruct ):
    """
    M = multpred( inSpace, filt=1, input=None, adj=False )
    Multiple Prediction Program of Deli's
    """
    name = "multpred"
    
    __block_diagonal__ = True
    
    def __init__( self, inSpace, filt=1, input=None, adj=0, **kparams ):
        """
        Takes filt and input as paramaters. Input as source so it creates it.
        """
        kparams.update( filt=filt, adj=adj )
        
        if filt==1:
            assert input is not None
            kparams.update( input=Source(input.getContainer()) )
    
        LinearOperatorStruct.__init__( self, inSpace, **kparams )
    

