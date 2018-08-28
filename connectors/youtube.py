#!/usr/bin/env python3

import asyncio
import logging
import queue
import re
from pathlib import Path

import requests
import requests_html
import youtube_dl

from .. import sync


class YoutubeConnector:
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/40.0"

    def __init__(self):
        self.playlist = queue.Queue()
        self.read_songs = set()
        self.session = requests_html.HTMLSession()

    def find_and_download_song(self, search_query):
        r = requests.post(
            'https://www.youtube.com/results',
            data={'search_query': search_query},
            headers={"User-Agent": YoutubeConnector.USER_AGENT}
        )
        result = re.search(r'href=\"/watch\?v=(.{11})', r.text).group()[-11:]
        if result:
            logging.info("Song find with tag %s" % result)
            asyncio.get_event_loop().run_until_complete(self._download_song(result, self.playlist))
            return self.playlist

        else:
            raise Exception("No Youtube result found for '%s'" % search_query)

    async def find_next_song_and_queue(self):
        video_id = list(self.read_songs)[-1]
        next_video_id = await self._find_next_song(video_id)
        if next_video_id not in self.read_songs:
            await self._download_song(next_video_id, self.playlist)
        else:
            logging.info("song '%s' has already been listened. Stop downloading songs" % video_id)

    async def _find_next_song(self, video_id):
        r = self.session.get(
            'https://www.youtube.com/watch?v=%s' % video_id,
            headers={"User-Agent": YoutubeConnector.USER_AGENT}
        )
        logging.info("next song is %s" % r.html.find("title", first=True).text)
        next_song = r.html.find('.watch-sidebar-body a', first=True)
        if next_song:
            return next_song.attrs['href'][-11:]

        else:
            raise Exception("No next song found for '%s'" % video_id)

    async def _download_song(self, video_id, playlist):
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
            await sync.sync_to_async(ydl.download)(['http://www.youtube.com/watch?v=%s' % video_id])

        self.read_songs.add(video_id)
        playlist.put(Path(filename))
