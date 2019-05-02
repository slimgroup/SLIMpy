"""
handy class that seporates dictionaries to many dictionaries
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


class dictSeporator( object ):
    """
    handy class that seporates dictionaries to many dictionaries
    """
    
    def __new__( cls, d, fkeys=None ):
        """
        
        """
        if fkeys is None:
            fkeys = []
        return dictSeporator.dictSeporator( d, fkeys=fkeys )
    
    @staticmethod
    def dictSeporator( k, fkeys=None ):
        """
        seporates dictionaries to many dictionaries
        """
        if fkeys is None:
            fkeys = []

        List = []
        d = {}
        
        for key in k.keys():
            x = key[-1]
            if x.isdigit():
                d2 = d.setdefault( int( x ), dictSeporator.getNonNumberedKeys( k, fkeys=fkeys ) )
                d2[key[:-1]] = k[key]
        
        if d:
            x = 1
            while x:
                item = d.pop( x, False )
                x += 1
                if item:
                    List.append( item )
                else:
                    break
                    
            return List
        else:
            return [dictSeporator.getNonNumberedKeys( k, fkeys=fkeys )]
        
            
        
        

    
    
    @staticmethod
    def getNonNumberedKeys( k, fkeys=None ):
        """
        gets 
        """
        if fkeys is None:
            fkeys = []
            
        d = dict.fromkeys( fkeys )
        
        for key in k.keys():
    
            if not key[-1].isdigit():
                d[key] = k[key]
        return d
    
