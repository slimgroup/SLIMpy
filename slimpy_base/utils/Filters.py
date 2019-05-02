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



class Filter( object):
    
    def gen_index_set( self, record_list ):
        
        index_list = range( len(record_list) )
        return set( index_list )
    

class VerbosityFilter( Filter ):
    
    def __init__(self,verb):
        self._verb = verb
        return
    
    def gen_index_set( self, record_list ):
        index_set = set( )
        for i,item in enumerate( record_list ):
            if item['verb'] <= self._verb:
                index_set.add( i )
        
        return index_set
    
class DebugFilter( Filter ):
    
    def __init__(self, db_list):
        self._db = set( db_list )
        
    
    def gen_index_set( self, record_list ):
        
        index_set = set( )
        
        for i, item in enumerate( record_list ):
            
            if self._db.intersection( item['debug'] ):
                index_set.add( i )
        
        return index_set
    
