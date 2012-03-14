#!/usr/bin/env python
# coding=utf8

from cStringIO import StringIO
import os
import re
import sys

_U_RE = re.compile('<U([0-9A-F]{4})>')
def _uni_sub(s):
    def _u_repl(m):
        code_point = int(m.group(1), 16)
        return unichr(code_point)

    return _U_RE.sub(_u_repl, s)


class LException(Exception):
    def __init__(self, fn, lineno, err):
        super(LException, self).__init__('%s:%d %s' % (fn, lineno, err))


class LexerError(LException):
    pass


class ParserError(LException):
    @classmethod
    def from_lexer(cls, lex, err):
        return cls(lex.fn, lex.lineno, err)


TOKENS = ('LC_IDENTIFICATION', 'LC_CTYPE', 'LC_COLLATE', 'LC_TIME',
          'LC_NUMERIC', 'LC_MONETARY', 'LC_MESSAGES', 'LC_PAPER', 'LC_NAME',
          'LC_ADDRESS', 'LC_TELEPHONE', 'END', 'escape_char', 'comment_char',
          'translit_start', 'translit_end', 'include', 'copy')

class LocaleLexer(object):
    def _error(self, msg):
        raise LexerError(self.fn, self.lineno, msg)

    def lex(self, f, fn):
        # very half-assed, but there's no docs on the format i can find
        self.f = f
        self.fn = fn
        self.lineno = 0

        self.comment_char = '#'  # the default comment_char seems to be #
        self.escape_char = '\\'  # default escape

        buf = f.read()

        class PutbackIter(object):
            def __init__(self, i):
                self.putback_buf = []
                self.i = i

            def getch(self):
                if self.putback_buf:
                    return self.putback_buf.pop()
                return self.i.next()

            def putback(self, ch):
                self.putback_buf.append(ch)

        def read_char(i):
            c = i.getch()

            if '\n' == c:
                # compress newlines
                while c == '\n':
                    self.lineno += 1
                    self.line_start = True
                    c = i.getch()

                if c == self.comment_char:
                    return read_char(i)
                else:
                    i.putback(c)
                    return '\n'

            elif self.escape_char == c:
                c = i.getch()

                if self.escape_char == c:
                    return self.escape_char

                if '\n' == c:
                    self.lineno += 1  # increase lineno, but don't return
                                      # actual newline
                    return read_char(i)
                # ignore the escape, just return the normal character

            elif self.comment_char == c:
                # FIXME: broken, because of STRINGS
                while i.getch() != '\n':
                    pass
                i.putback('\n')
                return read_char(i)

            return c

        def skip_space(i):
            c = i.getch()

            while c.isspace() and not '\n' == c:
                c = i.getch()

            return c

        i = PutbackIter(iter(buf))
        c = read_char(i)
        word = StringIO()
        self.line_start = True

        while True:
            # string
            if '"' == c:
                c = read_char(i)
                while c != '"':
                    if '\n' == c:
                        self._error("EOL inside string")
                    word.write(c)
                    c = read_char(i)

                yield ('STRING', _uni_sub(word.getvalue()))
                word = StringIO()
                c = read_char(i)
                continue

            # yield EOLs
            if '\n' == c:
                yield ('EOL',)
                c = read_char(i)
                continue

            # skip whitespace
            if c.isspace():
                c = skip_space(i)
                continue

            if c == ';':
                yield ('SEMICOLON',)
                c = read_char(i)
                continue

            if c.isdigit():
                while c.isdigit():
                    word.write(c)
                    c = i.getch()
                yield ('INTEGER', int(word.getvalue()))
                word = StringIO()
                continue

            # consume word
            while True:
                if c in (self.comment_char, '"') or c.isspace() or c == ';':
                    break
                word.write(c)
                c = read_char(i)

            w = word.getvalue()
            word = StringIO()
            if w in TOKENS:
                yield ('KEYWORD', w)

                # changes lexing behavior
                if 'escape_char' == w:
                    self.escape_char = skip_space(i)
                    yield ('WORD', unicode(self.escape_char))
                elif 'comment_char' == w:
                    self.comment_char = skip_space(i)
                    yield ('WORD', unicode(self.comment_char))
            else:
                yield ('WORD', _uni_sub(w))


class BlockParser(object):
    BLOCK_TYPES = ['LC_IDENTIFICATION', 'LC_CTYPE', 'LC_COLLATE', 'LC_TIME',
                   'LC_NUMERIC', 'LC_MONETARY', 'LC_MESSAGES', 'LC_PAPER',
                   'LC_NAME', 'LC_ADDRESS', 'LC_TELEPHONE']
    def parse(self, lexer, lex):
        def _yield_until_end_of(blocktype):
            while True:
                t = lex.next()
                if ('KEYWORD', 'END') == t and lexer.line_start:
                    t = lex.next()
                    if not ('KEYWORD', blocktype) == t:
                        raise ParserError.from_lexer(
                            lexer,
                            'Expected end of %s, got %r instead' % \
                            (blocktype, t)
                        )
                    _expect(lex, 'EOL')
                    # done with the section
                    raise StopIteration

                yield t

        for t in lex:
            if t[0] == 'KEYWORD' and t[1] in self.BLOCK_TYPES:
                handler = getattr(self, 'handle_' + t[1], None)
                gen = _yield_until_end_of(t[1])

                if not handler:
                    for g in gen:
                        print lexer.line_start, g
                        pass  # skip until end
                    print "SKIPPED", t[1]
                else:
                    handler(gen)


def _expect(lex, *args):
    t = lex.next()
    assert args == t[:len(args)], 'Expected %r, got %r instead' % (args, t)
    return t


class TranslitParser(BlockParser):
    def handle_LC_CTYPE(self, lex):
        print "HANDLING LEXER", lex


def parse_file(fn):
    ttbl = {}
    with file(fn) as f:
        lexer = LocaleLexer()
        lex = lexer.lex(f, fn)

        bp = TranslitParser()
        bp.parse(lexer, lex)
    return ttbl


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='+')

    args = parser.parse_args()
    for fn in args.files:
        print "PARSING",fn
        ttbl = parse_file(fn)
