#!/usr/bin/env python
'''
Short auto-documentation for SLIMpy
'''

__copyright__ = """
Copyright 2008 Henryk Modzelewski
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


from string import Template

OPTIONS={
'text':'generate quick and dirty text output (default)',
'html':'generate HTML output to directory (dir-out must be specified)',
'latex':'generate LaTeX output to file',
'help':'this info'
}

# imports
import os
import sys
import getopt
import time
import pickle

# defaults
TITLE='SLIMpy methods and classes'
HEADER={
    'LaTeX': '''\\maketitle''',
    'HTML': '''<HTML><HEAD><TITLE>'''+TITLE+'''</TITLE></HEAD><BODY>\n''',
    'TEXT': '''\n'''
}
FOOTER={
    'LaTeX': '''\n''',
    'HTML': '''<P><I>'''+time.asctime()+'''</I></BODY>\n''',
    'TEXT': '''\n'''+time.asctime()+'''\n'''
}
LINEEND={ 'LaTeX': '\n', 'HTML': '\n', 'TEXT': '\n' }
LINEBREAK={ 'LaTeX': '\n', 'HTML': '<BR>\n', 'TEXT': '\n' }
HLINE={ 'LaTeX': '\n', 'HTML': '<HR>\n', 'TEXT': '#'*30+'\n' }
SECTION={ 'LaTeX': ['\\section*{','}\n'], 'HTML': ['<H3>','</H3>\n'], 'TEXT': ['# ','\n\n'] }
SUBSECTION={ 'LaTeX': ['\\subsection*{','}\n'], 'HTML': ['<H4>','</H4>\n'], 'TEXT': ['### ','\n'] }
ITEMIZE={ 'LaTeX': ['\\begin{itemize}\n','\\end{itemize}\n'], 'HTML': ['<UL>\n','</UL>\n'], 'TEXT': ['\n','\n'] }
ITEM={ 'LaTeX': ['\\item ','\n'], 'HTML': ['<LI>','</LI>\n'], 'TEXT': ['   || ','\n'] }
PARAGRAPH={ 'LaTeX': ['\n','\n'], 'HTML': ['<P>','</P>\n'], 'TEXT': ['','\n'] }

def usage():
    """ print usage info """
    print __doc__
    print os.path.basename(sys.argv[0]), '[options] file-in [file/dir-out]'
    print '\tOptions:'
    options = OPTIONS.keys()
    options.sort()
    for option in options:
        print '\t--'+option,':',OPTIONS[option]
    print '\tNote: formating options are exclusive (last counts)'
    print COPYRIGHT
    sys.exit(2)

def makeSafe(format,text):
    ''' conversion of strings to LaTeX compliant'''
    if format!='LaTeX': return text
    texmap = [('\\','\\e '),('{','\\{'),('}','\\}'),('_','{\\_}'),('%','{\\%}')]
    for key,val in texmap:
        text = text.replace(key,val)
    return text

class l_Section(object):
    
    sec = Template("""
\\section*{${name}: ${perc}\\%}
There are ${all} methods in ${name}: ${tested} tested methods and ${untested} untested 


${perc}{\\%} of ${name} is tested.

${subsections}
    """)
    
    def __init__(self,name,dict):
        
        
        all_methods = dict['all_methods']
        tested_methods = dict['tested_methods']
        doc = dict['doc'] 
        assert tested_methods.issubset( all_methods ), (tested_methods,all_methods)
        untested = all_methods.difference( tested_methods )
        
        if not len(all_methods):
            self.perc = 100
        else:
            self.perc = 100*len(tested_methods) / len(all_methods)
        
        self.name = makeSafe('LaTeX', name)
        untested_sec = sub_section('untested methods: %d' %len(untested), untested, doc )
        tested_sec = sub_section('tested methods: %d' %len(tested_methods), tested_methods, doc )
        
        self.subsections = str(tested_sec) + str( untested_sec )
        self.untested = len(untested)
        self.tested = len(tested_methods)
        self.all = len(all_methods)
    
    def __str__(self):
        
        return self.sec.substitute( **self.__dict__ )
    
class sub_section( object ):
    
    subsec = Template("""
