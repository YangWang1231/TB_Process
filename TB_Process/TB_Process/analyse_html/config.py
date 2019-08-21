#!/usr/bin/python
 #coding:utf-8

import json
import os.path


def init_config():
    config = None
    curpath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(curpath, 'config.json')
    with open(filepath,'r') as json_config_file:
        config  = json.load(json_config_file)
    return config

_config_data = init_config()