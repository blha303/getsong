getsong
=======

A Python program which uses BeautifulSoup and Youtube-dl to download a
song from youtube

The result will be stored in the current working directory.

Usage
-----

::

    usage: getsong [-h] [-y] [-m] [-p] [-u] [-q] [-i] term

    positional arguments:
      term              Youtube search term

    optional arguments:
      -h, --help        show this help message and exit
      -y, --yes         Skip prompt
      -m, --musicvideo  Get first result for <term>, not '<term> lyrics'
      -p, --print-path  Prints path to file to stdout, so you can pipe it to a
                        command or play the file or something
      -u, --print-url   Prints URL to stdout without downloading the audio track
      -q, --quiet       Hides youtube-dl output. Still shows y/n prompt if not
                        hidden by -y
      -i ID, --id ID    Skip search, lookup ID. Use "" for the search term instead

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
