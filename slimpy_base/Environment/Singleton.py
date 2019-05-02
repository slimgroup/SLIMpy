"""
TODO: doc
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

from inspect import getmro

class Singleton(object):
    """
    Singleton class conforms to singleton 
    design pattern
    """ 
    
    def __new__(cls, *p):
        """
        sets class attributs _default_instance and 
        _instance_map if not set.
        and checks that no subclass overloads the 
        __init__ method.
        """
        if '_default_instance' not in  cls.__dict__:
            cls._default_instance = 'default' 

        if '_instance_map' not in  cls.__dict__:
            cls._instance_map = dict()                     
        
        name = "__init__"
        if name in cls.__dict__:
            obj = cls.__dict__[name]
        else:
            obj = getattr(cls, name)

        # Figure out where it was defined.
        homecls = getattr(obj, "__objclass__", None)
        if homecls is None:
            mro = getmro( cls )
            # search the dicts.
            for base in mro:
                if name in base.__dict__:
                    homecls = base
                    break
                
        if homecls is not Singleton:
            msg = ( "can not overload '__init__' method of Singleton class.\n"
                    "class %(homecls)s defines new '__init__'" %vars() )

            raise TypeError(msg)
        
        return object.__new__( cls )

    def __init__( self, *p ):
        """
        should not be called by subclasses
        """
        if not p:
            instance_name = self.__class__._default_instance
        else:
            instance_name = p[0]
            
            
        if self._instance_map.has_key(instance_name):
            shared_state = self._instance_map[instance_name]
            self.__dict__ = shared_state
            return
        else:
            shared_state = self._instance_map.setdefault(instance_name,{})
            self.__dict__ = shared_state
            self.__new_instance__( instance_name )
            
        
    def __new_instance__( self, name ):
        """
        to be initialize class instead of __init__
        """
        self.__i_name = name
    
    @classmethod
    def __del_instance__( cls, name ):
        """
        delete the instance 'name' 
        """
        if cls._instance_map.has_key(name):
            del cls._instance_map[ name ]
    
    def __clean__(self):
        'to be used instead of __del__ to delete and instance'
        pass
        
    @classmethod
    def _num_instances(cls):
        'get the number of instances of this class'
        return len( cls._instance_map )

    def _get_instance_name(self):
        '''
        returns the name if this instance.
        not that singl.__class__( singl._get_instance_name() ) 
        returns 'singl'
        '''
        return self.__i_name  

    def _set_instance_name(self, val):
        'dont use this'
        self.__i_name = val
        
    _instance_name =  property( _get_instance_name, _set_instance_name )
    

  
