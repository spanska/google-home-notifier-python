#!/usr/bin/env python3

import random
import string

KEY_LENGTH = 92

if __name__ == '__main__':
    api_secret = ''.join(random.choice(string.ascii_letters + string.digits + '-_.~') for _ in range(KEY_LENGTH))
    print("Your api secret is %s" % api_secret)
