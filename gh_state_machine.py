#!/usr/bin/env python3

import threading
from inspect import signature


class GoogleHomeStateMachine:

    def __init__(self, reset_sentence, error_sentence):
        self.threadLock = threading.Lock()
        self.state = 'WAITING_METHOD'
        self.reset_sentence = reset_sentence
        self.error_sentence = error_sentence
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
                    self.say(self.error_sentence)
                    raise Exception("%s is not a valid method" % token)

            elif self.state == 'WAITING_PARAM':

                if token == "cancel":
                    self._reset()
                    self.say(self.reset_sentence)
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
                            self.say(self.error_sentence)
                            self._reset()
                            raise e

                    else:
                        self._say_and_increment()
                        return "Successfully register %s parameter" % token

    def _reset(self):
        self.params = []
        self.state = 'WAITING_METHOD'
        self.index = 0
        self.method_name = None

    def _say_and_increment(self):
        self.say(self.config[self.method_name]["dialog"][self.index])
        self.index += 1
