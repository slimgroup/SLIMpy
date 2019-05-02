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


"""
n1,n2 and n1out,n2out are the same.  If n1 (or n1out) is declared then
you set the space to equal n1 (or n1out).

If beg1,beg2,end1,end2 are declared instead. Then you want to grab the
exsisting space and add these to the being and end of them.
"""
def padHelper(command,space,*spaces):
    for cmd in command.kparams.keys():
        if re.match('^n\d+$',cmd):
            space[cmd] = command[cmd]
        elif re.match('^n\d+out$',cmd):
            space[re.findall('(^n\d+)out$',cmd)[0]] = command[cmd]
        elif re.match('^beg\d+$',cmd):
            dim = re.findall('^beg(\d+)$',cmd)[0]
            if command.has_key('end'+dim):
                space['n'+dim] = space['n'+dim] + command[cmd] + command['end'+dim]
            else:
                space['n'+dim] = space['n'+dim] + command[cmd]
        elif re.match('^end\d+$',cmd):
            dim = re.findall('^end(\d+)$',cmd)[0]
            if not command.has_key('beg'+dim):
                space['n'+dim] = space['n'+dim] + command[cmd]

"""
We want to have:
Back to original Size: 
"""
def padAdjHelper(command,space,*spaces):
    for cmd in command.kparams.keys():
        if re.match('^n\d+$',cmd):
            space[cmd] = command[cmd]
        elif re.match('^n\d+out$',cmd):
            space[re.findall('(^n\d+)out$',cmd)[0]] = command[cmd]
        elif re.match('^beg\d+$',cmd):
            dim = re.findall('^beg(\d+)$',cmd)[0]
            if command.has_key('end'+dim):
                space['n'+dim] = space['n'+dim] - command[cmd] - command['end'+dim]
            else:
                space['n'+dim] = space['n'+dim] - command[cmd]
        elif re.match('^end\d+$',cmd):
            dim = re.findall('^end(\d+)$',cmd)[0]
            if not command.has_key('beg'+dim):
                space['n'+dim] = space['n'+dim] - command[cmd]

"""
And map the new paramters to f# and n#:
beg1/end1:
    f1 = beg1
         Update n1 accordingly.
    n1 = n1(after pad) - end1
n1/n1out:
    n1 = n1
    n1 = n1out
"""

def shape(space):
    n_val = 1
    key = "n%(n_val)s"
    shp = []
    while space.has_key(key):
        shp.append( space[key] )
        
    return shp
    
def padReplaceHelper(command,space):
    kparams = command.kparams        
    
    for par in kparams.keys():
        if re.match('^n\d+$',par):
            pass
        elif re.match('^n\d+out$',par):
            kparams[re.findall('(^n\d+)out$',par)[0]] = kparams[par]
            kparams.pop(par)
        elif re.match('^beg\d+$',par):
            dim = re.findall('^beg(\d+)$',par)[0]
            if kparams.has_key('end'+dim):
                kparams['f'+dim] = kparams[par]
                kparams['n'+dim] = space['n'+dim] - kparams[par] - kparams['end'+dim]
                kparams.pop('end'+dim)
                kparams.pop(par)
            elif kparams.has_key(par):
                kparams['f'+dim] = kparams[par]
                kparams['n'+dim] = space['n'+dim] - kparams[par]
                kparams.pop(par)
        elif re.match('^end\d+$',par):
            dim = re.findall('^end(\d+)$',par)[0]
            if kparams.has_key('beg'+dim):
                kparams['n'+dim] = space['n'+dim] - kparams[par] - kparams['beg'+dim]
                kparams['f'+dim] = kparams['beg'+dim]
                kparams.pop('beg'+dim)
                kparams.pop(par)
            elif kparams.has_key(par):
                kparams['n'+dim] = space['n'+dim] - kparams[par]
                kparams.pop(par)
    return command
    
