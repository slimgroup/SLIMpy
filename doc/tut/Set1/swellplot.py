
from rsfproj import Flow, Plot, End, Result

graphit = lambda title=None, min=-0.25, max=0.25: 'graph title="%(title)s" min2=%(min)s max2=%(max)s' %vars()
def plot_swell( data, noise, sig , enoise, esig, residual=None):
    
#    Flow( esig, [enoise, data] , 'math x=${SOURCES[1]} output="x-input"')
    
    
    Plot( 'enoise', enoise,       graphit( title="Estimated Swell Noise") )
    Plot( 'noise',noise,  graphit( title="True Swell Noise")      )
    
    Plot( 'esig',esig,         graphit( title="Estimated Signal" )     ) 
    Plot('sig',sig,       graphit( title="True Signal" )          )
    
    
    Result('plot1',['sig','esig'],              'SideBySideAniso' )
    Result('plot2',['noise','enoise'],          'SideBySideAniso' )
    
    if residual:
        Plot('residual',residual,       graphit( title="Residual" ) )
        Result('plot3',[esig,enoise,residual],'SideBySideAniso' )
    
    End()

