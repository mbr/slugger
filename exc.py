#!/usr/bin/env python
# coding=utf8


class LException(Exception):
    def __init__(self, src, err):
        super(LException, self).__init__('%d.%d %s' % (
            src.lineno, src.colno, err
        ))


class TokenizerError(LException):
    pass
