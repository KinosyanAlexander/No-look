#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  download_info.py
#  
#  Copyright 2020 kinos <kinos@DESKTOP-7650S1U>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import yandex_music_api.proxy_request as proxy_request


class ValidationError(Exception):
    pass


class MusicInfo():
    '''
    Class providing information about the musical type (track/album/artist)
    '''
    def __init__(self, id: str, kind: str):
        self.id = id
        self.kind = kind
    
    def get_info(self):
        ''' Get info about music(i.e. track, album or artist)'''
        url = f'https://api.music.yandex.net/{self.kind + "s"}/{self.id}/'
        request = proxy_request.get(url, timeout=2)
        data = request.json()
        
        if 'error' in data.keys():
            if data['error']['name'] == 'validate':
                raise ValidationError
            else:
                return data
        else:
            self.info = data['result']
            if self.kind == 'track':
                self.info = self.info[0]
            return self.info

if __name__ == '__main__':
    print(MusicInfo('700374', 'track').get_info())
