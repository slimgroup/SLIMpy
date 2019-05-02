#!/usr/bin/env python
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

import unittest
#from slimpy_base.api.Plugins.slim2rsf import rsf_data_container



class TestRSFcommand(unittest.TestCase):
    
    def setUp(self):
        pass 
    
    def testInit(self):
        pass
    
    def testparamMap(self):
        pass
 
    def testKparam_map(self):
        pass
    
    def testFormat(self):
        pass
    
    def testTransform(self):
        pass


class TestRSFContainer(unittest.TestCase):
    
    def setUp(self):
        pass 
    
    def testisCompatibleWith(self):
        pass

    def testisempty(self):
        pass
        
    def testparse(self):
        pass

    def testsetname(self):
        pass

    def testremove(self):
        pass

    def testreadattr(self):
        pass
            
    def testreadbin(self):
        pass
    
    def testwritebin(self):
        pass
    
    def testbook(self):
        pass
    
    def testwriteattr(self):    
        pass
    
    def testwrite(self):
        pass
    
    def testgetfilepos(self):
        pass


def sfCommSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestRSFcommand)

def ContainerSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestRSFContainer)

def suite():
    return unittest.TestSuite([sfCommSuite(),ContainerSuite()])

if __name__ == '__main__':
    unittest.main()
