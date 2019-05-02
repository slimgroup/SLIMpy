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

def _permute_iter( nested_iter ):
    
    nested_iter = list(nested_iter)
     
    if len( nested_iter ) == 0:
        raise Exception("can not pass in empty list")
    # base case
    elif len( nested_iter ) == 1:
        for item in nested_iter[0]:
            yield [item]
    # recursive case
    else:
        head,tail = nested_iter[0], nested_iter[1:]
        for hitem in head:
            for titems in _permute_iter( tail ):
                yield [hitem] + titems 


def permute_range( shape ):
    return permute( map(xrange, shape))
    
    
def permute( iter_lists , restrict=None, constructor=None ):
    """
    permute( nested_iterable ) -> permutation_genorator
    
    Takes a nested iterator sequence and returns all of the 
    permutaions 
    
    eg. 
    >>> pgen = permute( [[1,2], [3,4] ] )
    >>> for permutaion in pgen:
    >>>     print  permutaion
    [1, 3]
    [1, 4]
    [2, 3]
    [2, 4]

    >>> pgen = permute( dict( a=[1,2], b=[3] ) )
    >>> for permutaion in pgen:
    >>>     print  permutaion
    { 'a':1, 'b':3 }
    { 'a':2, 'b':3 }
    
    if constructor is not None, the output of each genoration is 
    replaced by  permutaion = constructor( permutaion )
    
    if restrict is passed in it may be a callable function
    that evaluates a permutaion and returns True if the 
    permutation needs to be restricted.
    if the first egample passing lambda perm: perm[0] ==  2
    will not generate permutations where permutaion[0] is 2
    i.e. only [1, 3] and [1, 4] are generated
    
    """
    
    if isinstance(iter_lists, dict):
        
        keylist = iter_lists.keys( )
        
        if constructor is None:
            constructor = lambda value_list: dict( zip(keylist,value_list) )
    
        list_of_lists = [ ]
        for key in keylist:
            list_of_lists.append( iter_lists[key] )
    else:
        
        list_of_lists = iter_lists

        if constructor is None:
            constructor = lambda value_list: value_list
    
    if not restrict:
        restrict = lambda permutation: False
    
    for value_list in _permute_iter(list_of_lists):
        permutation = constructor(value_list) 
        if restrict(permutation): 
            continue
        else:
            yield permutation
    
    return
    


