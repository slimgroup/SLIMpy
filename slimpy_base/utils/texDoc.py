
"""
latex documentation tool
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
import sys
from pydoc import ( Doc, TextRepr, join , split, rstrip, classname, 
                   inspect, splitdoc, visiblename, 
                   isdata, strip, deque, 
                   _split_list, ispackage )

import __builtin__ , os, re

class TexDoc( Doc ):
    """Formatter class for text documentation."""

    # ------------------------------------------- text formatting utilities

    _repr_instance = TextRepr()
    repr = _repr_instance.repr

    def bold( self, text ):
        """Format a string in bold by overstriking."""
        return "\\textbf{ %s }" %text
    
    def italic( self, text ):
        """Format a string in bold by overstriking."""
        return "\\textit{ %s }" %text      
    
    def texttt( self, text ):
        return "\\texttt{ %s }" %text
    
    
    
    def classdesc( self, classname, text ):
        classname= makeLatexSafe( classname )
        
        return ( "\\section{\\module{%(classname)s}}\n"
                "\declaremodule{standard}{%(classname)s}{%(classname)s}\n"
                "\\begin{classdesc*} {%(classname)s}\n" 
                "%(text)s\n" 
                "\n\\end{classdesc*}" %vars() )
        
    def funcdesc( self, name, parameters, text ):
        name= makeLatexSafe( name )
        parameters= makeLatexSafe( parameters )
        
        #text = makeLatexSafe(text)
        
        parameters=parameters.replace( '(', '' )
        parameters=parameters.replace( ')', '' )
        parameters = parameters.split( ',' )
        parameters.remove( 'self' )
        parameters = ",".join( parameters )
        
        return ( "\\begin{funcdesc} {%(name)s}{%(parameters)s}\n"
                "%(text)s\n"
                "\n\\end{funcdesc}" %vars() )
    
    def itemize( self, List ):
        items = "\n\\item[] "+"\n\\item[] ".join( List )
        
        return "\\begin{itemize}\n %(items)s\n\\end{itemize}" %vars()


    def indent( self, text, prefix='    ' ):
        """Indent text by prepending a given prefix to each line."""
        if not text: return ''
        lines = split( text, '\n' )
        lines = map( lambda line, prefix=prefix: prefix + line, lines )
        if lines: lines[-1] = rstrip( lines[-1] )
        return join( lines, '\n' )

    def section( self, title, contents ):
        """Format a section with a given heading."""
        return "\\section{ " + title + '}\n' + rstrip( self.indent( contents ) ) + '\n'

    def paragraph( self, title, contents ):
        """Format a section with a given heading."""
        return "\\paragraph{ " + title + '}\n' + rstrip( self.indent( contents ) ) + '\n'

    # ---------------------------------------------- type-specific routines

    def formattree( self, tree, modname, parent=None, prefix='' ):
        """Render in text a class tree as returned by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type( entry ) is type( () ):
                c, bases = entry
                result = result + prefix + classname( c, modname )
                if bases and bases != ( parent, ):
                    parents = map( lambda c, m=modname: classname( c, m ), bases )
                    result = result + '(%s)' % join( parents, ', ' )
                result = result + '\n'
            elif type( entry ) is type( [] ):
                result = result + self.formattree( 
                    entry, modname, c, prefix + '    ' )
        return result

    def docmodule( self, object, name=None, mod=None ):
        """Produce text documentation for a given module object."""
        name = object.__name__ # ignore the passed-in name
        synop, desc = splitdoc( getdoc( object ) )
        result = self.section( name, synop )

        try:
            all = object.__all__
        except AttributeError:
            all = None

        try:
            file = inspect.getabsfile( object )
        except TypeError:
            file = '(built-in)'
        result = result + self.paragraph( 'File', file )

        if desc:
            result = result + self.section( 'Description', desc )

        classes = []
        for key, value in inspect.getmembers( object, inspect.isclass ):
            # if __all__ exists, believe it.  Otherwise use old heuristic.
            if ( all is not None
                or ( inspect.getmodule( value ) or object ) is object ):
                if visiblename( key, all ):
                    classes.append( ( key, value ) )
        funcs = []
        for key, value in inspect.getmembers( object, inspect.isroutine ):
            # if __all__ exists, believe it.  Otherwise use old heuristic.
            if ( all is not None or
                inspect.isbuiltin( value ) or inspect.getmodule( value ) is object ):
                if visiblename( key, all ):
                    funcs.append( ( key, value ) )
        data = []
        for key, value in inspect.getmembers( object, isdata ):
            if visiblename( key, all ):
                data.append( ( key, value ) )

        if hasattr( object, '__path__' ):
            modpkgs = []
            for file in os.listdir( object.__path__[0] ):
                path = os.path.join( object.__path__[0], file )
                modname = inspect.getmodulename( file )
                if modname != '__init__':
                    if modname and modname not in modpkgs:
                        modpkgs.append( modname )
                    elif ispackage( path ):
                        modpkgs.append( file + ' (package)' )
            modpkgs.sort()
            result = result + self.section( 
                'Package Contents', join( modpkgs, '\n' ) )

        if classes:
            classlist = map( lambda ( key, value ): value, classes )
            contents = []
            for key, value in classes:
                contents.append( self.document( value, key, name ) )
            result = result + self.paragraph( 'Classes', "\n\\begin{itemize}\n\\item[] "+join( contents, '\n\\item[] ' ) +'\n\\end{itemize}' )

        if funcs:
            contents = []
            for key, value in funcs:
                contents.append( self.document( value, key, name ) )
            result = result + self.paragraph( 'Functions', join( contents, '\n' ) )

        if data:
            contents = []
            for key, value in data:
                contents.append( self.docother( value, key, name, 70 ) )
            result = result + self.paragraph( 'Data', join( contents, '\n' ) )

        if hasattr( object, '__version__' ):
            version = str( object.__version__ )
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip( version[11:-1] )
            result = result + self.paragraph( 'Version', version )
        if hasattr( object, '__date__' ):
            result = result + self.paragraph( 'Date', str( object.__date__ ) )
        if hasattr( object, '__author__' ):
            result = result + self.paragraph( 'Author', str( object.__author__ ) )
        if hasattr( object, '__credits__' ):
            result = result + self.paragraph( 'Credits', str( object.__credits__ ) )
        return result

    def docclass( self, object, name=None, mod=None ):
        """Produce tex documentation for a given class object."""
        realname = object.__name__
        name = name or realname
        bases = object.__bases__

        def makename( c, m=object.__module__ ):
            return classname( c, m )

        if name == realname:
            title = self.texttt( 'class ' + realname )
        else:
            title = self.texttt( name + ' = class ' + realname )
        if bases:
            parents = map( makename, bases )
            title = title + '(%s)' % join( parents, ', ' )

        doc = getdoc( object )
        contents = doc and [doc + '\n'] or []
        push = contents.append

        # List the mro, if non-trivial.
        mro = deque( inspect.getmro( object ) )
