"""
This is the Solve Builder, More doc to come
"""
from slimproj_core.builders.CreateBuilders import CreateSLIMpyBuilder
from slimproj_core.builders.NewSolve import SolveBuilder

def generate(env):
    
    solve_build = CreateSLIMpyBuilder( "Solve", SolveBuilder )
    
    env['BUILDERS']['Solve'] = solve_build
    

def exists(env):
    return 1
