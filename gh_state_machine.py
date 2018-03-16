#!/usr/bin/env python3

import threading
from inspect import signature

import app


class GoogleHomeStateMachine:
    KEYWORD_TO_METHOD = {
        "messenger": app.say_on_facebook_messenger
    }

    def __init__(self):
        self.threadLock = threading.Lock()
        self.state = 'WAITING_METHOD'
        self.method = None
        self.arg_number = 0
        self.params = []

    def process(self, token):
        self.threadLock.acquire()

        if self.state == 'WAITING_METHOD':
            self.method = GoogleHomeStateMachine.KEYWORD_TO_METHOD[token]
            self.arg_number = len(signature(self.method).parameters)
            self.state = 'WAITING_PARAM'

        elif self.state == 'WAITING_PARAM':

            if token == "cancel":
                self._reset()

            else:
                self.params.append(token)
                if len(self.params) == self.arg_number:
                    self.method(*self.params)
                    self._reset()

        self.threadLock.release()

    def _reset(self):
        self.method = None
        self.arg_number = 0
        self.params = []
        self.state = 'WAITING_METHOD'
