---
layout: index
---


getsong
=======

A Python program which uses BeautifulSoup and Youtube-dl to download a song from youtube

Usage
-----

    usage: getsong [-h] [-y] [-m] term
    
    positional arguments:
      term              Youtube search term
    
    optional arguments:
      -h, --help        show this help message and exit
      -y, --yes         Skip prompt
      -m, --musicvideo  Get first result for <term>, not '<term> lyrics'

Installation
------------

* Install dependencies. `pip install -R requirements.txt` or `pip install beautifulsoup4 youtube-dl`. Also requires `ffmpeg` (or avconv) to fix the container on the downloaded audio.
* Copy getsong to a directory on your path. For example, `/usr/local/bin`.
