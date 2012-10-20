#!/usr/bin/env python
########################################################################################
#
# scrapes jpeg images by volume_id for Cassini ISS archived at pds-rings.seti.org
#
########################################################################################
import os.path, urllib  
import exceptions, urllib2, re
from BeautifulSoup import BeautifulStoneSoup
import sys

try:
    volume_id = sys.argv[1]
except IndexError:
    print """
    This script returns urls to jpeg images for an entire Cassini ISS data volume
    as archived by the NASA PDS Rings Node at http://pds-ring.seti.org
    This script prints image urls to stdout

    provide volume_id as first arg, optional image size as second arg
    valid sizes = thumb/small/med/full default is med

    note that jpegs prodcued by the Rings Node are color coded to indicat filter used 
    in all sizes except 'full' 

    This scraper made without prermission, please use wisely.
    """
    sys.exit()

default = 'med'
try:
    size =  sys.argv[2] if sys.argv[2] in ['thumb','small','med','full'] else default
except IndexError: 
    size = default

base_url = "http://pds-rings.seti.org/browse/" # base url for reletive links we find    
start_url = base_url + volume_id + "/data/"
try:
    start_page = urllib2.urlopen(start_url).read()   
except urllib2.HTTPError:
    raise Exception("Http 404 - invalid start url: " + start_url)

soup = BeautifulStoneSoup(start_page) 
links = soup.findAll('a')   

for link in links:
    browse_struct = True
    image_dir = link['href'].split('/')[-1] # this is if webmaster has built the browse struct
    if not image_dir:
        browse_struct = False
        image_dir = link['href'].split('/')[0] # browse struct not build, this is straight apache dir listing
    if re.match(r"(\d+)_(\d+)", image_dir):
        url = start_url + image_dir + '/index-file-list.html/' if browse_struct else start_url + image_dir + '/'
        page =  urllib2.urlopen(url).read()  
        soup = BeautifulStoneSoup(page)   
        image_links = soup.findAll('a')  
        for ilink in image_links:   
            if re.match(r"(.*)_" + size + ".jpg", ilink['href']): 
                image_link = base_url + volume_id + "/data/" + image_dir + '/' + ilink['href']  
                # print 'wget ' + image_link + ';'
                print image_link
