Emoji
=====

Emoji for Python.  This project was inspired by `kyokomi <https://github.com/kyokomi/emoji>`__. 
The defult converting languages contain ``'en'``, ``'es'``, and ``'pt'``. With the help of 
Emoji annotation files in `here <https://github.com/unicode-org/cldr/tree/release-38/common/annotations>`__,
more languages become possible.

Example
-------

The entire set of Emoji codes as defined by the `unicode consortium <http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html>`__
is supported in addition to a bunch of `aliases <http://www.emoji-cheat-sheet.com/>`__.  By
default, only the official list is enabled but doing ``emoji.emojize(use_aliases=True)`` enables
both the full list and aliases.

.. code-block:: python

    >> import emoji
    >> print(emoji.emojize('Python is :thumbs_up:'))
    Python is 👍
    >> print(emoji.emojize('Python is :thumbsup:', use_aliases=True))
    Python is 👍
    >> print(emoji.demojize('Python is 👍'))
    Python is :thumbs_up:
    >>> print(emoji.emojize("Python is fun :red_heart:"))
    Python is fun ❤
    >>> print(emoji.emojize("Python is fun :red_heart:",variant="emoji_type"))
    Python is fun ❤️ #red heart, not black heart

..

By default, the language is English (``language='en'``) but Spanish (``'es'``) and Portuguese (``'pt'``) are also supported.

.. code-block:: python

    >> print(emoji.emojize('Python es :pulgar_hacia_arriba:', language='es'))
    Python es 👍
    >> print(emoji.demojize('Python es 👍', language='es'))
    Python es :pulgar_hacia_arriba:
    >>> print(emoji.emojize("Python é :polegar_para_cima:", language='pt'))
    Python é 👍
    >>> print(emoji.demojize("Python é 👍", language='pt'))
    Python é :polegar_para_cima:️

..

If you want to convert Emoji code into other languages, an according annotation file is needed. Take the indonesion as
an example, download the ``id.xml`` in `here <https://github.com/unicode-org/cldr/tree/release-38/common/annotations>`__ and
import it.

.. code-block:: python

    >> emoji.import_from_annotation('annotaion_xml/id.xml', lang='id')
    >> print(emoji.demojize('Python adalah 👍', language='id'))
    'Python adalah :jempol ke atas:'

..

Installation
------------


.. code-block:: console

    $ git clone https://github.com/carpedm20/emoji.git
    $ cd emoji
    $ python setup.py install


Developing
----------

.. code-block:: console

    $ git clone https://github.com/carpedm20/emoji.git
    $ cd emoji
    $ pip install -e .\[dev\]
    $ nosetests

The ``utils/get-codes-from-unicode-consortium.py`` may help when updating
``unicode_codes.py`` but is not guaranteed to work.  Generally speaking it
scrapes a table on the Unicode Consortium's website with
`BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_ and prints the
contents to ``stdout`` in a more useful format.


Links
----

**For English:**

`Emoji Cheat Sheet <http://www.emoji-cheat-sheet.com/>`__

`Official unicode list <http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html>`__

**For Spanish:**

`Unicode list <https://emojiterra.com/es/puntos-de-codigo/>`__

**For Portuguese:**

`Unicode list <https://emojiterra.com/pt/pontos-de-codigo/>`__