\\subsection*{${name}}
\\begin{itemize}
${items}
\\end{itemize}
 
    """)
    def __init__(self,name, uset, doc):
        self.name = name
        self.uset = uset
        if doc:
            print doc
        self.items = "\n".join([ "\\item[%s] %s" %(item,doc.get(item,"")) for item in self.uset])
    
    def __str__(self):
        if self.uset:
            return self.subsec.substitute( **self.__dict__ )
        else:
            return ""
        

def makeList(Document,Output,FORMAT):
    
    if not Document:
        print "No Profiles were created"
        FileOut=open(Output,'w')
        FileOut.close()
        return
    
    tu = [ (len(val['all_methods']),len(val['tested_methods'])) for val in Document.itervalues()  ]
    
    all,tested = zip(*tu)
    
    all = sum(all)
    tested = sum(tested)
    untested = all - tested
    perc = 100* tested / all 
    
    keys = Document.keys()
    keys.sort()
    funcs = [ str(l_Section(key,Document[key] )) for key in keys ]
    
    FileOut=open(Output,'w')
    print >> FileOut, """%(perc)s \\%% of all SLIMpy classes have been tested

There are a total of  %(all)s class methods: %(tested)s tested and %(untested)s untested""" %vars()

    lines = "\n".join(funcs)
    FileOut.write(lines)
    
    FileOut.close()

    
def _makeList(Document,Output,FORMAT):
    '''
    makeList creates the list of Classes and Methods in either
    TEXT, LaTeX, or HTML format.

    Parameters:
        Document - hash of classes and methods
        Output - string with file/dir name or None
            file for TEXT/LaTeX
            directory for HTML
            None for TEXT/LaTeX to stdout
        FORMAT - either TEXT, LaTeX, or HTML
    '''

    if FORMAT=='HTML':
        if not os.path.isdir(Output):
            print 'FATAL ERROR:', Output, 'does not exist or is not a directory'
            sys.exit(1)
        ContentOut = os.path.join(Output,'index.html')
        try: FileOut=open(ContentOut,'w')
        except:
            print 'FATAL ERROR: cannot open', ContentOut
            sys.exit()
        FileOut.write(HEADER[FORMAT])
        FileOut.write(SECTION[FORMAT][0])
        FileOut.write(TITLE)
        FileOut.write(SECTION[FORMAT][1])
        FileOut.write(HLINE[FORMAT]) 
        FileOut.write(SECTION[FORMAT][0])
        FileOut.write('Table of Contents:')
        FileOut.write(SECTION[FORMAT][1])
        LINKS={}
        names=Document.keys()
        names.sort()
        for name in names:
            LINKS[name]=str('node'+str(len(LINKS)+1000)+'.html')
            FileOut.write(ITEMIZE[FORMAT][0])
            FileOut.write(ITEM[FORMAT][0])
            FileOut.write(''.join(['<A href=\"',LINKS[name],'\">[',name,']</A>']))
            ntested = len(Document[name]['tested_methods'])
            nall = len(Document[name]['all_methods'])
            line = " %.0f%% tested" %(100.*ntested/nall)
            FileOut.write(line)
            FileOut.write(ITEM[FORMAT][1])
            FileOut.write(ITEMIZE[FORMAT][1])
        FileOut.write(FOOTER[FORMAT])
        FileOut.close()
    else:
        if Output:
            try: FileOut=open(Output,'w')
            except:
                'FATAL ERROR: cannot open', Output
                sys.exit(1)
        else: FileOut=sys.stdout
        FileOut.write(HEADER[FORMAT])
    
    names=Document.keys()
    names.sort()
    for name in names:
        section = Document[name]
        used_in = section.setdefault('used in',{})
        doc = section['doc']
    
        if FORMAT=='HTML':
            NodeOut=os.path.join(Output,LINKS[name])
            try: FileOut=open(NodeOut,'w')
            except:
                'FATAL ERROR: cannot open', NodeOut
                sys.exit(1)
            FileOut.write(HEADER[FORMAT])
            FileOut.write(SECTION[FORMAT][0])
            FileOut.write(TITLE)
            FileOut.write(SECTION[FORMAT][1])
            FileOut.write('<A href=\"index.html\">[Back]</A> to Table of Contents')
            FileOut.write(LINEEND[FORMAT])
    
        FileOut.write(HLINE[FORMAT]) 
        FileOut.write(SECTION[FORMAT][0])
        if FORMAT=='HTML': line = ''.join(['<A name=\"',LINKS[name],'\">',name,'</A>'])
        else: line = makeSafe(FORMAT,name)
        FileOut.write(line)
        FileOut.write(SECTION[FORMAT][1])
    
        ntested = len(Document[name]['tested_methods'])
        nall = len(Document[name]['all_methods'])
        line = "There are %s tested methods and %s untested methods in %s" %(ntested,nall-ntested,name)
        line = makeSafe(FORMAT,line)
        FileOut.write(PARAGRAPH[FORMAT][0]+line+PARAGRAPH[FORMAT][1])
#        line = "%.0f%% of the %s is tested" %(100.*ntested/nall, name )
        if nall == 0:
            line = "0%% of the %s is tested" %( name )
        else:
            line = "%.0f%% of the %s is tested" %(100.*ntested/nall, name )
        line = makeSafe(FORMAT,line)
        FileOut.write(PARAGRAPH[FORMAT][0]+line+PARAGRAPH[FORMAT][1])
        FileOut.write(LINEEND[FORMAT])
        
        FileOut.write(SUBSECTION[FORMAT][0]+"tested methods:"+SUBSECTION[FORMAT][1])
        FileOut.write(ITEMIZE[FORMAT][0])
        methods = list(section['tested_methods'])
        methods.sort()
        for method in methods:
            FileOut.write(ITEM[FORMAT][0])
            line = makeSafe(FORMAT,' '.join([method, doc.get(method ,'')]))
            FileOut.write(line)
            FileOut.write(LINEBREAK[FORMAT])
            line = makeSafe(FORMAT,' '.join(["      used in the demos:", used_in.get(method,'')]))
            FileOut.write(line)
            FileOut.write(ITEM[FORMAT][1])
        FileOut.write(ITEMIZE[FORMAT][1])
        
        FileOut.write(SUBSECTION[FORMAT][0]+"untested methods:"+SUBSECTION[FORMAT][1])
        untested_methods = section['all_methods'].difference(section['tested_methods'])
        FileOut.write(ITEMIZE[FORMAT][0])
        methods = list(untested_methods)
        methods.sort()
        for method in methods:
            FileOut.write(ITEM[FORMAT][0])
            line = makeSafe(FORMAT,' '.join([method, doc.get(method ,'')]))
            FileOut.write(line)
            FileOut.write(ITEM[FORMAT][1])
        FileOut.write(ITEMIZE[FORMAT][1])
        FileOut.write(LINEEND[FORMAT])
        
        if FORMAT=='HTML':
            FileOut.write(''.join(['<A href=\"index.html\">[Back]</A> to Table of Contents']))
            FileOut.write(LINEEND[FORMAT])
            FileOut.write(FOOTER[FORMAT])
            FileOut.close()
    
    if FORMAT!='HTML': FileOut.write(FOOTER[FORMAT])
    
    return

# self-execution
if __name__ == '__main__':
    # defaults
    FORMAT='TEXT'

    # get options and arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], '',OPTIONS.keys())
    except getopt.GetoptError:
        print OPTIONS.keys()
        usage()
    
    for o, a in opts:
        if o == '--help': usage()
        if o == '--text': FORMAT='TEXT'
        if o == '--html': FORMAT='HTML'
        if o == '--latex': FORMAT='LaTeX'
    
    if ( len(args) == 0 or len(args) >2):
        print 'FATAL ERROR: too few or too many arguments'
        usage()
    if len(args) > 0:
        FileIn = args[0]
        Output = None
        if len(args) <2 and FORMAT=='HTML':
            print 'FATAL ERROR: no directory for HTML output'
            usage()
    if len(args) > 1:
        Output = args[1]
    
    # get hash table
    pickle_file = open(FileIn)
    Document = pickle.load( pickle_file )
    pickle_file.close()
    
    makeList(Document,Output,FORMAT)

    sys.exit(0)
