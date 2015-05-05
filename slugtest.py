from slugger import Slugger

s = Slugger('de', hanlang='ja')

print s.sluggify(u'Hellö & Wörld 漢字')
print s.sluggify(u'And they lived happily ever after!')
