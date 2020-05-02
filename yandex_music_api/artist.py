#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  artist.py
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
from yandex_music_api.track import TrackMP3
from yandex_music_api.album import Album
from yandex_music_api.download_info import MusicInfo
import yandex_music_api.proxy_request as proxy_request
from lxml import html


class Artist():
    '''
    By Yandex Music API) get main info about artist
    Such as tracks, albums, genre
    '''
    def __init__(self, id):
        self.data = MusicInfo(str(id), 'artist').get_info()
        self.id = str(id)

        self.title = self.data['artist']['name']
        self.tracks_count = self.data['artist']['counts']['tracks']
        self.albums_count = self.data['artist']['counts']['directAlbums']
        self.type = 'artist'
        try:
            self.image = self.get_download_cover_link()
        except KeyError:
            print('No artist image')
            self.image = None
        try:
            self.genre = self.data['artist']['genres']
        except KeyError:
            print('no genre')
            self.genre = None
        
        self.albums_info = self.data['albums']
        self.popular_tracks_id = self.data['popularTracks']
    

    def get_albums(self, count=3):
        '''
        Get albums, sorted by popular, in count of count
        return list of Album objects
        '''
        if len(self.albums_info) < count:
            count = len(self.albums_info)
        albums = list(map(lambda x: Album('').init_data(x), self.albums_info[:count]))
        return albums
    
    
    def get_tracks(self, count=3):
        '''
        Get tracks, sorted by popular, in count of count
        return list of TrackMP3 objects
        '''
        url = f'https://music.yandex.ru/artist/{self.id}/tracks'
        req = proxy_request.get(url)
        
        tree = html.fromstring(req.text)
        tracks = tree.xpath('//a[@class="d-track__title deco-link deco-link_stronger"]')
        if len(tracks) < count:
            count = len(tracks)
        
        tracks = map(lambda x: x.get('href'), tracks[:count])
        tracks_id = map(lambda x: x.split('/')[-1], tracks)
        tracks_mp3 = list(map(lambda x: TrackMP3(x), tracks_id))
        
        return tracks_mp3
    
    def get_download_cover_link(self, size=(200, 200)):
        ''' 
        get link to download cover with crrect size
        '''
        str_size = list(map(lambda x: str(x), size))
        link = 'https://' + self.data['artist']['cover']['uri'].replace('%%', 'x'.join(str_size))
        
        return link



if __name__ == "__main__":
    #a = Artist('1472')
    a = Artist('67437')
    pprint(list(map(lambda x: x.title, a.get_albums(count=5))))
    #tr = a.get_popular_tracks()
    #pprint(a.data)
    def x(l):
        print(l(83936))
    x(Artist)
