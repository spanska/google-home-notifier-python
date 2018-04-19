#!/usr/bin/env python3

import unicodedata


def normalize(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return ("".join([c for c in nkfd_form if not unicodedata.combining(c)])).lower()
