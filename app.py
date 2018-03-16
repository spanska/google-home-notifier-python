#!/usr/bin/env python3

import logging
import os
from functools import wraps, update_wrapper
from pathlib import Path
from urllib.parse import urlparse

import arrow
import pychromecast
import requests
from flask import request, abort, make_response
from flask_api import FlaskAPI, status
from flask_apscheduler import APScheduler
from flask_cors import CORS
from gtts import gTTS
from slugify import slugify
from webargs import fields
from webargs.flaskparser import use_args

import gh_state_machine
from connectors import facebook_messenger
from connectors import youtube

logging.basicConfig(level=logging.INFO)

app = FlaskAPI(__name__)
CORS(app)
app.config.from_pyfile('app_config.py')

logging.info("Finding ChromeCast named '%s'" % app.config.get("CHROMECAST_FRIENDLY_NAME"))
chromecast = next(
    cc for cc in pychromecast.get_chromecasts()
    if cc.device.friendly_name == app.config.get("CHROMECAST_FRIENDLY_NAME")
)

messenger = facebook_messenger.FacebookMessengerClient()
gh_adapter = gh_state_machine.GoogleHomeStateMachine()


def check_secret(view):
    @wraps(view)
    def inner_check_secret(*args, **kwargs):
        secret = request.args.get("secret") if request.method == 'GET' else request.get_json()["secret"]
        if secret != app.config.get("API_SECRET"):
            abort(401)
        else:
            response = make_response(view(*args, **kwargs))
            return response

    return update_wrapper(inner_check_secret, view)


@app.route('/play/<filename>', methods=['GET'])
@check_secret
def play(filename):
    mp3 = Path("./static/" + filename)
    if mp3.is_file():
        _play_audio("http://" + urlparse(request.url).netloc + "/static/" + filename)
        return {}, status.HTTP_204_NO_CONTENT
    else:
        return {"error": "%s is not a file" % mp3.absolute()}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/say', methods=['GET'])
@use_args({
    "text": fields.Str(required=True),
    "lang": fields.Str(default=app.config.get("DEFAULT_LOCALE"))
})
@check_secret
def say(args):
    _play_tts(args["text"], lang=args["lang"])
    return {}, status.HTTP_204_NO_CONTENT


@app.route('/youtube/play', methods=['GET'])
@use_args({
    "query": fields.Str(required=True)
})
@check_secret
def play_song_from_youtube(args):
    song = youtube.find_and_download_first_song(args['query'])

    path = "/static/cache/"
    song_url = "http://" + urlparse(request.url).netloc + path + song.name
    logging.info("Playing %s", song_url)
    _play_audio(song_url, codec="audio/%s" % song.suffix[1:])
    return {}, status.HTTP_204_NO_CONTENT


@app.route('/facebook/messenger/say', methods=['POST'])
@use_args({
    "to": fields.Str(required=True),
    "message": fields.Str(required=True),
}, locations=('json', 'form'))
@check_secret
def say_on_facebook_messenger(args):
    messenger.send_message(args['to'], args['message'])
    return {}, status.HTTP_204_NO_CONTENT


@app.route('/android/sms/send', methods=['POST'])
@use_args({
    "to": fields.Str(required=True),
    "message": fields.Str(required=True),
}, locations=('json', 'form'))
@check_secret
def send_sms(args):
    requests.get(app.config.get("SEND_SMS_WS"), data={'value1': args['to'], 'value2': args['message']})
    return {}, status.HTTP_204_NO_CONTENT


@app.route('/google/home/adapter', methods=['GET'])
@use_args({
    "token": fields.Str(required=True)
})
@check_secret
def adapt_to_google(args):
    gh_adapter.process(args['token'])
    return {}, status.HTTP_204_NO_CONTENT


def _play_tts(text, lang=app.config.get("DEFAULT_LOCALE"), slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = slugify(text + "-" + lang + "-" + str(slow)) + ".mp3"
    path = "/static/cache/"
    cache_filename = "." + path + filename
    tts_file = Path(cache_filename)
    if not tts_file.is_file():
        logging.error(tts)
        tts.save(cache_filename)

    mp3_url = "http://" + urlparse(request.url).netloc + path + filename
    logging.info("Playing %s", mp3_url)
    _play_audio(mp3_url)


def _play_audio(audio_url, codec='audio/mp3'):
    chromecast.wait()
    chromecast.media_controller.play_media(audio_url, codec)


def _clean_cache():
    logging.info("Cleaning cache")
    critical_time = arrow.now().shift(days=-app.config.get("AUDIO_CACHING_DAYS"))
    for item in Path('./static/cache/').glob('*'):
        if item.is_file():
            if arrow.get(item.stat().st_atime) < critical_time:
                logging.info("Removing '%s'" % item)
                os.remove(item)


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    gh_adapter.init_config({
        "messenger": say_on_facebook_messenger,
        "sms": send_sms
    })
    app.run(host='0.0.0.0', port=8080, debug=app.config.get("DEBUG"), use_reloader=False)
