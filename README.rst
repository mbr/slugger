Slugger is slugging done right
==============================
Slugger solves the "simple" problem of turning a title of a title like
*Headless body in topless bar* into a slug: *headless-body-in-topless-bar*.

Criterias of what makes a good slug vary, but most often they are required to
have a maximum length a reduced character set that is highly URL-friendly.

Transcribing
-----------
Many languages have special rules for transcribing phrases that fall
outside the `ISO basic Latin alphabet
<http://en.wikipedia.org/wiki/ISO_basic_Latin_alphabet>`_, which vary from
language to language.

An example: The headline *160 Häftlinge warten auf den Tag der offenen Tür*
would be transcribed by native German speaker like this:
*160-Haeftlinge-warten-auf-den-Tag-der-offenen-Tuer*. Notice that the letter
"ä" is transcribed to "ae".

Transcribing the finnish phrase *Itä-Länsi-pelaaja Jan Latvala juhlii tänään
Lahdessa* however, should result in the following:
*Ita-Lansi-pelaaja-Jan-Latvala-juhlii-tanaan-Lahdessa*
In this case, the "ä" is simply replaced with an "a", no extra letters.

Character substitution
----------------------
Slugger also supports replacing characters with words where appropriate. For
example, *Me & You* is better sluggified as "Me-and-You" or "me-and-you",
instead of just dropping the and-sign. Of course, in French, the phrase "Toi et
Moi" would properly sluggified as "toi-et-moi".

External libraries
------------------
There are very few actual rules inside the library itself, most data is taken
from external languages. These are:

* `glibc <http://en.wikipedia.org/wiki/GNU_C_Library>`_'s locales, the LC_CTYPE
  section
* `unihandecode <https://launchpad.net/unihandecode>`_, a fork of `unidecode
  <http://pypi.python.org/pypi/Unidecode/0.04.9>`_ that also handles asian
  languages other than chinese. *unihandecode* itself pulls in four different
  transcription libraries for Chinese, Japanese, Korean and Vietnamese.

This is done mainly to offset the weaknesses of the respective libraries, as
*glibc* handles asian transliterations rather poorly and incomplete, while
*unidecode* (and with this, *unihandecode*) doesn't handle any language
specific substitutions at all.

Additional fixes are contained in slugger itself.

Usage
=====
Detailed docs are still missing. Here is a quick example::

    from slugger import Slugger

    s = Slugger('de', hanlang='ja')
    print s.sluggify(u'Hellö & Wörld 漢字')

This will print ``helloe-und-woerld-kan-ji``. The Slugger class itself supports
a number of construction options, see ``slugger/__init__.py`` for details.

You should not rely on Slugger generating the same slug across different
versions, as the goal of this library is to steadily improve, either through
better underlying libraries or fixes in Slugger itself.

Installation
------------
You cannot use Slugger straight from a checkout of the repository, as
*glibc*-localedata has to be parsed and pickled first. When installing a
release from `PyPi <http://pypi.python.org>`_, this data is already included.

Development
===========
Development takes places on `GitHub <https://github.com>`_, see
<https://github.com/mbr/slugger>.

The ``glcp.py`` script contains a parser for *glibc*-locale files and extracts
the ``LC_CTYPE`` section to use with the script. Try ``python glcp.py --help``
for a bit of help.

Any help is welcome, especially contributing new rules for new languages. If
you find a generated slug unsatisfactionary, please `let me know
<https://github.com/mbr/slugger>`_.

License
-------
Slugger is licensed under the LGPL license like *glibc*, as it uses an integral
part of that library (the localedata information).
