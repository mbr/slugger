Using the Slugger library
=========================

Installation
------------

Releases of Slugger should be installed from `PyPi <http://pypi.python.org>`_,
using `pip <https://pypi.python.org/pypi/pip>`_:

.. code-block:: sh

   $ pip install slugger

You cannot use Slugger straight from a checkout of the github repository, as
*glibc*-localedata has to be parsed and pickled first. When installing a
release from , this data is already included.

See :doc:`development` for details on how to generate this data.


Slugging things
---------------

Use is usually straightforward:

.. code-block:: python

    from slugger import Slugger

    s = Slugger('de', hanlang='ja')
    print s.sluggify(u'Hellö & Wörld 漢字')

This will print ``helloe-und-woerld-kan-ji``. The :class:`~slugger.Slugger`
class itself supports a number of construction options, to fine-tune the
result.

You should not rely on Slugger generating the same slug across different
versions, as the goal of this library is to steadily improve, either through
better underlying libraries or fixes in Slugger itself. It is therefore
necessary to store the generated slug in addition to the title if you keep a
database of those.
