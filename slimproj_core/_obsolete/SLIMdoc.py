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

from SCons.Script import Mkdir,WhereIs,Action
from glob import glob
from os.path import splitext,split,join,abspath
from string import Template
import os
import re

def myAction(cmd_str):
    def act_on(function):
        return Action(function,cmd_str)
    return act_on

term_template = Template("""
\\term{ ${term} }

${abstract}

\\textbf{Author:} ${author}

\\citetitle[${link}]{${term}}
""")

re_title = re.compile(r'\\title\{(.*?)\}')
re_author = re.compile(r'\\author\{(.*?)\}')
default_name = lambda all,def_: all and all[0] or def_
def makedef( file_name, lines , link=None):
    
    head, tail = split( file_name )
    name,ext = splitext( tail )

    #######
    line_less = lines.replace('\n',' ')
    
    all_titles  = re_title.findall( line_less )
    all_authors = re_author.findall( line_less )
    
    term = default_name(all_titles, name)
    
    auth = default_name(all_authors, "No Author" )
    #######
    
    if link is None:
        link = '../%(name)s/index.html' %vars() 
    
    if lines.find("\\begin{abstract}") != -1:
        abstract = lines.split("\\begin{abstract}")[-1].split("\\end{abstract}")[0]
    else:
        abstract = '\\emph{No abstract}'
    
    
    
    return term_template.substitute( term=term, 
                                     abstract=abstract, 
                                     link=link,
                                     author=auth
                                     )
#    return '\\term{ %(term)s }\n %(abstract)s\n\n%(author)s\n\n%(citetitle)s\n' %vars()

def maketut( terms ):
    
    if not terms:
        return "% no terms"
    begin = "\\begin{definitions}"
    end = "\\end{definitions}"
#    terms = "\n".join([open(term).read() for term in glob('%(dir)s/*.term' %vars())])
    terms = "\n".join( [ term.get_contents() for term in  terms] )
    
    return "%(begin)s\n%(terms)s\n%(end)s" %vars()


def how_to_gen( source, target, env, for_signature ):
    
    env.Alias( 'mkhowto', target )
    html_dir = env.get('html_dir',None)
    if html_dir is None:
        name = splitext ( split (str(source[0]))[-1] )[0]
        html_dir = join("#", 'html', name)
    
    dir = env.Dir( html_dir )
    
    MKHOWTO = WhereIs('mkhowto') or os.environ.get('MKHOWTO') 
    MKHOWTO = env.get('MKHOWTO',MKHOWTO)
    env['MKHOWTO'] = MKHOWTO
    
    mk_act = ("${TEXINPUTS and 'TEXINPUTS='}${':'.join(TEXINPUTS)} "
       "${MKHOWTO} --quiet --html --dir=%(dir)s "
       "${ADDRESS and '--address='}${ADDRESS} "
       "${UP_LINK and '--up-link='}${UP_LINK} "
       "${UP_TITLE and '--up-title='}${'\"'+str(UP_TITLE)+'\"'} "
       "${SOURCE}" % vars() )
    
    mk_act_str = "mkhowto --html --dir=${TARGET.dir} "
    mkhowto_action = Action(mk_act,mk_act_str)
    Mkdir( str(dir) )
    return   [mkhowto_action] 
        

def howto_emitter( target, source, env):

    html_dir = env.get('dir',None)
    if html_dir is None:
        name = splitext ( split (str(source[0]))[-1] )[0]
        html_dir = join("#", 'html', name)
        
    index  = join( html_dir , 'index.html' )
    target.pop( )
    target.append( env.File(index) )
    
    dir = str( env.Dir(html_dir) )
    aux = map( abspath, glob( join( dir, "*" ) ) )
    
    for tgt in target:
        abs_tgt = abspath(str(tgt))
        if aux.count( abs_tgt ):
            aux.remove( abs_tgt )
    
    env.SideEffect( aux, target )
    env.Clean( target, aux )
    
    env.Alias( 'mkhowto', target )
    
    return target, source


GLOBAL_TERMS_DEMOS = []
GLOBAL_TERMS_TUTOR = []

add_to_demos = GLOBAL_TERMS_DEMOS.append
add_to_tutorials = GLOBAL_TERMS_TUTOR.append

@myAction("Term Builder( '${SOURCE}' )")
def term_builder(target,source,env):
    link = env.get('link',None)
    text = makedef( str(source[0]), source[0].get_contents() ,link=link )
    fd = open( str(target[0]) , 'w' )
    fd.write( text )
    

def term_emitter( target, source, env ):
#    global GLOBAL_TERMS
#    GLOBAL_TERMS.append( target[0] )

    env.Alias( 'term' , target )
    return target, source

@myAction("Make Index( ['${TARGET}'] )")
def tutorial_index( target, source, env ):
    
    terms = [ src for src in source if src.suffix == '.term']
    text = maketut( terms )
    
    open(str(target[0]) , 'w' ).write( text )


def index_emitter( target, source, env ):
    global GLOBAL_TERMS_TUTOR
    for term in GLOBAL_TERMS_TUTOR:
        source.append( term )
    
    return target, source

def index_emitter_demo( target, source, env ):
    global GLOBAL_TERMS_DEMOS
    
    for term in GLOBAL_TERMS_DEMOS:
        source.append( term )
    return target, source
