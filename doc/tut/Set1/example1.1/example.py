"""
This is the very first example you should look at when learning SLIMpy
@page es1step1 Step 1
\par Objectives: 
 - get SLIMpy ready to use
 - become familiar with the python syntax
 - do a simple non-iterative de-noise with surfacelets
@section setup Setup 
 Now that you have acquired SLIMpy 
you should 
\ref configure_slimpy "configure" 
it using the configure_slimpy.py script this creates a .slimpy_rc file in your home directory
@section walkthrough Walkthrough

@par Preamble

@code
>>> from SLIMpy import *
@endcode
Include the SLIMpy package into the current python module.
    
@code

>>> options = parse_args( )

@endcode

\ref SLIMpy.setup.parse_args "parse_args"  
tells SLIMpy that it is working as a command line program and to
enable the SLIMpy command line arguments. 
    
parse_args initializes SLIMpy. This produces the following output 
@code

SLIMpy: Building AST ...

@endcode

@code

>>> sig = vector( '../sig.rsf' )
>>> noise = vector( '../swellnoise.rsf' )
>>> data  = sig + noise

@endcode

Here we tell SLIMpy to look at the files `sig.rsf' and 'swellnoise.rsf' as vectors.
\ref slimpy_base.User.adiFactories.VectorFactory "vector" is acutaly a forctory function that creates a 
\ref slimpy_base.Core.User.Structures.serial_vector.Vector "Vector Class" instance.

@code
>>> A = Cosine( sig.space )
@endcode
This creates an implicit linear operator representing the 
\ref slimpy_base.api.linearops.contourlets.surf "Surfacelet Transform".

@par Body

@code
>>> tmp1 = A * data
>>> tmp2 = tmp1.thr( 0.0001 )
>>> res = A.H * tmp2 
@endcode

These line represents the body of the code. this is where slimpy makes it easy
for the user to create a flow.

@par Finalize

@code
>>> data.setName('data')
>>> res.setName( "res" )
@endcode

The command 
\ref slimpy_base.Core.User.Structures.serial_vector.Vector.setName "setName"
tells SLIMpy that the vector res is a
target to be built and kept.

\note that the previous lines two produce NO output because there is no actual work
done here since SLIMpy is still in the ``Build AST'' mode.

@code
    >>> Execute( )
@endcode

\ref slimpy_base.Environment.InstanceManager.InstanceManager.Execute "Execute"
 is where the work is done, it produces the following lines of output:
     
@code
SLIMpy: Done building AST 
SLIMpy: Executing commands ... 
true | sfmath type="float" n2="256" n1="256" output="0" | 
       sfput label1="Time" label2="Lateral" var="0.0002" unit2="km" unit1="s" d1="0.004" d2="0.032" o2="0" o1="0" | 
       DATAPATH=./ sfnoise mean="0" > ./slim.18526.env1.exampl.creat.00001.rsf 
< ./sig.rsf DATAPATH=./ sfmath output="vec+input" vec="./slim.18526.env1.exampl.creat.00001.rsf" > ./data.rsf 
< ./data.rsf sfsurf adj="n" Pyr_Level="2" | sfthr mode="soft" thr="0.0001" | 
       DATAPATH=./ sfsurf adj="y" Pyr_Level="2" > ./res.rsf 
sync 
sfrm ./slim.18526.env1.exampl.creat.00001.rsf 
SLIMpy: Done executing commands 
@endcode

"""


from SLIMpy import *

# parse the command line  
# fiunuction parse_args enables SLIMpy to recognise --help and other command line options 
options = parse_args( )

# define a vector
sig = vector( '../sig.rsf' )
noise = vector( '../swellnoise.rsf' )
data  = sig + noise


A = Cosine( sig.space )

tmp1 = A * data
tmp2 = tmp1.thr( 0.0001 )
res = A.H * tmp2 

# set the name of the result tells SLIMpy to keep res and data as a final target 
data.setName('data')
res.setName( "res" )

# Run the command built up above
Execute( )


