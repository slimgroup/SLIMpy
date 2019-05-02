"""
Contains the N-D contourlet transform.
These are the Surfacelet helper functions. 
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

import re

def surfSpaceChange( command, space, *spaces ):
    """
    Applies the forward space change. Converts it to a Linear
    array of values.  Works in N-D
    """
    nDim = 0
    nTotal = 1
    for cmd in space.keys():
        if re.match( '^n\d+$', cmd ):
            nTotal = nTotal * space[cmd]
            space[cmd+'_orig'] = space[cmd]
            space[cmd] = 1
            nDim += 1
    
    #Redundancy Factor for Surfaclets.
    nRed = 4.25
    if command['Pyr_Level'] == 2 and nDim == 2: nRed = 4.25
    elif command['Pyr_Level'] == 3 and nDim == 2: nRed = 4.5625
    elif command['Pyr_Level'] == 4 and nDim == 2: nRed = 4.640625
    elif command['Pyr_Level'] == 5 and nDim == 2: nRed = 4.66015625
    elif command['Pyr_Level'] == 2 and nDim == 3: nRed = 6.125
    elif command['Pyr_Level'] == 3 and nDim == 3: nRed = 6.390625
    elif command['Pyr_Level'] == 4 and nDim == 3: nRed = 6.423828125
    elif command['Pyr_Level'] == 5 and nDim == 3: nRed = 6.427978515625
    
    space['n1'] = nTotal * nRed

def surfInvSpaceChange( command, space, *spaces ):
    """
    Applies the reverse space change.  This takes into concideration
    the adjoint and the inverse operators.  Works in N-D.
    """
    for cmd in space.keys():
        if re.match( '^n\d+$', cmd ):
            space[cmd] = space[cmd+'_orig']
