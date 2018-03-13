#!/usr/bin/env python3

import logging
from pathlib import Path
from urllib.parse import urlparse

import pychromecast
from flask import request, abort
from flask_api import FlaskAPI
from flask_cors import CORS
from gtts import gTTS
from slugify import slugify

logging.basicConfig(level=logging.INFO)

app = FlaskAPI(__name__)
CORS(app)
app.config.from_pyfile('app_config.py')

logging.info("Finding ChromeCast")
chromecast = next(
    cc for cc in pychromecast.get_chromecasts() if cc.device.friendly_name == app.config.get("CHROMECAST_FRIENDLY_NAME")
)


@app.route('/play/<filename>')
def play(filename):
    _check_secret()
    urlparts = urlparse(request.url)
    mp3 = Path("./static/" + filename)
    if mp3.is_file():
        _play_mp3("http://" + urlparts.netloc + "/static/" + filename)
        return filename
    else:
        return "False"


@app.route('/say')
def say():
    _check_secret()
    text = request.args.get("text")
    lang = request.args.get("lang")
    if not text:
        return False
    if not lang:
        lang = "fr"
    _play_tts(text, lang=lang)
    return text


def _check_secret():
    if request.args.get("secret") != app.config.get("API_SECRET"):
        abort(401)


def _play_tts(text, lang='fr', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = slugify(text + "-" + lang + "-" + str(slow)) + ".mp3"
    path = "/static/cache/"
    cache_filename = "." + path + filename
    tts_file = Path(cache_filename)
    if not tts_file.is_file():
        logging.info(tts)
        tts.save(cache_filename)

    urlparts = urlparse(request.url)
    mp3_url = "http://" + urlparts.netloc + path + filename
    logging.info(mp3_url)
    _play_mp3(mp3_url)


def _play_mp3(mp3_url):
    chromecast.wait()
    chromecast.media_controller.play_media(mp3_url, 'audio/mp3')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config.get("DEBUG"))
