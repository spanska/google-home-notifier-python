#!/usr/bin/env python3

import unicodedata
from collections import Counter

from pylev3 import Levenshtein


def find_best_match(input_str, tab):
    normalized_input_str = _normalize(input_str)
    normalized_tab = [_normalize(item) for item in tab]
    result = Levenshtein.wfi([item[0: len(normalized_input_str)] for item in normalized_tab], normalized_input_str)

    grouped_list = Counter(result)
    distance_between_contacts = max(grouped_list.keys()) - min(grouped_list.keys())
    minimums_count = grouped_list[min(grouped_list.keys())]

    if (distance_between_contacts < 4) or (minimums_count > 3):
        raise Exception("No Contact named %s found" % input_str)

    else:
        index = result.index(min(result))
        return tab[index]


def _normalize(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return ("".join([c for c in nkfd_form if not unicodedata.combining(c)])).lower()
