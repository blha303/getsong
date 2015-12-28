#!/usr/bin/env python
from __future__ import print_function

try: # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from io import StringIO
except ImportError: # Python 2
    from urllib import urlopen, urlencode
    from cStringIO import StringIO
import argparse
import sys
import os
import json

import mutagen.mp4
import youtube_dl
from bs4 import BeautifulSoup as Soup

STDOUT = sys.stdout

def prompt(*args):
    try:
        sys.stdout = sys.stderr
        return raw_input(*args) if hasattr(__builtins__, "raw_input") else input(*args)
    finally:
        sys.stdout = STDOUT

class StdoutPrinter(StringIO):
    def __init__(self, quiet):
        self.quiet = quiet
        super(StdoutPrinter, self).__init__()
    def write(self, txt):
        if not txt[0] == "{" and not self.quiet:
            print(txt.strip(), file=sys.stderr)
        super(StdoutPrinter,self).write(txt)

def get_video(uri, quiet=False):
    sys.stdout = tmpstdout = StdoutPrinter(quiet)
    ydl_opts = {'format': '140', 'dump_single_json': True} # 140 is 128k m4a
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        retcode = ydl.download(['http://www.youtube.com{}'.format(uri)])
    sys.stdout = STDOUT
    filename = ""
    tmpstdout = tmpstdout.getvalue().split("\n")
    for line in (l for l in tmpstdout if l[:10] == "[download]"):
        line = line.strip()
        if "[download] Destination: " in line:
            filename = line[24:]
            break
        elif line[-27:] == "has already been downloaded":
            filename = line[11:-28]
            break
    for jsonline in (l for l in tmpstdout if l[0] == "{"):
        data = json.loads(jsonline)
        break
    return filename, retcode, data


def get_first_yt_result(term, musicvideo):
    query = urlencode({'search_query': term + " lyrics" if not musicvideo else term})
    site = urlopen("https://www.youtube.com/results?" + query).read()
    soup = Soup(site, "html.parser")
    first_result = soup.find('h3', {'class': 'yt-lockup-title'})
    if first_result:
        uri, title = first_result.find('a')["href"], first_result.find('a').text
        return uri, title
    return None, None


def main():
    parser = argparse.ArgumentParser(prog="getsong", epilog="Track numbering currently unsupported by mutagen")
    parser.add_argument("term", help="Youtube search term")
    parser.add_argument("-y", "--yes", help="Skip prompt", action="store_true")
    parser.add_argument("-m", "--musicvideo", help="Get first result for <term>, not '<term> lyrics'", action="store_true")
    parser.add_argument("-p", "--print-path", help="Prints path to file to stdout, so you can pipe it to a command or play the file or something", action="store_true")
    parser.add_argument("-u", "--print-url", help="Prints URL to stdout without downloading the audio track", action="store_true")
    parser.add_argument("-q", "--quiet", help="Hides youtube-dl output. Still shows y/n prompt if not hidden by -y", action="store_true")
    parser.add_argument("-i", "--id", help="Skip search, lookup ID. Use \"\" for the search term instead")
    parser.add_argument("--artist", help="Uses Mutagen to write the artist information to the output file")
    parser.add_argument("--title", help="Uses Mutagen to write the title information to the output file")
    parser.add_argument("--album", help="Uses Mutagen to write the album information to the output file")
    args = parser.parse_args()
    if args.id is None:
        uri, title = get_first_yt_result(args.term, args.musicvideo)
    else:
        uri, title = "/watch?v={}".format(args.id), args.id
    if not uri or not title:
        print("Could not find result for {}. http://youtube.com/results?{}".format(args.term, urlencode({'search_query': args.term})), file=sys.stderr)
        return 2
    if args.print_url:
        print("https://youtube.com{}".format(uri))
        return 0
    askstr = "About to download the audio for {}, is this correct? [y] ".format(title)
    try:
        cont = args.yes or prompt(askstr).lower() or "y"
    except KeyboardInterrupt:
        cont = "ctrl-c"
    if cont is True or (type(cont) is str and cont[0] == "y"):
        filename, retcode, json_data = get_video(uri, args.quiet or args.print_path)
    else:
        print("\nAborted.", file=sys.stderr)
        return 0
    if args.print_path:
        print(filename)
    audio = mutagen.mp4.MP4(filename)
    if args.title:
        audio['\xa9nam'] = args.title
    elif json_data["alt_title"]:
        audio['\xa9nam'] = json_data["alt_title"]
    if args.artist:
        audio['\xa9ART'] = args.artist
    elif json_data["creator"]:
        audio['\xa9ART'] = json_data["creator"]
    if args.album:
        audio['\xa9alb'] = args.album
    audio.save()
    return retcode


if __name__ == "__main__":
    sys.exit(main())
