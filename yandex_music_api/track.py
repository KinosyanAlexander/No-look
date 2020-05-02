#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3, APIC, error, USLT, TIT2, TPE1, TRCK, TALB
from mutagen.easyid3 import EasyID3
import os
import re
from yandex_music_api.download_info import MusicInfo
import yandex_music_api.proxy_request as proxy_request
from lxml import html



class TrackMP3():
    '''
    By Yandex Music Track get main info about track
    Also can download this track wuth full info about him
    Only for available tracks
    '''
    def __init__(self, id, download_path='.', album_id=''):
        if id:
            self.data = MusicInfo(str(id), 'track').get_info()
            self.init_data(self.data, album_id=album_id, download_path=download_path)
        
       
    def init_data(self, data, album_id='', download_path='.'):
        '''
        Init object from data(dict)
        return TrackMP3
        '''
        self.data = data
        self.id = data['id']
        if album_id:
            self.data['album'] = list(filter(lambda x: str(x['id']) == str(album_id), self.data['albums']))[0]
        else:
            self.data['album'] = self.data['albums'][0]
        self.title = self.data['title']
        self.artists = list(map(lambda x: x['name'], self.data['artists']))
        self.album_name = self.data['album']['title']
        self.type = 'track'
        
        try:
            self.image = self.get_download_cover_link()
        except KeyError:
            print('No cover')
        
        try:
            genre = data['album']['genre']
            if type(genre).__name__ == 'list':
                self.genre = genre
            else:
                self.genre = [genre]
        except KeyError:
            print('no genre')
            self.genre = []
        
        try:
            self.track_position = self.data['album']['trackPosition']['index']
        except KeyError:
            print('No track position')
            self.track_position = ''
        
        try:
            self.year = self.data['album']['year']
        except KeyError:
            print('no year')
            self.year = ''
        
        
        
        self.lyrics = None
        
        self.set_path(download_path)
        
        return self
    
    
    
    def get_lyrics(self):
        # get track lyrics if track have lyrics
        if self.data['lyricsAvailable']:
            url = f'https://music.yandex.ru/album/{self.data["album"]["id"]}/track/{self.id}'
            req = proxy_request.get(url)
            tree = html.fromstring(req.text)
            lyrics_div = tree.xpath('//div[@class="sidebar-track__lyric-text typo "]')
            self.lyrics = lyrics_div[0].text_content()
            
            return self.lyrics
        else:
            self.lyrics = None
            return None
    
    def get_lyrics_language(self):
        #Get lyrics language, if that available
        url = f'https://music.yandex.ru/album/{self.data["album"]["id"]}/track/{self.id}'
        req = proxy_request.get(url)
        
        tree = html.fromstring(req.text)
        translate_link = tree.xpath('//div[@class="sidebar-track__lyric-text-info _hidden deco-typo-secondary"]/a')[0].get('href')
        language = re.findall(r'lang=([^-]+)-', translate_link)[0]
        
        return language
    
        
    
    
    def set_path(self, download_path):
        '''Set download path, where will download tracks'''
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        self.download_path = download_path
        self.audio_filename = os.path.join(self.download_path, re.sub(r'[/\?:\*"><|]', "", self.title) + '.mp3')
        self.cover_filename = os.path.join(self.download_path, re.sub(r'[/\?:\*"><|]', "", self.title) + '.png')
    
    
    def download_nake_mp3(self):
        ''' download nake mp3 - only music'''
        download_link = self.get_download_mp3_link()
        bytes_data = proxy_request.get(download_link).content
        with open(self.audio_filename, 'wb') as file:
            file.write(bytes_data)
    
    
    def get_download_info(self):
        ''' get download info about mp3 file '''
        url = f'https://api.music.yandex.net/tracks/{self.id}/download-info'
        download_info = proxy_request.get(url).json()
        
        mp3_data = list(filter(lambda x: x['codec'] == 'mp3', download_info['result']))[0]

        
        return mp3_data
    
    
    def get_download_mp3_link(self):
        '''get link to download mp3 file'''
        url = self.get_download_info()['downloadInfoUrl'] + '&format=json'
        download_data = proxy_request.get(url).json()
        
        host = download_data['host']
        path = download_data['path']
        s = download_data['s']
        ts = download_data['ts']
        
        download_link = f'https://{host}/get-mp3/{s}/{ts}{path}'
        
        return download_link
    
    
    def download_cover(self):
        ''' download cover'''
        download_link = self.get_download_cover_link()
        
        image_data = proxy_request.get(download_link).content
        
        with open(self.cover_filename, 'wb') as file:
            file.write(image_data)
    
    
    def get_download_cover_link(self, size=(200, 200)):
        ''' 
        get link to download cover with crrect size
        '''
        str_size = list(map(lambda x: str(x), size))
        link = 'https://' + self.data['coverUri'].replace('%%', 'x'.join(str_size))
        
        return link
    
    
    def add_details(self):
        '''
        Adds the details to mp3 file
        '''
        try:
            tags = EasyMP3(self.audio_filename)
        except FileNotFoundError:
            self.download_nake_mp3()
        finally:
            tags = EasyMP3(self.audio_filename)
        
        tags["title"] = self.title
        tags["artist"] = self.artists
        tags["album"] = self.album_name
        tags['tracknumber'] = str(self.track_position)
        tags['date'] = str(self.year)
        tags['genre'] = self.genre
        tags.save()

        '''
        if self.lyrics:
            tags = ID3(self.audio_filename)
            uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=self.lyrics)
            tags["USLT::'eng'"] = uslt_output
            
        '''
        
        tags.save(self.audio_filename)
    
    
    def add_cover(self):
        """
        Adds album art to the initialized mp3 file
        """
        try:
            imagedata = open(self.cover_filename, 'rb').read()
        except FileNotFoundError:
            self.download_cover()
        finally:
            imagedata = open(self.cover_filename, 'rb').read()
        
        id3 = ID3(self.audio_filename)
        id3.add(APIC(3, 'image/png', 3, 'Front cover', imagedata))
        id3.add(TIT2(encoding=3, text=self.title))

        id3.save(v2_version=3)
    
    
    def make_mp3(self):
        ''' Download full-fledged mp3'''
        if self.data['available']:
            self.download_nake_mp3()
            self.download_cover()
            self.add_details()
            self.add_cover()
            os.remove(self.cover_filename)
        else:
            print('Not available track')
    
    def download(self):
        self.make_mp3()
        return self.audio_filename
    
    def add_beauty(self):
        self.download_cover()
        self.add_details()
        self.add_cover()
    
    def delete_cover(self):
        os.remove(self.cover_filename)



if __name__ == "__main__":
    print([1,2,3,4,5,6][90:-1])
    track_id = '29461633'
    print(9)
    track = TrackMP3(track_id).data
    print(99)
    
    print(999)
    tr = TrackMP3('').init_data(track, download_path='Music')
    print(9999)
    tr.make_mp3()
    print(99999)


