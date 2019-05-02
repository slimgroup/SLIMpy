"""
Helper functions for the 2d and 3d Curvelet Converter 
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


from slimpy_base.api.Plugins.slim2rsf.rsfContainer import rsf_data_container
from slimpy_base.Environment.InstanceManager import InstanceManager
from os.path  import join, isfile
from string import Template
from subprocess import Popen, PIPE
from slimpy_base.Core.Command.Drivers.Unix_Pipes import Unix_Pipes



__env__ = InstanceManager()
    
SFFDCT2 = lambda:join( __env__['slimvars']['RSFBIN'] , 'sffdct2' )

SFMATH =  lambda:join( __env__['slimvars']['RSFBIN'] , 'sfmath' )

MATHCMD_2D = Template( "true | ${math} n1=${n1} n2=${n2} output=0" )
MAPONLY_2D = Template( "${SFFDCT} nbs=${nbs} "
                       "nba=${nba} ac=${ac} maponly=y > ${sizes}" )

curvelets = {}

def GetShapeInv( command ,space):
    
    nba = command['nba']
    nbs = command['nbs']
    ac  = command['ac']
    
    
    key = (nba,nbs,ac)
    if curvelets.has_key(key):
        ck = curvelets[key]
        mshape = tuple(space.shape)
        if ck.has_key( mshape ):
            return ck[ mshape ]
        
    raise Exception( "could not predict sizes" ) 

def GetShapeFwd( command ,space ):
    

    nba = command['nba']
    nbs = command['nbs']
    ac  = command['ac']
    
    n1 = space.shape[0]
    n2 = space.shape[1]
    
    key = (nba,nbs,ac)
    if curvelets.has_key(key):
        ck = curvelets[key]
        mshape = tuple(space.shape)
        if ck.has_key( mshape ):
            return ck[ mshape ] 
        
    if not isfile( SFFDCT2() ):
        raise EnvironmentError( "could not find file 'sffdct2' " )
    if not isfile( SFMATH() ):
        raise EnvironmentError( "could not find file 'sfmath' " )
    
    
    sizes = join ( __env__['slimvars']['globaltmpdir'] , 'sizes.rsf' )
    
    MATH = MATHCMD_2D.substitute( math=SFMATH(), n1=n1, n2=n2 )
    cmd = MAPONLY_2D.substitute(  SFFDCT=SFFDCT2(), nba=nba, nbs=nbs, ac=ac, sizes=sizes )
    
    sizes_command = Unix_Pipes.CreateComand([MATH,cmd], 'localhost', 
                                            is_local=[None,False],
                                            is_tmp=[None,True] )
    
    print >> __env__['record']( 5, 'cmd','sizes' ) , sizes_command
    p0 = Popen( sizes_command, shell=True, stderr=PIPE )
    
    retcode = p0.wait()
    if retcode:
        out = p0.stderr.read()
        raise Exception( "Command: '%(cmd)s' failed\n%(out)s" %vars() )
    
    sizes_cont = rsf_data_container( sizes )
    shape = sizes_cont.params.shape
    
    sizes_cont.rm()
    
    ck = curvelets.setdefault( key, {} )
    ck[ (n1,n2) ] = shape
    ck[ tuple(shape) ] = (n1,n2) 
    return shape


#===============================================================================
# #############################################################################    
#===============================================================================
SFFDCT3 = lambda:join( __env__['slimvars']['RSFBIN'] , 'sffdct3' )
MATHCMD_3D = Template( "true | ${math} n1=${n1} n2=${n2} n3=${n3} output=0" )
MAPONLY_3D = Template( "${SFFDCT} nbs=${nbs} nbd=${nbd} "
                       "ac=${ac} maponly=y > ${sizes}" )

curvelets3 = {}


def GetShapeInv3d( command ,space):
    
    nbd = command['nbd']
    nbs = command['nbs']
    ac  = command['ac']
    
    
    key = (nbd,nbs,ac)
    if curvelets.has_key(key):
        ck = curvelets[key]
        mshape = tuple(space.shape)
        if ck.has_key( mshape ):
            return ck[ mshape ]
        
    raise Exception( "could not predict sizes" ) 

def GetShapeFwd3d( command ,space ):
    

    nbd = command['nbd']
    nbs = command['nbs']
    ac  = command['ac']
    
    n1 = space.shape[0]
    n2 = space.shape[1]
    n3 = space.shape[2]
    
    key = (nbd,nbs,ac)
    if curvelets.has_key(key):
        ck = curvelets[key]
        mshape = tuple(space.shape)
        if ck.has_key( mshape ):
            return ck[ mshape ] 
        
    if not isfile( SFFDCT3() ):
        raise EnvironmentError( "could not find file 'sffdct2' " )
    if not isfile( SFMATH() ):
        raise EnvironmentError( "could not find file 'sfmath' " )
    
    
    sizes = join ( __env__['slimvars']['globaltmpdir'] , 'sizes3d.rsf' )
    
    MATH = MATHCMD_3D.substitute( math=SFMATH(), n1=n1, n2=n2, n3=n3 )
    cmd = MAPONLY_3D.substitute(  SFFDCT=SFFDCT3(), nbd=nbd, nbs=nbs, ac=ac, sizes=sizes )
    
    sizes_command = Unix_Pipes.CreateComand([MATH,cmd], 'localhost', 
                                            is_local=[None,False],
                                            is_tmp=[None,True] )
    
    print >> __env__['record']( 5, 'cmd','sizes' ) , sizes_command
    p0 = Popen( sizes_command, shell=True, stderr=PIPE )
    
    retcode = p0.wait()
    if retcode:
        out = p0.stderr.read()
        raise Exception( "Command: '%(cmd)s' failed\n%(out)s" %vars() )
    
    sizes_cont = rsf_data_container( sizes )
    shape = sizes_cont.params.shape
    
    sizes_cont.rm()
    
    ck = curvelets.setdefault( key, {} )
    ck[ tuple(space.shape) ] = shape
    ck[ tuple(shape) ] = tuple(space.shape) 
    return shape


