#!/usr/bin/env python3

import threading
from inspect import signature


class GoogleHomeStateMachine:

    def __init__(self):
        self.config = None
        self.say = None
        self.reset_sentence = None
        self.threadLock = threading.Lock()
        self.state = 'WAITING_METHOD'
        self.method = None
        self.index = 0
        self.arg_number = 0
        self.params = []
        self.method_name = None

    def init_config(self, config, say, reset_sentence):
        self.config = config
        self.say = say
        self.reset_sentence = reset_sentence

    def process(self, token):
        with self.threadLock:
            if self.state == 'WAITING_METHOD':

                if token in self.config:
                    self.method = self.config[token]["method"]
                    self.arg_number = len(signature(self.method).parameters)
                    self.method_name = token
                    self.state = 'WAITING_PARAM'
                    self._say_and_increment()
                    return "Successfully register %s method" % self.method.__name__

                else:
                    raise Exception("%s is not a valid method" % token)

            elif self.state == 'WAITING_PARAM':

                if token == "cancel":
                    self._reset()
                    self.say(self.reset_sentence)
                    return "Reset GoogleHomeStateMachine to WAITING_METHOD"

                else:
                    self.params.append(token)
                    if len(self.params) == self.arg_number:
                        self.method(*self.params)
                        self._say_and_increment()
                        self._reset()
                        return "Successfully call %s%s" % (self.method.__name__, self.params)

                    else:
                        self._say_and_increment()
                        return "Successfully register %s parameter" % token

    def _reset(self):
        self.method = None
        self.arg_number = 0
        self.params = []
        self.state = 'WAITING_METHOD'
        self.index = 0
        self.method_name = None

    def _say_and_increment(self):
        self.say(self.config[self.method_name]["dialog"][self.index])
        self.index += 1
