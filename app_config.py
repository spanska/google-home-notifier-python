#!/usr/bin/env python3

# Flask Parameters
DEBUG = False
API_SECRET = ""

# casting Parameters
CHROMECAST_IP = {
    "default": "",
    "hifi": ""
}
DEFAULT_LOCALE = "fr"
PLAYLIST_GET_TIMEOUT = 240

# purge Parameters
AUDIO_CACHING_DAYS = 30
SCHEDULER_API_ENABLED = True
JOBS = [
    {
        'id': 'cache_cleaner',
        'func': 'app:_clean_cache',
        'trigger': 'cron',
        'day_of_week': 'sun',
        'hour': 4,
    }
]

# facebook parameters
FACEBOOK_USER_RESOLVER_CACHE = 32
FACEBOOK_EMAIL = ""
FACEBOOK_PASSWORD = ""

# ifttt webservices parameters
IFTTT_WS = ""
SEND_SMS_WS = IFTTT_WS.replace("{event}", "sms")
VCF_FILE = ""

# google state machine parameters
RESET_SENTENCE = "OK, l'action a été correctement annulée"
ERROR_SENTENCE = "Je suis désolé mais je crois que l'adapteur google a rencontré une erreur"
MESSENGER_DIALOG = [
    "OK, l'interface facebook est prête",
    "OK, le destinataire est correctement sélectionné",
    "OK, le message facebook est envoyé"
]
SMS_DIALOG = [
    "OK, l'interface sms est prête",
    "OK, le destinataire est correctement sélectionné",
    "OK, le message SMS est envoyé"
]

MESSAGE_MARKER = "(Envoyé depuis ma GoogleHome)"
