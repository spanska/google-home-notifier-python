#!/usr/bin/env python3

import logging
import re
from pathlib import Path

import requests
import youtube_dl

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/40.0"


def find_and_download_first_song(search_query):
    filename = None

    r = requests.post(
        'https://www.youtube.com/results',
        data={'search_query': search_query},
        headers={"User-Agent": USER_AGENT}
    )
    result = re.search(r'href=\"/watch\?v=(.{11})', r.text).group()[-11:]
    if result:
        logging.info("Song find with tag %s" % result)

        def _play_hook(d):
            nonlocal filename
            if d['status'] == 'finished':
                filename = d['filename']

        with youtube_dl.YoutubeDL({
            'format': 'bestaudio/best',
            'progress_hooks': [_play_hook],
            "outtmpl": "./static/cache/%(title)s.%(ext)s"
        }) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=%s' % result])

        return Path(filename)

    else:
        raise Exception("No Youtube result found for '%s'" % search_query)
