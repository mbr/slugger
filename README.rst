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
* `unihandecode https://launchpad.net/unihandecode`_, a fork of `unidecode
  http://pypi.python.org/pypi/Unidecode/0.04.9`_ that also handles asian
  languages other than chinese. *unihandecode* itself pulls in three different
  transcription libraries for Korean, Japanese and Chinese.

This is done mainly to offset the weaknesses of the respective libraries, as
*glibc* handles asian transliterations rather poorly and incomplete, while
*unidecode* (and with this, *unihandecode*) doesn't handle any language
specific substitutions at all.

Additional fixes are contained in slugger itself.