#coding:utf-8
import os
import json

STRUCTURE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api-structure.json")
API_STRUCTURE = json.load(open(STRUCTURE_FILE))
