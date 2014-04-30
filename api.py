#coding:utf-8
import os
import json
import operator
import collections

STRUCTURE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-structure.json")
API_STRUCTURE = {}

for api_method, method_params in json.load(open(STRUCTURE_FILE)).items():
    if not method_params:
        method_params = {}
    API_STRUCTURE[api_method] = method_params

try:
    API_STRUCTURE = collections.OrderedDict(sorted(API_STRUCTURE.items(), key=operator.itemgetter(0)))
except AttributeError:
    # No OrderedDict, that's OK
    pass
