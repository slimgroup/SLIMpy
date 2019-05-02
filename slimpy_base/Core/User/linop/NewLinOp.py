"""
This is the class for a User Created Linear Operator.
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


from slimpy_base.Core.Interface.Structure import Structure 
from slimpy_base.Core.User.linop.linear_operator import LinearOperator


class NewLinop( Structure, LinearOperator ):
    """
    The base linear operator object should not be called by itself.
    This is an abstract class
    the newlinop class must be subclassed into a concrete class
    
    for example:
    the code:
    
    class fft_user(newlinop):
        command = "fft1"
        params  = ()

        def __init__(self,space,opt='y',inv='n'):
            self.inSpace = space
            self.kparams = dict(opt=opt,inv=inv)
            newlinop.__init__(self)

    #Initialize/Define the User created Linear Operator
    F = fft_user(vec1.getSpace())

    will create a new linear operator that will work on an rsf dataset.
    the variables may be specified in the __init__ function as well
    
    the variables that must be specified are:
        command
        params
        inSpace
        outSpace
        
    optional variables for the adjoint are:
        kparams
        adj_command
        adj_params
        adj_kparams
        
    if the optional variables are not specified then they are assumed to be
    the same voidSpace.
    """
    name = "newlinop"
    command = None
    params = ()
        
    inSpace = None
    outSpace = None
    kparams = {}
    adj_command = None
    outSpace = None
    adj_params = None
    adj_kparams = None
    
    def __init__( self ):
        """
        Initialize the class, checks the inSpace and otuSpace and sets them to voidSpace if needed.
        """
        # init Structure not necissary but to conserve consistancy
        Structure.__init__( self )
#        self.isadj = False
        if self.command is None:
            raise TypeError( "need to define command in operator" )
        
        if self.inSpace is None:
            raise TypeError( "need to define inSpace, use voidSpace if unknown" )
        if self.outSpace is None:
            raise TypeError( "need to define outSpace, use voidSpace if unknown" )
            
        if self.adj_kparams is None:
            self.adj_kparams = self.kparams

        if self.adj_params is None:
            self.adj_params = self.params
            
            
        if self.adj_command is None:
            self.adj_command = self.command
        
        LinearOperator.__init__( self, self.inSpace, self.outSpace , *self.params, **self.kparams )
    
    def adj( self ):
        """
        Overload the adj command because we now have mor variables to worry about
        """
        from copy import copy
        
        t = self.copy()
        
        inSpace = copy( t.inSpace )
        t.inSpace = copy( t.outSpace )
        t.outSpace = inSpace
        
        t.isadj = not self.isadj
        
        kparams = copy( t.kparams )
        t.kparams = t.adj_kparams
        t.adj_kparams = kparams
        
        params = copy( t.params )
        t.params = t.adj_params
        t.adj_params = params
        
        com = t.command
        t.command = t.adj_command
        t.adj_command = com
    
        return t
    
    def applyop( self, other ):
        """
        applies the operator to other
        generates a new instance of the type of other
        """
        return self.generateNew( other, self.command , *self.params, **self.kparams )

    
