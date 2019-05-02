"""
Vector Interface to RSF.
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

from pdb import set_trace
from slimpy_base.Core.Command.Drivers.Unix_Pipes import gethostname

from slimpy_base.Core.Command.Drivers.Unix_Pipes import Unix_Pipes, is_localhost
from slimpy_base.Core.Interface.ContainerBase import  DataContainer
from slimpy_base.Environment.InstanceManager import InstanceManager
from numpy import int32, float32, float64, complex64 #IGNORE:E0611:E1101 @UnresolvedImport
from numpy import product, fromfile #IGNORE:E0611
from os import tempnam, system, getpid
from os.path import isfile, join, dirname, abspath, basename, exists, split
from rsfScalar import Scalar as ScalarMethods
from sfCommandFactory import rsfCommandFactory
from string import Template
from subprocess import Popen, PIPE as __PIPE__, STDOUT as _STDOUT
from sys import modules





class rsf_data_container( DataContainer ):
    """
    rsf_data_container - to keep track of "out of core" vectors
    corresponding binary files on disk.
    """
    suffix = ".rsf"
    psuffix = ".vpl"
    name = "rsf"
#    slimvars = GlobalVars()
#    log = Log()

    env = InstanceManager()
    
    COUNT = 0
    sfFactory = rsfCommandFactory()
    
#    command = "%(path)s < %(data)s want=%(want)s lval=%(lval)s" %vars()
    _scalar_methods = ScalarMethods
    
    
    @classmethod
    def isCompatibleWith( cls, obj ):
        '''
        statict method to determine if 'obj' is an rsf file
        @param obj:
        @type obj: any object that would be 
            contained in a datacontainer class
        '''
        
        obj = str(obj)
        
        if obj.endswith( cls.suffix ):
            if not isfile( obj ):
                raise Exception, "the file %s can not be found" %( obj )
            return True
        if isfile( obj+cls.suffix ):
            return True
        
        return False 
    
    def __init__( self , data=None , parameters=None, command=None , tmp=None, nodenames=None, target_node=None):
        
#        self.scalar = Scalar()    
        self.SFRM =   join( self.env['slimvars']['RSFBIN'], 'sfrm' )
        self.SFGREY = join( self.env['slimvars']['RSFBIN'], 'sfgrey' )
        self.SFMV =   join( self.env['slimvars']['RSFBIN'], 'sfmv' )
        self.XTPEN =  join( self.env['slimvars']['RSFBIN'], 'xtpen' )
        self.SFATTR = join( self.env['slimvars']['RSFBIN'], 'sfattr' )
        self.SFDD =   join( self.env['slimvars']['RSFBIN'], 'sfdd' )
        
        self.PLOTCMD = Template( "< ${data} ${plotcmd}  |  ${viewcmd} &" )
        self.MVCMD = Template( "${mv} ${From} ${To}" )
        self.RMCMD = Template( "${rm} ${file}" )
        
        self.ATTRMD = Template( "${attr} <  ${file} want=${want} lval=${lval} " )
        
        
        node_info = None
        
        if data is not None:
            data = str(data)
            data = abspath( data )
            if not data.endswith( self.suffix ):
                data = data + self.suffix
            
            dname = dirname( data )
            data = basename(data)
            node_info = dict( location=dname )
            
        DataContainer.__init__( self, data=data, 
                                parameters=parameters , 
                                command=command ,tmp=tmp, 
                                nodenames=nodenames,
                                node_info=node_info,
                                target_node=target_node )
        
        
    
    def __setitem__( self, item, value ):
        """
        """
        raise NotImplementedError
        
#        assert item == 'data', "can not set the item %s(item)s" % vars()
  
    def makeparams( self ):
        '''
        returns a param object created from the data contained
        ie. the rsf header info
        '''
        par = DataContainer.makeparams( self )
        

        # RSF specific stuff
        try:
            format, data_type = par['data_format'].split( '_' )
        except KeyError:
            print self, 'has no key "data_format"'
            raise
                
        par['data_type'] = data_type
        
        return par
    
    
    def genname_helper(self, string):
        """
        formatting and better output files, no more tempname just 'slim.%prog.%cmd.%id.rsf'
        where %prog is the main programs name and %cmd is the last command 
        on the pipe that created the data and 
        %id is a unique incremented identifier
        """
        main_file = "ineractive"
        
        main = modules['__main__']
        if hasattr(main, '__file__'):
            main_file = main.__file__
            
        prog = basename( main_file )[:-3]
        
        join_dot = lambda *args:".".join(args)
        
        pid = str(getpid())
        cur_env = self.env.current_env
        
        make = lambda fcn, cnt: join_dot( 'slim',
                                       pid, cur_env, 
                                       prog[:6], 
                                       fcn[:5], 
                                       "%.5d" % cnt) + self.suffix
        
        if exists(string):
            string = split(string)[1]
        self.__class__.COUNT += 1
        filename = make( string, self.COUNT ) 
        while  exists( filename ):
            self.__class__.COUNT +=1
            filename = make(string, self.COUNT )
        return filename
        
        
    def genName( self, command=None):
        """
        generate a random name if command is given
        then generate a unique but formatted name
        'slim.%prog.%cmd.%id.rsf'
        """
        if command is not None and hasattr(command, 'tag') and isinstance(command.tag, str):
            filename = self.genname_helper(command.tag)
        elif command is not None and isinstance(command, str):
            filename = self.genname_helper( command )
        else:
#            raise Exception( "must spcify a valid command to generate an appropreate file" )
            td = self.get_tmp_dir()
            filename = tempnam( td ) + self.suffix
         
        return filename
    
    def get_tmp_dir(self):
        if self.is_local:
            return self.env['slimvars']['localtmpdir']
        else:
            return self.env['slimvars']['globaltmpdir']
    
        
        
    
    def isempty( self ):
        """
        check if this data has bee built
        """
        local_data = self.get_data('localhost')
        if isfile( local_data ):
            return False
        
        if self.data:
            if 'localhost' in self.nodenames:
                return not isfile( local_data )
            else:
                return not len( self.nodenames )
        
#    def getConverter( self , command ):
#        '''
#        return converter class
#        
#        command must have attribute 'function'  
#        '''
#        return self.sfFactory[command.tag]
        
    @classmethod
    def get_converter(self ,command ):
        
        if isinstance(command, str ):
            tag = command
        else:
            tag = command.tag
        return self.sfFactory[tag]
    
    def __str__( self ):
        """Adds the current lib's suffix to the end of filename
        note: if no lib is set then self.plugin.suffix returns ''
        """
        if self.data != None:
            return str( self.data )
        else:
            return "None"
        
    def __repr__( self ):
        return str( self )

    def path( self ):
        """
        returns the absolute pathname to the file
        """
        pathstr = abspath( str( self ) )
        pathstr = dirname( pathstr )
        return pathstr
    
    def getName( self ):
        'returns the name of the data contained'
        return  self.data


    def plot( self, command=None, plotcmd=None ):
        """
        plot returns the path the the plotfile
        """
        
        if command is None:
            
            if plotcmd is None:
                plotcmd = self.SFGREY
             
            command = self.PLOTCMD.substitute( data=self.local_data, 
                                               plotcmd=plotcmd, 
                                               viewcmd=self.XTPEN ) 

        
        print >> self.env['record']( 1, 'plot' ), command
        system( command )
        
        return None
    
    def _get_local_data(self):
        return self.get_data("localhost" )
    
    local_data = property( _get_local_data )
    
    def _get_any_node(self):
        if 'localhost' in self.nodenames or not self.nodenames:
            node = 'localhost'
        else:
            node = list(self.nodenames)[0]
            
        return node, self.get_data(node)
        
    
    def setName( self, newname, path=None ):
        """wrapped by SLIMpy.serial_vector.setname"""
        newname = str(newname)
        
        if newname.endswith( self.suffix ):
            newname = newname
        else:
            newname = newname + self.suffix
        
        if not path:    
            newname = abspath(newname)
            path = dirname( newname )
            newname = basename( newname )
        
        if self.isfull():
            self.move( newname )

        self.updateData( newname )
        ninfo =self._node_info.setdefault( 'localhost', {} )
        self.add_node_name( 'localhost' )
        ninfo['location'] = path
        
        self.tmp( False )
        
    
    def updateData( self, newname ):
        '''
        @param newname: string to rename data to
        @type newname:
        '''
        self.data = newname 
    
    def getHeader( self ):
        """
        return open header, data must exist
        """
        
        node,data = self._get_any_node()
        if node == 'localhost':
            return open( data )
        
        else:
            cat = Unix_Pipes.CreateComand( ['cat'], node_name=node, source=data )
            p0 = Popen( cat, shell=True, stdout=__PIPE__ )
            
        return p0.stdout

    def move( self, newname ):
        "move data file on disk"
        
        mv = self.MVCMD.substitute( mv=self.SFMV, From=self.local_data, To=abspath( newname ) )
        
        err = system( mv )
        if err is not 0:
            raise Exception( "commmand %(mv)s failed " %vars() )
    
    def rm( self ):
        """
        removes the file on disc
        """
        
        print >> self.env['record']( 10, 'cleaner' ), "call to remove %s:" %self.data
        print >> self.env['record']( 11, 'cleaner' ), "\tistmp=%s , isfull=%s" %( self.istmp() , self.isfull() )
        
        if not self.istmp():
            return False
        if self.isempty():
            return False
        
        err = 0
        cmd_log1 = self.env['record'](1,'cmd')
#        print "rm called"
        
        synccmd = self.env['slimvars']['SYNC_CMD']
        do_sync = self.env['slimvars']['sync_disk_om_rm']
        
        def sync(synccmd):
            
            sync_command = Unix_Pipes.CreateComand([synccmd], node)
            print >> cmd_log1 , sync_command
            p0 = Popen( sync_command, shell=True, stderr=__PIPE__)
            ret = p0.wait( )
            if ret:
                print >> self.env['record'] , 'error running %(sync_command)s ' %vars()
                print >> self.env['record'] , 'try running SLIMpy with "sync_disk_om_rm=False" ' %vars()
        
        for node in self.nodenames.copy():
            
            data = self.get_data( node )
            sfrm = self.RMCMD.substitute( rm=self.SFRM, file=data )
            rm = self.RMCMD.substitute( rm='rm', file=data )
            if do_sync:            
                sync(synccmd)
                        
            command = Unix_Pipes.CreateComand([sfrm], node)
            print >> cmd_log1 , command
            p0 = Popen( command, shell=True, stderr=__PIPE__)
            ret = p0.wait()
            print >> self.env['record'](2) , "finished::",node,'rm'
            if ret:
                err += 1
                msg = p0.stderr.read( )
                p0.stderr.close()
                print >> self.env['record'] , 'error %(ret)s on %(command)s: removeing header file:\n%(msg)s' %vars()
                command = Unix_Pipes.CreateComand([rm], node)
                print >> cmd_log1 , command                
                p0 = Popen( command, shell=True, stderr=__PIPE__)
                ret = p0.wait()
                if ret:
                    msg = p0.stderr.read()
                    print >> cmd_log1 ,"could not 'sfrm' or rm 'data'\n%(msg)s" % vars()
                else:
                    self.nodenames.remove(node)
            else:
                self.nodenames.remove(node)

            p0.stderr.close()
            return not err

    def node_copy(self, node_name):
        """
        copy from one node to another
        """
        if self.is_global or self.isempty():
            return
        if node_name in self.nodenames:
            return
        

        
        tmddir = self.env['slimvars']['localtmpdir']
        from_cmd = "%s form=xdr" %  self.SFDD 
        to_cmd = "%s form=native" % self.SFDD 
        
        from_node = list(self.nodenames)[0]
        
        from_data = self.get_data( from_node )
        to_data = self.get_data( node_name )
        
        is_tmp = self.istmp() 
        to_cmd = Unix_Pipes.CreateComand([to_cmd], node_name=node_name, 
                                target=to_data ,is_local=[True], 
                                is_tmp=[is_tmp] ,ssh_localhost=True)
        frm_node = list(self.nodenames)[0]
        
        
        self.add_node_name( node_name )
        
        cmd = Unix_Pipes.CreateComand( [from_cmd,to_cmd],
                                       is_local=[None,None],
                                       is_tmp=[is_tmp,is_tmp],
                                       node_name=frm_node, 
                                       source=from_data, 
                                       ssh_localhost=False)
        
        print >> self.env['record'](1,'cmd'), cmd
        assert  frm_node != node_name, "can not copy from same node to same node" 
        p0 = Popen(cmd, shell=True, stderr=__PIPE__ )
        p0.wait()
        print >> self.env['record'](2,'cmd'), "finished:: cp",node_name
        if p0.returncode:
            out = p0.stderr.read()
            raise IOError("copying from node to node retuned error %s\n\n%s" %(p0.returncode,out) )
        
        
    def available_from( self, nodename ):
        if nodename in self.nodenames:
            return True
        elif 'localhost' in self.nodenames:
            return True
        return False
    

    def readattr( self ):
        'returns rsf header info as a dict object'
        header = self.getHeader()
        lines = header.readlines()
        
        header.close()
        
        file_dict = {}
        for line in lines:
            if '=' in line:
                line = line[1:-1]
                line = line.split( '=' )
                try:
                    line[1] = eval(line[1])
                except:
                    pass
                file_dict[line[0]] = line[1]
                
        self.BinFile = file_dict.pop( 'in' )
            #l = lambda x : (x=='native_int' and int) or (x=='native_float' and float) or (x=='native_double' and long) or (x=='native_complex' and complex)
            
            #file_dict['type'] = l(file_dict['data_format'])
            #del file_dict['data_format']
                
        return file_dict 
            
    def readbin( self, start=0, len=-1 ): #IGNORE:W0622 
        '''
        @precondition: data must exist.
        @return: a numpy array.
        
        @param start: element in data to start from.  
        @type start: int
        
        @param:  len: lenght of data to read into array
                if -1 reads until the end of data.   
        @type len:int
        '''
        
        l = lambda x : ( ( x == 'native_int'     and int32 ) or
                        ( x == 'native_float'   and  float32 ) or 
                        ( x == 'native_double'  and  float64 ) or 
                        ( x == 'native_complex' and  complex64 ) )
        
        file_dict  = self.readattr()
        typeflag = l( file_dict['data_format'] )
    
    
        fd = open( self.BinFile )
        fd.seek( start*typeflag().nbytes )
    
        return fromfile( fd, typeflag, len )
    
    def writebin( self, data, start=0, size=0 ):
        """
        write data to file 
        not tested
        """
        header = self.path()
        start = start*4
    
        vector_dict, file_dict  = self.readattr( header )
        if size == 0:
            size = product( vector_dict['dim'] )
        binfile = file_dict['in']
        fd = open( binfile, 'r+' )
        #a = array.array('f', __numarray.transpose(data[:size]).tolist()[0])
        fd.seek( start )
        data[:, :size].tofile( fd )
        fd.close()
        
    def book( self, header ):
        'not tested'
        header = str( header )
        f = open( header )
        L = f.read()
        return L
    
    def writeattr( self, header, vector_dict, file_dict ):
        'not tested'
        file_dict = dict( file_dict )
        if file_dict.has_key( 'in' ):
            del file_dict['in']
        if file_dict.has_key( 'data_format' ):
            del file_dict['data_format']
        for i in range( 1, len( vector_dict['dim'] )+1 ):
            file_dict['n%s'%i] = vector_dict['dim'][i-1]
        fd=self.readattr( header )
        for item in fd.items():
            try:
                if file_dict[item[0]] == item[1]:
                    del file_dict[item[0]]
            except:
                pass
        book=''
        for item in file_dict.items():
            book += "\t%s=%s\n" %( item[0], item[1] )
        fd = open( header, 'r+' )
        fd.seek( 0, 2 )
        fd.write( book )
        fd.close()
    
    def write( self, header, data, book ):
        'not tested'
        header = str( header )
        fd = open( header, 'w' )
        fd.write( book )
        fd.close()
        dict = self.readattr( header )
        fd = open( dict['in'], 'w' )
        fd.close()
        self.writebin( header, data )
        
    def get_data( self, nodename ):
        
        data = self.data
        if self.is_global:
            loc = self.get_data_loc( 'localhost' )
        else:
            loc = self.get_data_loc( nodename )
        
        return join( loc, data )
    
    
    def get_data_loc(self, nodename):
        
        if nodename == 'localhost':
            path = self.env['slimvars']['globaltmpdir']
        else:
            path = self.env['slimvars']['localtmpdir']
        
        node_info = self._node_info.setdefault(nodename,{})
        path = node_info.setdefault( 'location',path )
        
        return path
        
    def diagnostic(self, nodename=None ):
        """
        run a check if this data is valid 
        """
        log = self.env['record'](1,'cmd','err')
        log2 = self.env['record'](2,'diagnostic')
        print >> log
        print >> log, "Runnind diagnostic on data %s" %self
        print >> log
        
        acmd = self.ATTRMD.substitute( attr=self.SFATTR, 
                                       file=str(self), 
                                       want='all',
                                       lval=2 )
        
        if nodename is None:
            nodename = list(self.nodenames)
        elif isinstance(nodename, str):
            nodename = [nodename]
        
        did_run = False
        for node in nodename:
            did_run = True            
            attr_command = Unix_Pipes.CreateComand([acmd], node)
            print >> log2 , attr_command
            p0 = Popen( attr_command, shell=True, stderr=_STDOUT,stdout=__PIPE__)
            ret = p0.wait( )
            
            lines = p0.stdout.read( )
            print >> log2, lines
            if ret:        
                print >> log , 'Error running Diagnostic on data "%(self)s"' %vars(  )
                return False
            else:
                print >> log , 'File "%(self)s" is OK.' %vars(  )

        return did_run
    
         
