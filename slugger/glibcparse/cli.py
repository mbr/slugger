"""A script to extract glibc localedata.

Woefully under documented. All its components are found in the glibcparse
package. If you need a parser for glibc locale files for some reason, this is
not a bad starting point. Message me on <https://github.com/mbr/slugger> for
help.
"""

import bz2
import os
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

import click
import logbook
import logbook.more
from remember.memoize import memoize

from .tokenize import Tokenizer
from .preprocess import Screener
from .parser import TranslitParser
from .exc import LException

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
            return parse_translit(full_fn)[0]

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

        return p.ttbl, p


@click.command(
    help=('Parses the provided files, calculates translation tables and '
          'writes bzip\'ed pickled files to disc.')
)
@click.option('--debug', '-d', 'loglevel', flag_value=logbook.DEBUG)
@click.option('--quiet', '-q', 'loglevel', flag_value=logbook.WARNING)
@click.option('--preprocess-only', '-E', is_flag=True,
              help='Preprocess only (used to test comment-stripping and '
                   'newline folding.')
@click.option('--output-dir', '-o',
              default=os.path.join(
                  os.path.dirname(__file__), '..', 'localedata'
              ),
              type=click.Path(exists=True, file_okay=False, writable=True,
                              readable=False),
              help='The directory where generated output should be stored. '
                   'Defaults to [slugger]/localedata.')
@click.option('--compress/--no-compress', '-c/-C', default=True,
              help='Compress resulting pickled files (default: enabled).')
@click.argument('files', nargs=-1, required=True,
                type=click.Path(exists=True, dir_okay=False, writable=False))
def main(**kwargs):
    return _main(**kwargs)


def _main(loglevel, preprocess_only, output_dir, files, compress):
    if loglevel is None:
        loglevel = logbook.INFO

    handler = logbook.more.ColorizedStderrHandler(level=loglevel)
    with logbook.NullHandler().applicationbound(), handler.applicationbound():
        log.info('Storing output in %s' % output_dir)

        for fn in files:
            if preprocess_only:
                with open(fn) as f:
                    for c in Screener(f.read()):
                        sys.stdout.write(c)
            else:
                ttbl, parser = parse_translit(fn)
                if not parser.has_LC_IDENITIFCATION:
                    log.warning('No LC_IDENTIFICATION in "%s", skipping' %
                                fn)
                else:
                    ext = '.ttbl' if not compress else '.ttbl.bz2'
                    out_fn = os.path.join(
                        output_dir,
                        os.path.basename(fn) + ext)
                    log.info('Writing output to %s' % out_fn)

                    outfile = open(out_fn, 'w') if not compress else\
                        bz2.BZ2File(out_fn, 'w', 1024**2, 9)
                    try:
                        pickle.dump(ttbl, outfile, pickle.HIGHEST_PROTOCOL)
                    finally:
                        outfile.close()
