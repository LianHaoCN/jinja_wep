#!/usr/bin/python
#-*-coding=utf-8-*-
#config.py

import config_default, config_override

configs = config_default.configs

def merge(configs, config_override):
    for i in config_override:
        configs[i] = dict(configs[i], **config_override[i])
    return configs
    
try:
    import config_override
    configs = merge(configs, config_override.configs)
    print configs
except ImportError:
    pass