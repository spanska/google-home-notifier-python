#!/usr/bin/env python3

import logging
import multiprocessing
import re
from pathlib import Path

import requests
import youtube_dl

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/40.0"


def find_and_download_song(search_query):
    r = requests.post(
        'https://www.youtube.com/results',
        data={'search_query': search_query},
        headers={"User-Agent": USER_AGENT}
    )
    result = re.search(r'href=\"/watch\?v=(.{11})', r.text).group()[-11:]
    if result:
        logging.info("Song find with tag %s" % result)
        return _download_playlist([result])

    else:
        raise Exception("No Youtube result found for '%s'" % search_query)


def _download_playlist(video_ids):
    if not video_ids:
        return []

    elif len(video_ids) == 1:
        playlist = []
        _download_song(video_ids[0], playlist)
        return playlist

    else:
        with multiprocessing.Manager() as manager:
            playlist = manager.list()

            processes = []
            for video_id in video_ids:
                process = multiprocessing.Process(target=_download_song, args=(video_id, playlist))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()

            return [song for song in playlist]


def _download_song(video_id, playlist):
    filename = None

    def _play_hook(d):
        nonlocal filename
        if d['status'] == 'finished':
            filename = d['filename']

    with youtube_dl.YoutubeDL({
        'format': 'bestaudio/best',
        'progress_hooks': [_play_hook],
        "outtmpl": "./static/cache/%(title)s.%(ext)s"
    }) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=%s' % video_id])

    playlist.append(Path(filename))
