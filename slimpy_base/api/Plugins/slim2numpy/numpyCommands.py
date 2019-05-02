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

"""
Vector Interface to RSF.
""" 
from slimpy_base.Core.Interface.node import source
from Storage import Storage 
from slimpy_base.Core.Command.Constr import  Constr
from slimpy_base.Core.Command.Tran import  Tran 
from slimpy_base.Core.Command.CommandMap import CommandMap
try:
    import numpy
except ImportError:
    numpy = None
store = Storage()
class numpyCommandFactory(object):
    
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
    
    
    def add(self,cmnd,**dict):
        self.__setattr__(cmnd,dict)



    def parse(self,command):
        # Update all commands to run on the ooc_driver
        command.update(map=CommandMap(function=command.name,finalize={"Cmnd":None}))

        if self.__dict__.has_key(command.name):
            
            sfdict = self.__getattribute__(command.name)
            
            command.update(**sfdict)
        else:
            pass
    
def addfunc(*p,**k):
    
    if len(p) == 2:
        val = p[1]
    elif k.has_key('val'):
        val = k['val']
    print k['Target'], '=' , p[0],"+",val
    store[k['Target']] = numpy.ndarray.__add__(p[0],val)
    

def addAll():


    numpyFactory = numpyCommandFactory()
    
    numpyFactory.add('add',
                    map = CommandMap(function=addfunc,
                                     pmap=[source]),
                    unusedSource=True
                    )
    """
    sfFactory.addNew("create",
                    map = CommandMap(kmap1={'out':'output',"data_type":'type'},
                                     pmap1=[sfExec('sfmath')] ,
                                     keep1=['output','type','n1','n2','n3','n4','n5'],
                                     pmap2=[sfExec('sfput')],
                                     discard2=['out','data_type','n1','n2','n3','n4','n5']
                                     )
                     )
    
    sfFactory.addNew("fft1",
                    map = CommandMap(pmap=[sfExec('sffft1')] ,
                                     funcs = [truefalseHelper(),CommandMap.addKparam(inv='n')]),
                    InSpaceConstr =  Constr(match=Constr.match(data_type='float') ),
                    PTransform = Tran(Tran.change(data_type='complex'),
                                      Tran.evalChange(n1_fft="space['n1']",n1="int(ceil(space['n1']/2.)+1)")) )
    
    sfFactory.addNew("fft1Adj",
                    map = CommandMap(pmap=[sfExec('sffft1')] ,
                                     funcs = [truefalseHelper(),CommandMap.addKparam(inv='y')]),
                    InSpaceConstr =  Constr(match=Constr.match(data_type='complex') ),
                    PTransform = Tran(Tran.change(data_type='float'),
                                      Tran.evalChange(n1="space['n1_fft']")))

    sfFactory.addNew("fft",
                    map = CommandMap(pmap=[sfExec('sffft3')] ,
                                     funcs = [truefalseHelper()]))
    sfFactory.addNew("transp",
                    map = CommandMap(pmap=[sfExec('sftransp')] ,
                                     funcs = [transphelper]))
    
    
    sfFactory.addNew("cmplx",
                    map = CommandMap(pmap=['sfcmplx' , source ] ),
                    unusedSource=True)
    """
    
def transphelper(params,kparams):
    kparams = kparams.copy()
    plane = kparams['plane']
    kparams['plane'] = '%s%s' %(plane[0],plane[1])
    return params , kparams

