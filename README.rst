getsong
=======

A Python program which uses BeautifulSoup and Youtube-dl to download a
song from youtube

The result will be stored in the current working directory.

Usage
-----

::

    usage: getsong [-h] [-y] [-m] term

    positional arguments:
      term              Youtube search term

    optional arguments:
      -h, --help        show this help message and exit
      -y, --yes         Skip prompt
      -m, --musicvideo  Get first result for <term>, not '<term> lyrics'

Installation
------------

Via ``pip``:

::

    pip3 install getsong

Alternatively:

-  Clone the repository, ``cd getsong``
-  Run ``python3 setup.py install`` or ``pip3 install -e``
-  ``ffmpeg`` (or ``avconv``) is suggested to fix the container on the
   downloaded audio.
