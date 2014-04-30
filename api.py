#coding:utf-8
import os
import json

STRUCTURE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-structure.json")
API_STRUCTURE = {}

for api_method, method_params in json.load(open(STRUCTURE_FILE)).items():
    if not method_params:
        method_params = {}
    API_STRUCTURE[api_method] = method_params
