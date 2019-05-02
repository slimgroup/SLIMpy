"""
capture and  Filter output 
"""
import sys
import time
from slimpy_base.Environment.Singleton import Singleton
from slimpy_base.Environment.InstanceManager import InstanceManager
from atexit import register as __register__
from pickle import dump
import threading
from sys import stdout

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



__env__ = InstanceManager()

def time_format( t ):
    if t/(60.*60.) > 1:
        tm = "%3.1f hrs" %(t/(60.*60.))
    elif t/(60.) > 1:
        tm = "%3.1f min" %(t/(60.))
    else:
        tm = "%3i sec" %(t)
        
    return tm

class Records( Singleton ):
    """
    class to capture and filter output
    oprional dump to file an view with record_viewer scripts 
    """
#    env = InstanceManager()
    
    def __new_instance__(self, name):
        Singleton.__new_instance__(self, name)
         
        self._built_graph = None
        self.msg_record = []
        self.command_records = []
        self.trace_back_records = {}
        
        self._filters = set( )
        self._filter_type = "any"
        
        self._abridge = False 
#        print traceback.extract_stack()
        __register__( self.dump )
            
    def __call__( self, verbose_level , *debug):
        """
        records( vlevel, *debug ) -> RecordHelper
        returns a RecordHelper instance
        vlevel is an integer
        debug are optional keywords
        """
        curthread = threading.currentThread()

        node = curthread.getName()
        if hasattr(curthread, 'processor'):
            processor = getattr(curthread, 'processor')
        else:
            processor = 0
        
        
        rh = RecordHelper(verbose_level, (node,processor) , debug)
        return rh
    
    def write(self,msg):
        """
        
        """
        rc = self( 0 )
        rc.write(msg)
    
    def _get_graph(self):
        return self._built_graph

    def _set_graph(self,graph):
        self._built_graph = graph
        
    graph = property( _get_graph, _set_graph )
    
    def add_job(self,job_rec):
        
        self.command_records.append(job_rec)
        
    def rec(self,msg_record_item):
        
        if not isinstance(msg_record_item, dict):
            raise TypeError('msg_record_item must be a dictionary')
        
        assert msg_record_item.has_key('verb')
        assert msg_record_item.has_key('debug')
        assert msg_record_item.has_key('node')
        assert msg_record_item.has_key('msg')
        
        self.print_record_item( msg_record_item )
        self.msg_record.append( msg_record_item )
        pass
    
    def add_filter(self,filter):
        
        self._filters.add( filter )
    
        
    def print_record_item( self, msg_record_item ):
        verb = __env__['slimvars']['verbose']
        debug = __env__['slimvars']['debug']
        
        rdb = msg_record_item['debug']
        db = debug in rdb
        if  isinstance(debug, (list,tuple) ):
            db = db or bool(set( rdb ).intersection(debug))
        
        if db or verb >=  msg_record_item['verb']:
            msg = msg_record_item['msg']
            msg = self.abridge(msg)
            print msg,
            stdout.flush( )
             
    def dump(self):
#        print "dumping", __env__.get_env( )
        
        self._table_map = __env__['table']._map
        logfile = __env__['slimvars']['logfile']
        
#        print "|- ",logfile
        if logfile is not None: 
#            print "-- ",logfile
            f = open(logfile,'w')
            dump(self, f)
            
            f.flush( )
            f.close( )

    def End(self):
#        print 'end'
        self.dump( )
    
    
    def _init_env(self):
        
        __env__['table']._map = self._table_map
        __env__['table']._do_not_clean( )
    
    
    def set_filter_type( self, ftype ):
        self._filter_type = ftype
        
    def generate_index_list(self):
        
        
        if self._filter_type == "all":
            index = range( len(self.msg_record) )
            index_set = set( index )
            cat = index_set.intersection_update
            
        elif  self._filter_type == "any":
            index_set = set(  )
            cat = index_set.update
        else:
            raise Exception
        
#        print cat
        for filter in self._filters:
#            print index_set
            f_iset = filter.gen_index_set( self.msg_record )
#            print f_iset
            cat( f_iset )
            
