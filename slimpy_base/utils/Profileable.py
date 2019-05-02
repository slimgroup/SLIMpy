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


def note( doc_str ):
    def p_doc( method ):
        method.__note__ = doc_str
        return method
    return p_doc
    
class Profileable( object ):
    Profiles = {}
    
    def __new__(cls,name,bases,dict):
    
        methods_dict = cls.get_methods_dict(dict)
        
        new_class = type(name,bases,dict)
        
        cls.Profiles[name] = (new_class,methods_dict)
        
        return new_class
    
    
    @classmethod
    def get_methods_dict(cls,dict):
        
        md = {}
        for key,val in dict.iteritems():
            if hasattr(val, "__note__"):
                doc_str = getattr(val, "__note__")
                md[key] = doc_str
        
        return md 
