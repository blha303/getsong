#!/usr/bin/env python

try: # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError: # Python 2
    from urllib import urlopen, urlencode
import argparse
import youtube_dl
from bs4 import BeautifulSoup as Soup
from sys import exit, version_info


def get_video(uri):
    ydl_opts = {'format': '140'} # 140 is 128k m4a
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.download(['http://www.youtube.com{}'.format(uri)])


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
    args = parser.parse_args()
    uri, title = get_first_yt_result(args.term, args.musicvideo)
    if not uri:
        print("Could not find result for {}. http://youtube.com/results?{}".format(term, urlencode({'search_query': term})))
        return 2
    try:
        input = raw_input
    except NameError:
        pass
    try:
        cont = args.yes or input("About to download the audio for {}, is this correct? [y] ".format(title)) or "y"
    except KeyboardInterrupt:
        cont = "ctrl-c"
        print("")
    if cont in [True, "y", "Y", "yes", ""]:
        return get_video(uri)
    print("Aborted.")
    return 0


if __name__ == "__main__":
    exit(main())
