#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  search.py
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
from lxml import html
import yandex_music_api.proxy_request as proxy_request
from yandex_music_api.track import TrackMP3
from yandex_music_api.album import Album
from yandex_music_api.artist import Artist

import gevent

class Search():
    def __init__(self, text, tracks=True, albums=False, artists=False, playlists=False):
        self.text = text
        '''
        self.urls = dict()
        self.bools = self.__init__.__defaults__
        self.types = ('tracks', 'albums', 'artists', 'playlists')
        self.types = list(map(lambda x: x[0], filter(lambda x: x[1], zip(self.types, self.bools))))
        for i in self.types:
            url = f'https://music.yandex.ru/search?text={self.text}&type={i}'
            self.urls[i] = url
        '''
    
    def get_tree(self, url):
        '''
        get html tree from url
        '''
        req = proxy_request.get(url)
        tree = html.fromstring(req.text)
        return tree
    
    
    def get_music_objects(self, music_class, type, a_class, span_class='', start=0, count=1):
        '''
        Get best matche Artists
        return list of Artist objects
        '''
        url = f'https://music.yandex.ru/search?text={self.text}&type={type + "s"}'
        tree = self.get_tree(url)
        
        if not span_class:
            xpath_text = f'//a[@class="{a_class}"]'
        else:
            xpath_text = f'//span[@class="{span_class}"]/a[@class="{a_class}"]'
        
        objects = tree.xpath(xpath_text)
        count = len(objects) - start if count + start >= len(objects) else count
        objects = map(lambda x: x.get('href'), objects[start:start+count])
        objects_id = map(lambda x: x.split('/')[-1], objects)
        #objects = list(map(lambda x: music_class(x), objects_id))
        
        objects = dict()
        def adding_objects(id, number):
            print(f'Starting {id}')
            objects[number] = music_class(id)

        jobs = [gevent.spawn(adding_objects, id, number) for number, id in enumerate(objects_id)]
        gevent.joinall(jobs)
        #print(sorted(list(objects.items()), key=lambda x: x[0]))
        objects = list(map(lambda x: x[1], sorted(list(objects.items()), key=lambda x: x[0])))
        #print(objects)
        return objects
    
    def get_artists(self, start=0, count=3):
        '''
        Get best matches Artists
        return list of Artist objects
        '''
        return self.get_music_objects(Artist, 
                                      'artist',
                                      "d-link deco-link",
                                      span_class="d-artists d-artists__expanded",
                                      start=start,
                                      count=count)
    
    def get_albums(self, start=0, count=3):
        '''
        Get best matches Albums
        return list of Album objects
        '''
        return self.get_music_objects(Album, 
                                      'album',
                                      "d-link deco-link album__caption",
                                      start=start,
                                      count=count)
    
    def get_tracks(self, start=0, count=3):
        '''
        Get best matches Tracks
        return list of TrackMP3 objects
        '''
        return self.get_music_objects(TrackMP3, 
                                      'track',
                                      "d-track__title deco-link deco-link_stronger",
                                      start=start,
                                      count=count)
    
    def download_best_album(self, path='.', in_one_folder=True):
        '''Download Best Match Album'''
        album = self.get_albums()[0]
        album.set_path(path)
        album.download(in_one_folder=in_one_folder)


if __name__ == "__main__":
    '''
    a = input()
    s = Search(a)
    d = s.get_albums(start=0, count=7)
    pprint(list(map(lambda x: x.title, d)))
    s.download_best_album('Music')
    '''
