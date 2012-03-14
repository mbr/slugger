#!/usr/bin/env python
# coding=utf8

import sys

from tokenize import Tokenizer
from preprocess import Screener


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='+')

    args = parser.parse_args()
    for fn in args.files:
        with open(fn) as f:
            print "PARSING",fn
            t = Tokenizer(Screener(f.read()))

            for i in t:
                pass