#        if len(mro) > 2:
#            push("Method resolution order:")
#            for base in mro:
#                push('    ' + makename(base))
#            push('')

        #  class to pump out a horizontal rule between sections.
        class HorizontalRule:
            def __init__( self ):
                self.needone = 0
            def maybe( self ):
                if self.needone:
                    push( '%' * 40 )
                self.needone = 1
        hr = HorizontalRule()

        def spill( msg, attrs, predicate ):
            ok, attrs = _split_list( attrs, predicate )
            if ok:
                hr.maybe()
                #push(msg)
                docstr = []
                for name, kind, homecls, value in ok:
                    if name.startswith( '__' ) and name.endswith( '__' ):
                        pass
                    else:
                        docstr.append( self.document( getattr( object, name ), 
                                            name, mod, object ) )
                push( "\n".join( docstr ) )
                    
            return attrs

        def spillproperties( msg, attrs, predicate ):
            ok, attrs = _split_list( attrs, predicate )
            if ok:
                hr.maybe()
                push( msg )
                for name, kind, homecls, value in ok:
                    push( self._docproperty( name, value, mod ) )
            return attrs

        def spilldata( msg, attrs, predicate ):
            ok, attrs = _split_list( attrs, predicate )
            if ok:
                hr.maybe()
                push( msg )
                for name, kind, homecls, value in ok:
                    if callable( value ) or inspect.isdatadescriptor( value ):
                        doc = getdoc( value )
                    else:
                        doc = None
                    push( self.docother( getattr( object, name ), 
                                       name, mod, 70, doc ) + '\n' )
            return attrs

        attrs = filter( lambda ( name, kind, cls, value ): visiblename( name ), 
                       inspect.classify_class_attrs( object ) )
        while attrs:
            if mro:
                thisclass = mro.popleft()
            else:
                thisclass = attrs[0][2]
            attrs, inherited = _split_list( attrs, lambda t: t[2] is thisclass )

            if thisclass is __builtin__.object:
                attrs = inherited
                continue
            elif thisclass is object:
                tag = "defined here"
            else:
                tag = "inherited from %s" % classname( thisclass, 
                                                      object.__module__ )
            filter( lambda t: not t[0].startswith( '_' ), attrs )

            # Sort attrs by name.
            attrs.sort()

            # Pump out the attrs, segregated by kind.
            attrs = spill( "Methods %s:\n" % tag, attrs, 
                          lambda t: t[1] == 'method' )
            attrs = spill( "Class methods %s:\n" % tag, attrs, 
                          lambda t: t[1] == 'class method' )
            attrs = spill( "Static methods %s:\n" % tag, attrs, 
                          lambda t: t[1] == 'static method' )
