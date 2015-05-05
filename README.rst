Slugger is slugging done right
==============================

Slugger solves the seemingly simple problem of turning a title into an url
frienly slug:

.. code-block:: pycon

   >>> from slugger import Slugger
   >>> s = Slugger(lang='en_US')
   >>> s.sluggify(u'Headless-body-in-topless-bar')
   u'headless-body-in-topless-bar'

Unlike many other slugging libraries, it also handles language-specific
ascii-translation. Compare the ``ä``, ``ö`` and ``ü`` in German

.. code-block:: pycon

   >>> s.sluggify(u'Türöffner')
   u'tueroeffner'

against Swedish:

.. code-block:: pycon

   >>> s.sluggify(u'Färsk Ägg')
   u'farsk-agg'


Criterias of what makes a good slug vary, common requirements are a maximum
length and a reduced character set that is highly URL-friendly.

To generate high-quality slugs, Slugger leverages the locale information from
glibc (included in the package), the `unihandecode
<https://pypi.python.org/pypi/Unihandecode>`_ library and some hand-written
replacements.

.. code-block:: pycon

   >>> s = Slugger('en_US')
   >>> s.sluggify(u'Bed & Breakfast')
   u'bed-and-breakfast'
   >>> s.sluggify(u'Folding@Home')
   u'foldingathome'

These are also language-aware:

   >>> s = Slugger('fr_FR')
   >>> s.sluggify(u'Toi & Moi')
   u'toi-et-moi'


Help out
--------

If you find a badly generated slug, please report on `github
<https://github.com/mbr/slugger>`_. Also, any help in implementing better
support for more languages is appreciated; see the `official documentation
<http://pythonhosted.org/slugger>`_ on how to get involved in development.
