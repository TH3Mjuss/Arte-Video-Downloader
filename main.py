<<<<<<< HEAD
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This downloads videos
    from Arte website"""

from urllib.request import urlopen, urlretrieve
from urllib.parse import unquote, urlparse
import bs4 as BeautifulSoup
import re
import json
import wget
import os

def get_json_url(url):
    # Get source code as BeautifulSoup array
    url = '//' + url if not url.startswith('//') else url
    u = urlparse(url)
    u = u._replace(scheme='https')
    assert u.netloc == 'arte.tv'
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
    file = urlopen(vid_url).read().decode()
    dict = json.loads(file)
    l = list(dict['videoJsonPlayer']['VSR'])
    name = dict['videoJsonPlayer']['VTI']

    i = 0
    print()
    for element in dict['videoJsonPlayer']['VSR']:
        quality = dict['videoJsonPlayer']['VSR'][element]['quality']
        mime = dict['videoJsonPlayer']['VSR'][element]['mimeType']
        code = dict['videoJsonPlayer']['VSR'][element]['versionCode']
        libelle = dict['videoJsonPlayer']['VSR'][element]['versionLibelle']
        width = dict['videoJsonPlayer']['VSR'][element]['width']
        height = dict['videoJsonPlayer']['VSR'][element]['height']

        print(i, ": Quality: ", quality, ", Media Type: ", mime, ", Version: ", libelle, "/", code, ", Resolution: ", width, "x", height)
        i += 1

    sel = input("Choose your media: ")
    sel = int(sel)
    dl_url = dict['videoJsonPlayer']['VSR'][l[sel]]['url']

    return dl_url, name.replace('/', ' of ')

def dl_vid(dl_url, dl_name):
    file_name = dl_name + ".mp4"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    try:
        print("Downloading, please wait...")
        _dest = os.path.join(THIS_FOLDER, file_name)
        wget.download(dl_url, _dest)
        print ("Download completed !")
    except Exception as e:
        print(e)

    return 0


def main():
    url = input("Please enter your file url: ")
    json_url = get_json_url(url)
    print("URL: ", json_url)
    vid = get_vid_url(json_url)
    dl_vid(vid[0], vid[1])
    return 0

main() 
=======
#!/usr/bin/env python
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

    #Check for valid URL
    url = '//' + url if not url.startswith('//') else url
    u = urlparse(url)
    u = u._replace(scheme='https')
    assert u.netloc == 'arte.tv'
    html = urlopen(u.geturl()).read()

    # Get source code as BeautifulSoup array
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
    file = urlopen(vid_url).read().decode()
    dict = json.loads(file)
    l = list(dict['videoJsonPlayer']['VSR'])
    name = dict['videoJsonPlayer']['VTI']

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

    sel = input("Choose your media: ")
    sel = int(sel)
    dl_url = dict['videoJsonPlayer']['VSR'][l[sel]]['url']
    
    return dl_url, name.replace('/', ' of ')

def dl_vid(dl_url, dl_name):
    file_name = dl_name + ".mp4"
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    try:
        print("Downloading, please wait...")
        _dest = os.path.join(THIS_FOLDER, file_name)
        wget.download(dl_url, _dest)
        print ("Download completed !")
    except Exception as e:
        print(e)

    return 0


def main():
    url = input("Please enter your file url: ")
    json_url = get_json_url(url)
    print("URL: ", json_url)
    vid = get_vid_url(json_url)
    dl_vid(vid[0], vid[1])
    return 0

main()
>>>>>>> 2557fb5d83d023cfef19ae2aadc0089f11e488a8
