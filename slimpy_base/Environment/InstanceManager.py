"""
environment settings for all of slimpy 
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


from thread import get_ident

def thread_landmark():
    'returns the thread id'
    return get_ident()

class InstanceManager( object ):
    '''
    manages instance with a landmak function
    
    '''
    _shared_state = { }
    singletons = dict()
    non_singletons = dict()
    _ns_map = dict()
    _lm_map = { }
    _lm_count = 0
    
    _rank = []
    
    def __str__( self ):
        return "InstanceManager<default=%s>" %self.get_env()
    
    def get_count( self ):
        'returns the number of dirrent keys the lanmark has returned'
        InstanceManager._lm_count += 1
        return InstanceManager._lm_count
    
    count = property( get_count )
    
    def __init__( self ):
        self.__dict__ = self._shared_state
        
    def set_schema( self, schematic ):
        'not implemented'
        pass
    
    def __iter__( self ):
        'returns a list of the names of the singleton classes'
        for key in self.singletons:
            yield self[key]
        return
    
    def __getitem__( self, item ):
        '''
        returns an singleton instance
        env[name]  <==> env.get_singleton(name)  
        '''
        Class = self.singletons[item]
        
        landmark_id = self.landmark()
        
        instance_id = self.map( landmark_id )

        instance = Class( instance_id )
        
        return instance
    
    def get_singleton( self, item ):
        'same as env.get_singleton(name) <==> env[name]'
        Class = self.singletons[item]
        
        landmark_id = self.landmark()
        
        insnace_id = self.map( landmark_id )

        instance = Class( insnace_id )
        
        return instance

    def get_non_singleton( self, name ):        
        'return non singleton class managed by this'
        cur_env = self.current_env
        
        env_map = self._ns_map[name]
        
        ns = self.non_singletons[name]
        
        if not env_map.has_key( cur_env ):
            obj = ns['obj']
            p = ns['p']
            kw = ns['kw']
            
            non_single = obj( *p, **kw )
        else:
            non_single = env_map[cur_env]
            
        return non_single 
        

    def map( self, landmark_id ):
        """return the current landmark id
        as env#  
        """
        if landmark_id not in self._lm_map:
            self._lm_map[ landmark_id ] = "env%s" %self.count
        return self._lm_map[ landmark_id ]
        
    def _get_lm( self ):
        'returns landmark function'
        return self._lm_map.keys()
    
    lms = property( _get_lm )
        
    def _get_instance_names( self ):
        'returns all of the evironments that where instanciated so far'
        return set( self._lm_map.values() )
    
    instance_names = property( _get_instance_names )
    
    def __setitem__( self, item, value ):
        "add a singleton class"
        self.singletons[item] = value
        
        self._rank.append( item )
     
    def set_landmark( self, lm ):
        'set landmark function'
        self._landmark = lm
        return
    
    def get_landmark( self ):
        'returns landmark function'
        if not hasattr( self, "_landmark" ):
            return thread_landmark
        else:
            return self._landmark
    
    def set( self, lm, name ):
        """
        should use set_env instead
        set the mapping for landmark
        used to mark instances that should be the same but are not
        example:
            if the landmark is by thread, then
            to map two theads to the same instance
            then
            call:
                set( thread1_id, "newname")
                set( thread2_id, "newname")
             
        """
        self._lm_map[ lm ] = name
    
    def set_env( self, name ):
        """
        set an environment name in the map
        if instances have already been created with a
        old name then  
        """
        landmark_id = self.landmark()
        
        if self._lm_map.has_key( landmark_id ):
            if not self._lm_map[landmark_id] == name:
                raise Exception( "environment already set" )
            else:
                return
            
        self._lm_map[ self.landmark() ] = name
    
    def get_env( self ):
        '''
        returns the current env name
        '''
        landmark_id = self.landmark()
        return self.map( landmark_id )
    
    landmark = property( get_landmark, set_landmark )
    current_env = property( get_env, set_env )
    
    
    def __delitem__(self,instance_name):
        self.del_instance( instance_name )
    
    def del_instance( self, instance_name ):
        """
        delete the instance 'instance_name' from each 
        singleton stored
        """
#        for singleton_class in self.singletons.values():
        for key in self._rank:
            singleton_class = self.singletons[key]
            singleton_class( instance_name ).__clean__()
            singleton_class.__del_instance__( instance_name )
            
        for key, val in self._lm_map.iteritems():
            if val == instance_name:
                self._lm_map.pop( key )
                break
            
        return 
                
    def assure_new_instances( self ):
        """
        calls the __new_instance__ class for each of the 
        classes stored
        """
        for key in self._rank:
            self[key]
            
        return

    def manage_non_singleton( self, name, obj, *p, **kw ):
        """
        add a non-singleton class, treats it like a singleton
        """
        self.non_singletons[name] = { 'obj': obj, 'p':p, 'kw':kw }
        
#        ns = self.non_singletons[name]
        
        env_map = self._ns_map.setdefault( name, {} )
        env_map[self.current_env] = obj( *p, **kw )
    
    def Execute(self):
        return self.End()
    def End( self ):
        """
        calls 'End' on each singleton class before calling 
        __del_instance__
        """
        current_env = self.current_env
        
        for instance in self:
            if hasattr( instance, "End" ):
                instance.End()
        
        self.del_instance( current_env )
        self.assure_new_instances()
        
    def reset( self ):
        current_env = self.current_env
        self.del_instance( current_env )
        self.assure_new_instances()
