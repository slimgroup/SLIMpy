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

from linearops.linear_ops import *
from linearops.transforms import *
from linearops.linear_alg import *
from linearops.fft import *
from linearops.wavelets import *
from linearops.curvelets import *
from linearops.contourlets import *
from linearops.MatMult import *
from linearops.ScatterOperator import Scatter
from linearops.mpi_linops import *

from linearops.operator_functions import Norm, MinVelConst, is_linear_op
from linearops.operator_functions import Normalize
