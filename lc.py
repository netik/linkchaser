#!/usr/bin/python

import re
import sys
import requests
import optparse
import socket

from urlparse import urlparse
from optparse import OptionParser

def addrs_from_url(url):
  addrs=""

  u = urlparse(url)
  
  for a in socket.getaddrinfo(u.netloc, 80):
    if a[2] == 6: 
      addrs = addrs + a[4][0] + " " 

  return addrs

def geturl(url): 
  global options

  status=0
  depth=0
  maxdepth=9

  # lie about our header so that they think we're a browser.
  headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.84 Safari/534.13','Accept' : '*/*' }

  while (status != 200 and status != 403 and status != 401 and status != 404 and depth < maxdepth):

    if len(options.excludelist) > 0:
      for exword in options.excludelist:
        if url.find(exword) != -1:
          print "\n%d: %s> %s (EXCLUDED)" % (depth, "-" * depth, url)
          return

    if status == 404:
      print "404: Not found"
      return

    depth = depth + 1
    lasturl = url
    r = requests.get(url, headers=headers, allow_redirects=False)
    print "\n%d: %s> %s %s (%s)" % (depth, "-" * depth, url, addrs_from_url(url), r.status_code)

    if options.verbose:
      print r.headers
    
    if (status >=300 or status <= 399):
      url = r.headers['location']
      if url != None:
        print "%d: %s> (HTTP Header)---> %s" % (depth, "-" * depth, url)
    
    status = r.status_code

    if status == 200:
      for line in r.content.split('\n'):
        if line.lower().find("http-equiv=\"refresh\"") > -1:
          m = re.search('content=\"(.*)\"',line,re.IGNORECASE)
          if m:
            u = re.search('URL=(.*)',m.group(1),re.IGNORECASE)

            if u.group(1).startswith("/"):
              url = "%s%s" % (lasturl, u.group(1))
              # therefore, it's a redirect...
              status = 301
              print "%d: %s> (META Header): %s" % (depth, "-" * depth, url)

parser = OptionParser("usage: %prog [options] URL")

parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Be more verbose about the process");

parser.add_option("-x", "--exclude",
                  action="append", dest="excludelist", default=[],
                  help="If the URL contains this word, stop the crawl when seen. Multiple excludes allowed.");

(options, args) = parser.parse_args()

if len(args) != 1:
  parser.error("missing URL")

geturl(args[0])

