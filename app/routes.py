#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  route.py
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

from flask import render_template, redirect, url_for, request, send_file, send_from_directory
from app import app
import app.forms as forms
from yandex_music_api.search import Search, TrackMP3, Album
import os
import shutil


from flask_executor import Executor


executor = Executor(app)



@app.route('/')
@app.route('/home')
def home():
    return redirect('/search')#render_template('base.html', title='Home')


@app.route('/search', methods=['GET', 'POST'])
def search():
    keys = request.args
    text = ''

    search_form = forms.SearchForm()
    if search_form.validate_on_submit():
        text = search_form.question.data
        return redirect(url_for('search', text=text, type='tracks'))#redirect(f'/search/text={text}&type=tracks')
    else:
        search_form.question.data = keys['text'] if len(list(keys.keys())) == 2 else ''

    if keys:
        # return keys
        count = 8
        results = eval(f'''Search("{keys['text']}").get_{keys['type']}(count={count})''')
        return render_template('search_results.html', title='Result', search_form=search_form, results=results, text=keys['text'], col=count)
    else:
        return render_template('home.html', title='Search', search_form=search_form)


@app.route('/download-mp3/<string:type>/<string:id>', methods=['POST', 'GET'])
def download(id, type):
    if executor.futures.done('downloading') != False:
        try:
            shutil.rmtree('app\\tempo')
            print(9999999999999999999999)
        except FileNotFoundError:
            pass

    if type == 'track':
        type_class = TrackMP3
    elif type == 'album':
        type_class = Album
    else:
        return redirect(f"https://music.yandex.ru/artist/{id}")
    #return os.getcwd()
    object = type_class(id)
    adress = 'app\\tempo'
    object.set_path(adress)
    
    # app\tmp\Never Marry A Railroad Man.mp3
    if type == 'track':
        file = object.download()
        # return os.getcwd()
        # return file
        return send_file(os.path.join(os.getcwd(), file), as_attachment=True)
    elif type == 'album':
        #executor.shutdown(wait=False)
        if executor.futures.done('downloading') != False :
            print(executor.futures.done('downloading'))
            executor.submit_stored('downloading', object.download)
            # executor.futures.pop('downloading')
        print('album downloading...')
        return redirect(url_for('download_button'))
    #shutil.rmtree('.\\app\\tmp')
    #return result





@app.route('/download-album')
def download_button():
    #print('[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
    print('doning:', executor.futures.done('downloading'))
    zip_files = list(filter(lambda x: '.zip' in x, os.listdir('app\\tempo')))
    print('zip files:', zip_files)
    print('all files:', os.listdir('app\\tempo'))
    print('here is', os.getcwd())
    if zip_files:
        print('pop:', executor.futures.pop('downloading'))
        #executor.shutdown(wait=False)
        print('zip files detected')
        zip_file = os.path.join('app\\tempo', zip_files[0])
        print(zip_file)
        print(os.path.join(os.getcwd(), zip_file))
        return send_file(os.path.join(os.getcwd(), zip_file), as_attachment=True)#send_from_directory('app\\tmp', zip_file, as_attachment=True)
    else:
        return render_template('download-button.html', title='Download album!')
        




@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', title='Сорян)'), 500


