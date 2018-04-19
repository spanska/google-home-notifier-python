#!/usr/bin/env python3

import threading
from inspect import signature

import app_config


class GoogleHomeStateMachine:

    def __init__(self):
        self.threadLock = threading.Lock()
        self.state = 'WAITING_METHOD'
        self.method_name = None
        self.index = 0
        self.params = []
        self.config = None
        self.say = None

    def init_config(self, config, say):
        self.config = config
        self.say = say

    def process(self, token):
        with self.threadLock:
            if self.state == 'WAITING_METHOD':

                if token in self.config:
                    self.method_name = token
                    self.state = 'WAITING_PARAM'
                    self._say_and_increment()
                    return "Successfully register %s method" % self.method_name

                else:
                    self.say(app_config.ERROR_SENTENCE)
                    raise Exception("%s is not a valid method" % token)

            elif self.state == 'WAITING_PARAM':

                if token == "cancel":
                    self._reset()
                    self.say(app_config.RESET_SENTENCE)
                    return "Reset GoogleHomeStateMachine to WAITING_METHOD"

                else:
                    self.params.append(token)
                    if len(self.params) == len(signature(self.config[self.method_name]["method"]).parameters):

                        try:
                            self.config[self.method_name]["method"](*self.params)
                            self._say_and_increment()
                            msg = "Successfully call %s%s" % (
                                self.config[self.method_name]["method"].__name__,
                                self.params
                            )
                            self._reset()
                            return msg

                        except Exception as e:
                            self.say(app_config.ERROR_SENTENCE)
                            self._reset()
                            raise e

                    else:
                        self._say_and_increment()
                        return "Successfully register %s parameter" % token

    def _reset(self):
        self.state = 'WAITING_METHOD'
        self.method_name = None
        self.index = 0
        self.params = []

    def _say_and_increment(self):
        self.say(self.config[self.method_name]["dialog"][self.index])
        self.index += 1
