#!/usr/bin/env python3

import threading
from inspect import signature


class GoogleHomeStateMachine:

    def __init__(self):
        self.config = None
        self.threadLock = threading.Lock()
        self.state = 'WAITING_METHOD'
        self.method = None
        self.arg_number = 0
        self.params = []

    def init_config(self, config):
        self.config = config

    def process(self, token):
        with self.threadLock:
            if self.state == 'WAITING_METHOD':

                if token in self.method:
                    self.method = self.config[token]
                    self.arg_number = len(signature(self.method).parameters)
                    self.state = 'WAITING_PARAM:'

                else:
                    raise Exception("%s is not a valid method" % token)

            elif self.state == 'WAITING_PARAM':

                if token == "cancel":
                    self._reset()

                else:
                    self.params.append(token)
                    if len(self.params) == self.arg_number:
                        self.method(*self.params)
                        self._reset()

    def _reset(self):
        self.method = None
        self.arg_number = 0
        self.params = []
        self.state = 'WAITING_METHOD'
