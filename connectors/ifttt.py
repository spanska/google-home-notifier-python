#!/usr/bin/env python3

import requests

import app_config


def send_sms(to, msg):
    method, url = app_config.SEND_SMS_WS
    r = requests.post(url, data={'to': to, 'msg': msg}) if method == "POST" \
        else requests.get(url, data={'to': to, 'msg': msg})

    if r.status_code != 200:
        raise Exception("Cannot send '%s' text message to '%s'" % (to, msg))
