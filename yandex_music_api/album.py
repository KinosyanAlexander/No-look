#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  album.py
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
#  yandex_music_api.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from yandex_music_api.download_info import MusicInfo
from yandex_music_api.track import TrackMP3
import yandex_music_api.proxy_request as proxy_request
from lxml import html
import shutil
import re

import gevent
from zipfile import ZipFile
import time

class Album():
    '''
    By Yandex Music API) get main info about album from id or from data
    Also can download this albun wuth full info about tracks
    Download album Only for available albums
    '''
    def __init__(self, id, download_path='.'):
        if id:
            self.data = MusicInfo(str(id), 'album').get_info()
            self.init_data(self.data, download_path=download_path)
        
        
    def init_data(self, data, download_path='.'):
        '''
        Init object from data(dict)
        return Album
        '''
        self.data = data
        self.id = data['id']
        self.title = data['title']
        self.artists = list(map(lambda x: x['name'], self.data['artists']))
        self.track_count = data['trackCount']
        self.image = self.get_download_cover_link()
        self.type = 'album'
        try:
            genre = data['genre']
            if type(genre).__name__ == 'list':
                self.genre = genre
            else:
                self.genre = [genre]
            
        except KeyError:
            print('no genre')
            self.genre = []
        
        try:
            self.year = data['year']
        except KeyError:
            print('no year')
            self.year = None
        
        self.lyrics = None
        
        self.set_path(download_path)
        self.clean_title = re.sub(r'[/\?:\*"><|]', '', self.title)
        
        return self
   
    def get_download_cover_link(self, size=(200, 200)):
        ''' 
        get link to download cover with crrect size
        '''
        str_size = list(map(lambda x: str(x), size))
        link = 'https://' + self.data['coverUri'].replace('%%', 'x'.join(str_size))
        
        return link
   
    def set_path(self, download_path):
        '''set download path'''
        download_path = re.sub(r'[/\?:\*"><|]', "", download_path)
        print(download_path)
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.download_path = download_path
    
    def get_tracks(self):
        '''
        Get album tracks
        return list of TrackMp3 objects
        '''
        url = f'https://music.yandex.ru/album/{self.id}'
        req = proxy_request.get(url)
        
        tree = html.fromstring(req.text)
        
        tracks = tree.xpath('//a[@class="d-track__title deco-link deco-link_stronger"]')
        tracks = map(lambda x: x.get('href'), tracks)
        tracks_id = map(lambda x: x.split('/')[-1], tracks)
        

        self.tracks = []


        def add_track(id):
            self.tracks.append(TrackMP3(id, album_id=self.id))

        jobs = [gevent.spawn(add_track, id) for id in tracks_id]
        gevent.joinall(jobs)
        #self.tracks = list(map(lambda x: TrackMP3(x, album_id=self.id), tracks_id))
        
        return self.tracks
    
    def download(self, in_one_folder=True, zip=True):
        '''
        Download all tracks from album
        if infolder==True, tracks will download in one personal
        directory with name as album title
        '''

        start = time.time()


        self.get_tracks()
        if in_one_folder:
            tracks_download_path = os.path.join(self.download_path, self.clean_title)
        else:
            tracks_download_path = self.download_path
        if self.data['available']:
            '''
            for i in self.tracks:
                print(i.title)
                i.set_path(tracks_download_path)
                i.make_mp3()
            '''

            jobs_set_path = [gevent.spawn(track.set_path, tracks_download_path) for track in self.tracks]
            gevent.joinall(jobs_set_path)

            jobs_mp3 = [gevent.spawn(track.download_nake_mp3) for track in self.tracks]
            gevent.joinall(jobs_mp3)

            jobs_beauty = [gevent.spawn(track.add_beauty) for track in self.tracks]
            gevent.joinall(jobs_beauty)

            delete_covers = [gevent.spawn(track.delete_cover) for track in self.tracks]
            gevent.joinall(delete_covers)


            if zip:
                self.make_zip(tracks_download_path)
            
            end = time.time() - start
            print(end)
            return tracks_download_path
        else:
            print('Album is Not available')
            return False
    
    def make_zip(self, path):
        print(path, self.clean_title)
        with ZipFile(f'{os.path.join(self.download_path, self.clean_title)}.zip', 'w') as zipObj:
            for folderName, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)
        print('ok')
        #zip_path = shutil.make_archive(f'{self.download_path}\\{self.clean_title}_archive', 'zip', path)
        shutil.rmtree(path)
        #return zip_path
    

#C:\Users\kinos\Desktop\для яндекса\ya_music+pril\pc_yandex_cite\app\tmp\Big Bad Voodoo Daddy
    


if __name__ == '__main__':
    al = Album('89810')
    al.set_path('app\\tmp')
    print(al.download())

