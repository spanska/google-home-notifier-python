#!/usr/bin/env python3

from functools import lru_cache

from fbchat import Client
from fbchat.models import Message, ThreadType

import app_config


class FacebookMessengerClient:

    def __init__(self):
        self.client = Client(app_config.FACEBOOK_EMAIL, app_config.FACEBOOK_PASSWORD)

    def send_message(self, user, message):
        user_id = self._get_user_uid(user)
        self.client.send(Message(text=message), thread_id=user_id, thread_type=ThreadType.USER)

    @lru_cache(maxsize=app_config.FACEBOOK_USER_RESOLVER_CACHE)
    def _get_user_uid(self, user):
        results = self.client.searchForUsers(user)
        if results:
            first_user = results[0]

            if first_user.is_friend:
                return first_user.uid

            else:
                raise Exception("The user %s is not your friend. You can't talk to him" % user)

        else:
            raise Exception("No user named '%s' was found" % user)
