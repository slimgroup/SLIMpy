
"""
Contains the N-D contourlet transform.
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

from slimpy_base.Core.User.linop.rclinOp import linearop_r as __LR

_surf__LR = __LR

## Surfacelet Transform
# @ingroup linop
class surf(__LR):
    """
    The N-D Contourlet Transformation--Surfacelet.
    """
    name = 'surf'
    def __init__(self,inSpace,adj=False,Pyr_Level=2,**kparams):
        """
        Only Pyr_Level, K, lambda, beta, mSize, bo, dir_filter allowed.
         Constructor
         @param inSpace space instance
         @param adj create adjoint transform
         @param Pyr_Level ???
        """
        for key in kparams:
            if not key in ['Pyr_Level','K','lamb','beta','mSize','bo','dir_filter']:
                raise TypeError,"Invalid Paramter, only Pyr_Level, K, lamb, beta, mSize, bo, dir_filter allowed."
        
        kparams.update( adj=adj, Pyr_Level=Pyr_Level )
            
        __LR.__init__(self,inSpace,**kparams)

    def inv(self):
        """
        Apply the INVERSE version of the sfsurf
        """
        t = self.copy()
        t.kparams['inv'] = 'y'
        return t.adj()
    
