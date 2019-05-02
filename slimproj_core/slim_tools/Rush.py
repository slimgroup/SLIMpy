"""
SLIM version of FLow
"""
from subprocess import Popen, PIPE
from os import environ
from os.path import join
#===============================================================================
# GetPar
#===============================================================================    
def get_par_act( target, source, env ):

    par = env['par']
    src = source[0].path
    type = env.get('type',eval)
    get_command = "sfget parform=n %(par)s < %(src)s" %vars()
    print get_command
    p0 = Popen( get_command, shell=True, stdout=PIPE )
    err = p0.wait()
    val = p0.stdout.readline()
    value = type( val )
    print target[0], value
    target[0].write( value )
    return

def get_par_method( self,source, par, *p,**kw ):
    target=self.Value( par )
    return self._GetPar( target, source, par=par, *p, **kw )
    

#===============================================================================
# Rush
#===============================================================================
in_suffix = lambda s:  hasattr(s, 'suffix') and s.suffix in ['.rsf','.xsf']
def rush_gen( source, target, env, for_signature ):
    
    rush_action = env[ 'rush_action' ]
    
    if isinstance(rush_action, str):
        
        if  [s for s in source if in_suffix( s ) ] and env.get( "stdin", 1 ):
            rush_action = "< ${SOURCE} " + rush_action
        if target and env.get( "stdout", 1 ):
            rush_action = rush_action + " > ${TARGET}"
        
        rush_action = rush_action.split(";")
        
    return rush_action

def rush_emitter( target, source, env):
    if target:
        datapath = env.get( 'DATAPATH', '.' )
        for tgt in target:
            if hasattr(tgt,'get_suffix') and tgt.get_suffix() in ['.rsf','.xsf']:
                target.append( join( datapath, tgt.name + "@" ) )
#        elif isinstance( tgt, str) and tgt.endswith(".rsf") or tgt.endswith(".xsf")
#            target.append( join( datapath, tgt.name + "@" ) )

    return target, source

def rush_method( self, target, source, rush_action, *p,**kw ):
    return self._Rush( target, source, rush_action=rush_action, *p, **kw )

    
def gen_suffix(env, sources):
    result = ".rsf"
    for source in sources:
        if in_suffix( source ) :
            result = source.suffix
            break
        
    return result
         

def generate(env):
    
    sfbin = join( environ['RSFROOT'],"bin" )
    
    env.PrependENVPath( 'PATH', sfbin )
    
    GetParBuilder = env.Builder( action=get_par_act,
                              src_suffix=".rsf",
                            )
    
    RushBuilder= env.Builder( generator=rush_gen,
                              suffix=gen_suffix,
                              src_suffix=".rsf",
                              emitter=rush_emitter,
                            )
    
    env["BUILDERS"]['_Rush'] = RushBuilder
    env["BUILDERS"]['_GetPar'] = GetParBuilder
    
    env.AddMethod( rush_method, 'Rush')
    env.AddMethod( get_par_method,'GetPar')
    

def exists(env):
    return 1
