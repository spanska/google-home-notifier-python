#!/usr/bin/env python3

# Flask Parameters
DEBUG = True
API_SECRET = ""

# casting Parameters
CHROMECAST_IP = ""
DEFAULT_LOCALE = "fr"

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
