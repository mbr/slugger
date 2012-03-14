#!/usr/bin/env python
# coding=utf8

import os
import sys

import logbook
import logbook.more

try:
    from remember.memoize import memoize
    has_memoize = True
except ImportError:
    has_memoize = False

    def memoize(*args, **kwargs):
        def _wrap(f):
            return f
        return _wrap

from tokenize import Tokenizer
from preprocess import Screener
from parser import TranslitParser
from exc import LException

log = logbook.Logger('main')

def parse_translit(fn):
    return _parse_translit(os.path.normpath(os.path.abspath(fn)))

@memoize(100)
def _parse_translit(fn):
    with open(fn) as f:
        log.info("parse %s" % os.path.relpath(fn))
        tok = Tokenizer(Screener(f.read()))
        dirname = os.path.dirname(fn)

        def parse_func(new_fn):
            full_fn = os.path.join(dirname, new_fn)
            return parse_translit(full_fn)

        p = TranslitParser(parse_func, tok)

        try:
            p.parse()
        except LException, e:
            log.critical("%s:%d.%d %s" % (
                fn,
                e.src.lineno,
                e.src.colno,
                e.err
            ))
            sys.exit(1)

        return p.ttbl


if '__main__' == __name__:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('files', metavar='FILE', nargs='+')
        parser.add_argument('--preprocess-only', '-E', action='store_true',
                            default=False)
        parser.add_argument('--debug', '-d', action='store_const',
                            dest='loglevel', const=logbook.DEBUG,
                            default=logbook.INFO)

        args = parser.parse_args()
        logbook.NullHandler().push_application()
        logbook.more.ColorizedStderrHandler(
            level=args.loglevel,
        ).push_application()

        if not has_memoize:
            log.error('You do not have remember (from PyPi) installed. This '\
                      'program will still work, but large jobs will run about'\
                      ' 10x slower')

        for fn in args.files:
            if args.preprocess_only:
                with open(fn) as f:
                    for c in Screener(f.read()):
                        sys.stdout.write(c)
            else:
                ttbl = parse_translit(fn)
