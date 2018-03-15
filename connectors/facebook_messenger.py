#!/usr/bin/env python3

from fbchat import Client
from fbchat.models import Message, ThreadType

import app_config


class FacebookMessengerClient:

    def __init__(self):
        self.client = Client(app_config.FACEBOOK_EMAIL, app_config.FACEBOOK_PASSWORD)

    def send_message(self, user, message):
        results = self.client.searchForUsers(user)

        if results:
            first_user = results[0]
            if first_user.is_friend:
                self.client.send(Message(text=message), thread_id=first_user.uid, thread_type=ThreadType.USER)

            else:
                raise Exception("The user %s is not your friend. You can't talk to him" % user)

        else:
            raise Exception("No user named '%s' was found" % user)
