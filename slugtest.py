#!/usr/bin/env python
# coding=utf8

from slugger import Slugger

s = Slugger('de', hanlang='ja')

print s.sluggify(u'Hellö & Wörld 漢字')