#        print index_set
        
        index = list( index_set )
        index.sort( )
        
        return index
    
    
    def __getitem__(self,idx):
        msg = self.msg_record[idx]['msg']
        if self._abridge:
            
            msg = self.abridge( msg )
        return msg
    
    def print_log(self, abridge=False):
        
        index = self.generate_index_list( )
#        print index
        for i in index:
            print self[i],
            stdout.flush()
        return

        
    def print_filter(self,verb=1,debug=None, node=None,abridge=False ):
        
        verb_check = lambda item:(item['verb'] <= verb)
            
        if debug:
            debug_set = set(debug)
        
        def debug_check(item):
            if not debug:
                return False
            if not item['debug']:
                return False
            if debug_set.intersection( item['debug'] ):
                return True
            return False
         
        def node_check(item):
            if not node:
                return True
            nn,pr = node
            nodename,proc = item['node']
            
            ret = True
            if nn :
                
                if nodename in nn:
                    if pr:
                        if proc in pr:
                            return True
                        else:
                            return False
                    else:
                        return True 
                else:
                    return False
            else:
                return True
            
            
        
        check = lambda item: verb_check(item) or debug_check(item)
        
        filtered_list = [ item for item in self.msg_record if check(item) and node_check(item)]
                
        for item in filtered_list:
            if abridge:
                print self.abridge(item['msg']),
            else:
                print item['msg'],
            stdout.flush()
        return
    
    def print_filter_list(self):
        
        filter_list = [ item['debug'] for item in self.msg_record ]
        filter_set = set()
        for item in filter_list:
            filter_set.update( item )

        node_list = [ item['node'] for item in self.msg_record ]
        node_set = set()
        for item in node_list:
            node_set.add( item )
            
        print "\nItems to allow by:\n"
        for item in filter_set:
            print "    '%s'" % item
        print 
        
        print "Node to filter by:\n"
        for item in node_set:
            print "    node:'%s', processor:'%s'" % item
        print 
    
    def set_abridge( self, abr ):
        self._abridge = abr
        
    
    def abridge( self, string ):
        """
        uses the global dict variable 'abridgeMap' in SLIMGlobals
        to replace all of the ocurrences of each key with the value
        this is helpful in reducing the amount of garbage input
        for examle in the simple1 tutorial I replace each $RSFROOT path with ''
        
        """
        slimvars = __env__['slimvars']
#        file = re.compile( "(slim\.\d*.env\d*\..*\.(.*\.\d*)\.rsf)" )
#        
#        
#        items = file.findall( string )
#        for old,new in items:
#            print
#            print "old,new",old,new
#            string = string.replace(old,new)
        if slimvars['abridge']:
            for item in slimvars['abridgeMap'].items():
                string = string.replace( *item )
            
        return string
    
    def stat(self):
        if 'stat' in  __env__['slimvars']['debug']:
            print 
            graph = self._built_graph
            self._starttime = time.time( )
            self._tottime = 0
            self._numtorun = len([item for item in graph.getInvAdjacencyList().keys() if isinstance(item,tuple)])
            self._numran = 0
    
    def stat_done(self):
        if 'stat' in  __env__['slimvars']['debug']:
            print
            print "100% Done"
    
    def stat_update(self,msg=None):
        if 'stat' in  __env__['slimvars']['debug']:
            num = self._numtorun
            self._numran += 1
            i =self._numran
    
            self._tottime = time.time() - self._starttime
            tot_time = self._tottime
            etime = tot_time/i*(num-i)
            
            tot_time = time_format(tot_time)
            etime = time_format(etime)
            
            perc = (float(i)/float(num))*100.
            eq = "="*int(perc/2)
            sp = " "*(50-int(perc/2))
            
            
                
            print "|",eq+'>'+sp+'|', "%3i%%"%int(perc), "( %3i of %3i commands) total time %s || time remaining %s" %(i,num,tot_time,etime),
            print "\r",
            sys.stdout.flush( )
        
    
    
    
class RecordHelper( object):
    
    env = InstanceManager()
    
    def __init__(self,verbose_level ,node, debug):
        
        self.msg_record_item = { 'verb':verbose_level,
                                 'node':node,
                                 'debug':debug}
        
    def write(self,msg):
        
        msg_record_item = self.msg_record_item.copy()
        msg_record_item['msg'] = msg
        
        self.env['record'].rec( msg_record_item )
        
    
