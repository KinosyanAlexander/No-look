#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lol_rabotaet'
    UPLOAD_FOLDER = '/app/tmp'
    #LOGFILE = 'logs/Development.log'
    ENV = 'development'
    #DEBUG = True