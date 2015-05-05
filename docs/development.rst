Development
===========

Development takes places on `GitHub <https://github.com>`_, see
<https://github.com/mbr/slugger>.


External libraries
------------------

There are very few actual rules for slugging inside the library itself, most of
these come from external libraries. These are:

* `glibc <http://en.wikipedia.org/wiki/GNU_C_Library>`_'s locales, the
  ``LC_CTYPE`` section
* `unihandecode <https://launchpad.net/unihandecode>`_, a fork of `unidecode
  <http://pypi.python.org/pypi/Unidecode>`_ that also handles asian
  languages other than chinese. *unihandecode* itself brings in four different
  transcription libraries for Chinese, Japanese, Korean and Vietnamese.

This is done mainly to offset the weaknesses of the respective libraries, as
*glibc* handles asian transliterations rather poorly and incomplete, while
*unidecode* (and with this, *unihandecode*) doesn't handle any language
specific substitutions at all.


The glibc-locale parser
-----------------------

The ``glcp.py`` script contains a parser for *glibc*-locale files and extracts
the ``LC_CTYPE`` section to use with the script. Try ``python glcp.py --help``
for a bit of help.


Generating the localedata files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, make sure `click <http://click.pocoo.org>`_ is installed (it is a
dependency only for the `glcp` tool and will not be installed by default):

.. code-block:: sh

   $ pip install click

Afterwards, if you haven't done so, checkout the glibc-submodule:

.. code-block:: sh

   git submodule update --init --recursive

Now the ``glcp`` tool can be used to generate the necessary ``localedata``.

.. code-block:: sh

   $ mkdir slugger/localedata
   $ glcp -o slugger/localedata glibc/localedata/locales/*


License
-------

Slugger is licensed under the `LGPL <http://opensource.org/licenses/LGPL-2.1>`_
license like *glibc*, as it uses an integral part of that library (the
localedata information).
