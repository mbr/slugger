#!/usr/bin/env python
# coding=utf8

import bz2
import imp
import re
import os
import sys

from remember.memoize import memoize
import pkg_resources
import unihandecode

from exc import LanguageNotFoundError
import languages
import languages.default_language

try:
    import cPickle as pickle
except ImportError:
    import pickle


_MEMOIZE = 20


_LANGCODE_RE = re.compile('^([a-z]+)(?:_([A-Z]+).*)?$')
@memoize(_MEMOIZE)
def _split_language(lang_code):
    m = _LANGCODE_RE.match(lang_code)

    if not m:
        raise LanguageNotFoundError('Bad language code: %r - expected format '
                                    'similiar to "en_US".' % lang_code)

    return m.groups()


@memoize(_MEMOIZE)
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

@memoize(_MEMOIZE)
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

@memoize(_MEMOIZE)
def _compile_rpl_exp(tbl):
    assert(tbl), "cannot compile empty table"

    exp = re.compile(u'(%s)' % u'|'.join(re.escape(k) for k in tbl.iterkeys()))

    subf = lambda m: tbl[m.group(1)]

    return lambda s: exp.sub(subf, s)


class Slugger(object):
    def __init__(self, lang, chain=None, hanlang=None):
        self.lang = lang
        self.hanlang = hanlang

        # load the language
        try:
            self._lang = _load_language(lang)
        except LanguageNotFoundError:
            self._lang = languages.default_language

        self.substitution_tbl = getattr(
            self._lang, 'SUBSTITUTION',
            languages.default_language.SUBSTITUTION
        )

        self.chain = getattr(
            self._lang, 'CHAIN',
            languages.default_language.CHAIN)

        if chain:
            self.chain = chain

        # initialize chain
        for process in self.chain:
            getattr(self, 'init_%s' % process)()

    def do_subst(self, title):
        return title
        return self.subst_sub(title)

    def do_ttbl(self, title):
        return title
        return self.ttbl_sub(title)

    def do_unihandecode(self, title):
        return self.unihandecoder.decode(title)

    def do_cleanup(self, title):
        # FIXME: restrict length, characters, etc...
        return title

    def init_subst(self):
        if self.substitution_tbl:
            self.subst_sub = _compile_rpl_exp(self.substitution_tbl)
        else:
            self.subst_sub = lambda s: s

    def init_ttbl(self):
        # load translation table
        self.ttbl = _load_ttbl(self.lang)
        self.ttbl_sub = _compile_rpl_exp(self.ttbl)

    def init_unihandecode(self):
        hanlang = self.hanlang or self.lang[0:2]

        # work-around for annoying bugs in unihandecode
        # author has been emailed
        if hanlang == 'ja':
            hanlang = "ja"
        elif hanlang == 'kr':
            hanlang = "kr"
        elif hanlang == 'vn':
            hanlang = "vn"

        self.unihandecoder = unihandecode.Unihandecoder(lang=hanlang)

    def init_cleanup(self):
        pass

    def sluggify(self, title):
        title = unicode(title)
        for process in self.chain:
            title = getattr(self, 'do_%s' % process)(title)

        return title
