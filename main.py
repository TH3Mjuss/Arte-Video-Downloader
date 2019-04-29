#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This downloads videos
    from Arte website"""

from urllib.request import urlopen, urlretrieve
from urllib.parse import unquote, urlparse
import urllib
import bs4 as BeautifulSoup
import re
import json
import wget
import os

def get_json_url(url):
    # Check for correct URL et source code as BeautifulSoup array
    url = '//' + url if (not url.startswith('//') and not url.startswith('http')) else url
    u = urlparse(url)
    u = u._replace(scheme='https')
    try:
        assert 'arte.tv' in u.netloc
    except:
        print("Please use a link from Arte website.\n")
        quit()
    try:
        html = urlopen(u.geturl())
    except urllib.error.HTTPError as e: 
        print('HTTPError: {}'.format(e.code))
        quit()
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
        quit()
    
    # Get source code as BeautifulSoup array
    html = urlopen(u.geturl()).read()
    soup = BeautifulSoup.BeautifulSoup(html, 'html.parser')

    # Find the iframe and parse with ESCAPE char
    get_iframe = soup.find_all('iframe')[0]
    my_list = str(get_iframe).split(" ")

    # Get json_url parameter
    url = my_list[5]
    json_url = re.sub(r'.*json_url=', "", url)
    json_url = re.sub(r'"', "", json_url)

    # Decode json_url 
    json_url = unquote(json_url)

    return json_url

def get_vid_url(vid_url):

    # Open Json and make a list of the versions 
    file = urlopen(vid_url).read().decode()
    dict = json.loads(file)
    l = list(dict['videoJsonPlayer']['VSR'])
    name = dict['videoJsonPlayer']['VTI']

    # List video versions available
    i = 0
    for element in dict['videoJsonPlayer']['VSR']:
        quality = dict['videoJsonPlayer']['VSR'][element]['quality']
        mime = dict['videoJsonPlayer']['VSR'][element]['mimeType']
        code = dict['videoJsonPlayer']['VSR'][element]['versionCode']
        libelle = dict['videoJsonPlayer']['VSR'][element]['versionLibelle']
        width = dict['videoJsonPlayer']['VSR'][element]['width']
        height = dict['videoJsonPlayer']['VSR'][element]['height']

        print(i, ": Quality: ", quality, ", Media Type: ", mime, ", Version: ", libelle, "/", code, ", Resolution: ", width, "x", height)
        i += 1

    # Choose video version
    sel = input("Choose your media: ")
    
    while int(sel) < 0 or int(sel) > i-1 :
        sel = input("Please select a valid option: ")
        continue

    sel = int(sel)

    dl_url = dict['videoJsonPlayer']['VSR'][l[sel]]['url']

    return dl_url, name.replace('/', ' of ')

def dl_vid(dl_url, dl_name):

    # Set up file name and detect local path
    file_name = dl_name + ".mp4"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    # Download video to local path
    try:
        print("Downloading, please wait...")
        _dest = os.path.join(THIS_FOLDER, file_name)
        wget.download(dl_url, _dest)
        print ("\n\nDownload completed !")
    except Exception as e:
        print(e)

    return 0


def main():
    url = input("Please enter your file url: ")
    json_url = get_json_url(url)
    vid = get_vid_url(json_url)
    dl_vid(vid[0], vid[1])
    return 0

main()