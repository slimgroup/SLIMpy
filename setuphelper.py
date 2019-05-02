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

from os import walk
from os.path import dirname


def helper(dir):
    w = walk( dir )
    
    rm = '/'.join(dir.split('/')[:-1])+'/'
    print rm
    
    dirs =  [ ".".join(x.replace(rm,'').split('/')) for x,y,z in w if '.svn' not in x ]
    
    #dirs = [d[1:] for d in dirs[1:]]
    
    return dirs

if __name__ == '__main__':
    import slimpy_base
    dir = dirname(slimpy_base.__file__)
    packages = helper(dir)
    print '[',
    for package in packages:
        print 
        print '"'+package+'",',
    print ']'
    
#print "packages = [   '" + "',\n   '".join(dirs) + "' ]"

