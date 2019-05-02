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

def agvwidth( graph ):
    'some metric for how parallel a graph is'
    
    prev = set( graph.getSourceNodes() )
    tot = set( prev )
    
    widths = []
    push = widths.append
    
    while prev:
        push( len( prev ) )
        next = set()
        for item in prev:
            nitem = graph.adj( item )
            for i in nitem :
                if not i  in tot:
                    next.add( i )
                    tot.add( i )
        prev = next
    
    min_ = min( widths )
    max_ = max( widths )
    avg  = sum( widths ) / float( len( widths ) ) 
    return min_, max_, avg
