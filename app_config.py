#!/usr/bin/env python3

# Flask Parameters
DEBUG = True
API_SECRET = ""

# casting Parameters
CHROMECAST_FRIENDLY_NAME = ""
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
