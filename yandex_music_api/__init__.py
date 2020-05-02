#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from .album import Album
from .artist import Artist
from .download_info import MusicInfo
from .search import Search
from .track import TrackMP3
from .proxy_request import get
from .proxy_update import make_proxy_list

__all__ = ['Album', 'Artist', 'MusicInfo',
           'Search', 'TrackMP3', 'get', 'make_proxy_list']
