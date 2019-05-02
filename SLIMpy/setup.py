
"""
init file packags functions for ease of end user
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

from slimpy_base.setup.cmndLineParse import SlimOptionParser
from slimpy_base.setup.ParseEnv import parse_env
from slimpy_base.Environment.InstanceManager import InstanceManager as _im


End = _im().End
Execute = _im().Execute
 
option_parser = SlimOptionParser( )
parse_args = option_parser.parse

Defaults = option_parser.Defaults
Types = option_parser.Types
Parameters = option_parser.Parameters

check_required = option_parser.check_required
