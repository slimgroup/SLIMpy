"""
Helper functions that can produce a list of package names and the html equivalent
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

from os import walk, system
from os.path import dirname, join, split, sep
import slimpy_base



slfile = dirname( slimpy_base.__file__ )
w = walk( slfile )
fpath = split( slfile )[0] 

#pydoc = WhereIs('pydoc')

def helper():
    """
    Genorator function that yields a tuple of 
    """
    for dir , nextdirs , files in w:
        if ".svn" not in dir and 'test' not in dir and 'Plugin' not in dir:
            
            imp = dir.replace( fpath, "" )
            ldir = imp.split( sep )
            
            #yield ".".join(ldir)
            
            for f in files:
                if f.endswith( ".py" ):
                    file = join( dir+[f] )
                    html = ".".join( ldir+[f[:-3] + ".html"] )
                    imp = ".".join( ldir+[f[:-3]] )
                    yield file, html, imp

if __name__ == "__main__":
    for dir in helper():
         system( "pydoc -w %(dir)s" %vars() )
        
