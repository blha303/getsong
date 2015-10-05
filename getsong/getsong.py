#!/usr/bin/env python
from __future__ import print_function

try: # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError: # Python 2
    from urllib import urlopen, urlencode
import argparse
import youtube_dl
import sys
import os
from bs4 import BeautifulSoup as Soup

real_stdout = sys.stdout

def prompt(*args):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return raw_input(*args) if hasattr(__builtins__, "raw_input") else input(*args)
    finally:
        sys.stdout = old_stdout


def get_video(uri):
    old_stdout = sys.stdout
    sys.stdout = sys.stderr
    ydl_opts = {'format': '140'} # 140 is 128k m4a
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        retcode = ydl.download(['http://www.youtube.com{}'.format(uri)])
    stdout = old_stdout
    return retcode


def get_first_yt_result(term, musicvideo):
    query = urlencode({'search_query': term + " lyrics" if not musicvideo else ""})
    site = urlopen("https://www.youtube.com/results?" + query).read()
    soup = Soup(site, "html.parser")
    first_result = soup.find('h3', {'class': 'yt-lockup-title'})
    if first_result:
        return first_result.find('a')["href"], first_result.find('a').text
    return None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="Youtube search term")
    parser.add_argument("-y", "--yes", help="Skip prompt", action="store_true")
    parser.add_argument("-m", "--musicvideo", help="Get first result for <term>, not '<term> lyrics'", action="store_true")
    parser.add_argument("-p", "--print-path", help="Prints path to file to stdout, so you can pipe it to a command or play the file or something", action="store_true")
    args = parser.parse_args()
    if args.print_path:
        before = [a for a in os.listdir(".") if a[-4:] == ".m4a"]
    uri, title = get_first_yt_result(args.term, args.musicvideo)
    if not uri:
        print("Could not find result for {}. http://youtube.com/results?{}".format(term, urlencode({'search_query': term})), file=sys.stderr)
        return 2
    askstr = "About to download the audio for {}, is this correct? [y] ".format(title)
    try:
        cont = args.yes or prompt(askstr).lower() or "y"
    except KeyboardInterrupt:
        cont = "ctrl-c"
    if cont is True or (type(cont) is str and cont[0] == "y"):
        retcode = get_video(uri)
    else:
        print("\nAborted.", file=sys.stderr)
        return 0
    if args.print_path:
        try:
            changed = list(set([a for a in os.listdir(".") if a[-4:] == ".m4a"]) - set(before))
            print(changed[0], file=real_stdout)
        except IndexError:
            pass
    return retcode


if __name__ == "__main__":
    sys.exit(main())
