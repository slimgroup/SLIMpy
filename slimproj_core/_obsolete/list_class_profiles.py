"""
action for latex doc
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


import pickle
from ListClassesAndMethods import makeList
from SCons.Script import Action

def func_builder(target,source,env):

    FORMAT= 'LaTeX'
#    ContentOut = None
#    DirOut = None
    FileIn = str(source[0])
#    FileOut = open( str(target[0]) ,'w' )
    pickle_file = open(FileIn)
    Document = pickle.load( pickle_file )
    pickle_file.close()
    
#    makeList(FORMAT, ContentOut, Document, DirOut, FileOut)
    makeList(Document, str(target[0]), FORMAT)
    
    return
    
func_builder = Action( func_builder, "Build Latex From Profile [ ${SOURCE.file} --> ${TARGET.file} ]")


