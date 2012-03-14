#!/usr/bin/env python
# coding=utf8

import bz2
import imp
import re
import os
import sys

import pkg_resources
from remember.memoize import memoize

from exc import LanguageNotFoundError
import languages

try:
    import cPickle as pickle
except ImportError:
    import pickle


_LANGCODE_RE = re.compile('^([a-z]+)(?:_([A-Z]+).*)?$')
def _split_language(lang_code):
    m = _LANGCODE_RE.match(lang_code)

    if not m:
        raise LanguageNotFoundError('Bad language code: %r - expected format '
                                    'similiar to "en_US".' % lang_code)

    return m.groups()


@memoize(25)
def _load_language(lang):
    language, territory = _split_language(lang)

    def _load_language_module(lang):
        mod_name = '%s.%s' % (languages.__name__, lang)

        if mod_name in sys.modules:
            return sys.modules[mod_name]

        mod = imp.load_module(
            mod_name,
            *imp.find_module(lang, languages.__path__)
        )

        return mod

    mod = None
    try:
        if territory:
            mod = _load_language_module('%s_%s' % (language, territory))
    except ImportError:
        pass

    if not mod:
        try:
            mod = _load_language_module('%s' % language)
        except ImportError:
            pass

    if not mod:
        raise LanguageNotFoundError('Could not find language module for %s' % \
                                    (lang,))

    return mod


@memoize(25)
def _load_ttbl(lang):
    language, territory = _split_language(lang)

    language_resource = 'localedata/%s.ttbl' % language
    full_resource = 'localedata/%s_%s.ttbl' % (language, territory)
    fallback_resource = 'localedata/%s_%s.ttbl' % (language, language.upper())

    candidates = [
        full_resource + '.bz2',
        full_resource,
        language_resource + '.bz2',
        language_resource,
        fallback_resource + '.bz2',
        fallback_resource,
    ]

    for c in candidates:
        if pkg_resources.resource_exists(__name__, c):
            with pkg_resources.resource_stream(__name__, c) as f:
                buf = f.read()

            if c.endswith('.bz2'):
                buf = bz2.decompress(buf)

            return pickle.loads(buf)

    raise LanguageNotFoundError('Could not find translation table for %s' % \
                                lang)