#            attrs = spillproperties("Properties %s:\n" % tag, attrs,
#                                    lambda t: t[1] == 'property')
#            attrs = spilldata("Data and other attributes %s:\n" % tag, attrs,
#                              lambda t: t[1] == 'data')
#            assert attrs == []
#            attrs = inherited

        contents = '\n'.join( contents )
        if not contents:
            return title + '\n'
        return self.classdesc( realname, '\n' + self.indent( rstrip( contents ), '   ' ) )

    def formatvalue( self, object ):
        """Format an argument default value as text."""
        return '=' + self.repr( object )

    def docroutine( self, object, name=None, mod=None, cl=None ):
        """Produce text documentation for a function or method object."""
        realname = object.__name__
        name = name or realname
        note = ''
        skipdocs = 0
        if inspect.ismethod( object ):
            imclass = object.im_class
            if cl:
                if imclass is not cl:
                    note = ' from ' + classname( imclass, mod )
            else:
                if object.im_self:
                    note = ' method of %s instance' % classname( 
                        object.im_self.__class__, mod )
                else:
                    note = ' unbound %s method' % classname( imclass, mod )
            object = object.im_func

        if name == realname:
            title = realname
        else:
            if ( cl and realname in cl.__dict__ and
                cl.__dict__[realname] is object ):
                skipdocs = 1
            title = name + ' = ' + realname
        if inspect.isfunction( object ):
            args, varargs, varkw, defaults = inspect.getargspec( object )
            argspec = inspect.formatargspec( 
                args, varargs, varkw, defaults, formatvalue=self.formatvalue )
            if realname == '<lambda>':
                title = 'lambda'
                argspec = argspec[1:-1] # remove parentheses
        else:
            argspec = '(...)'
        #decl = self.texttt(title + argspec + note + ":")


        if skipdocs:
            text = '\n'
        else:
            doc = getdoc( object ) or ''
            text= ( doc and rstrip( self.indent( doc ) ) + '\n' )

        return self.funcdesc( title, argspec, text )

    def _docproperty( self, name, value, mod ):
        results = []
        push = results.append

        if name:
            push( name )
        need_blank_after_doc = 0
        doc = getdoc( value ) or ''
        if doc:
            push( self.indent( doc ) )
            need_blank_after_doc = 1
        for attr, tag in [( 'fget', '<get>' ), 
                          ( 'fset', '<set>' ), 
                          ( 'fdel', '<delete>' )]:
            func = getattr( value, attr )
            if func is not None:
                if need_blank_after_doc:
                    push( '' )
                    need_blank_after_doc = 0
                base = self.document( func, tag, mod )
                push( self.indent( base ) )

        return '\n'.join( results )

    def docproperty( self, object, name=None, mod=None, cl=None ):
        """Produce text documentation for a property."""
        return self._docproperty( name, object, mod )

    def docother( self, object, name=None, mod=None, maxlen=None, doc=None ):
        """Produce text documentation for a data object."""
        repr = self.repr( object )
        if maxlen:
            line = ( name and name + ' = ' or '' ) + repr
            chop = maxlen - len( line )
            if chop < 0: repr = repr[:chop] + '...'
        line = ( name and self.bold( name ) + ' = ' or '' ) + repr
        if doc is not None:
            line += '\n' + self.indent( str( doc ) )
        return line

def getdoc( object ):
    """Get the doc string or comments for an object."""
    result = inspect.getdoc( object ) or inspect.getcomments( object )
    res = result and re.sub( '^ *\n', '', rstrip( result ) ) or ''
    
    return makeLatexSafe( res )

def makeLatexSafe( text ):
    texmap = [( '\\', '\\e ' ), ( '{', '\\{' ), ( '}', '\\}' ), ( '_', '{\\_}' )]
    
    if '--latex' in text:
        return text
    else:
        for key, val in texmap:
            text = text.replace( key, val )
        return text


latex = TexDoc()
# --------------------------------------------------------- user interfaces

if __name__ == "__main__":
    if len( sys.argv ) == 1:
        print 'usage python texDoc.py moule class'
    else:
        item = sys.argv[1]
        From = sys.argv[2]
    
        x = __import__( item, globals(), locals(), From )
        
        k = getattr( x, From )
    
    print latex.document( k )

