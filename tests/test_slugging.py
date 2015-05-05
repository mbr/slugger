# coding: utf8

# FIXME: it'd be really nice to have some additional tests here
from slugger import Slugger


def test_simple_slug():
    s = Slugger('de', hanlang='ja')

    assert s.sluggify(u'Hellö & Wörld 漢字') == u'helloe-und-woerld-kan-ji'
    assert s.sluggify(u'And they lived happily ever after!') == \
        u'and-they-lived-happily-ever-after-'
