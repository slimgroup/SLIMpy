#!/usr/bin/env python
# encoding: utf-8
"""
Version helper updates the version in 'SLIMpy/info.py'

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

from os import popen
from os.path import dirname,exists
import re

def getrev():
    """
    get svn dat,revision as a string using the command line 
    'svn info \%(SLIMpy.__file__)s' 
    """
    if exists('SVNINFO.txt'):
        svn_info = popen("cat SVNINFO.txt")
    else:
        this = dirname(__file__)
        svn_info = popen("svn info %(this)s" %vars())
    info = svn_info.read()
    
    revex = re.compile("Last Changed Rev: \d*")
    all = revex.findall(info)
    try:
        rev = all[0][18:]
    except:
        rev = "Unknown"
    
    dateex = re.compile("Last Changed Date: .*")
    all = dateex.findall(info)
    dateex = re.compile("\(.*\)")
    all = dateex.findall(info)
    try:
        date = all[0][1:-1]
    except:
        date = "Unknown"
    
    return date, rev

def format(date, rev):
    """
    format data and revision in 
    python style 
    """
    return "date = '%(date)s'\nrev = '%(rev)s'" % vars()

def tofile(name):
    """
    put data and revision to 
    importable python file
    """
    filed = open(name, 'w')
    date, rev = getrev()
    filed.write(format(date, rev))
    filed.close()

if __name__ == "__main__":
#    svn_date, svn_rev = getrev()
    tofile("SLIMpy/info.py")

