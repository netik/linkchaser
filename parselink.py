from HTMLParser import HTMLParser


l = '<noscript><META http-equiv="refresh" content="0;URL=http://binged.it/R0XgyQ"></noscript><script>location.replace("http:\/\/binged.it\/R0XgyQ")</script>'

# order of operations
# 301/302 first
# javascript next
#    location.replace
#    location.xxxx
# meta next


# create a subclass and override the handler methods
class RedirectParser(HTMLParser):
  outputurl = None
  inscript = False
  foundmeta = False
  
  def handle_starttag(self, tag, attrs):
    print "Encountered a start tag:", tag
    if tag.upper() == "SCRIPT":
      self.inscript=True

    if tag.upper() == "META":
      heq = False
      for a in attrs:
        if a[0].upper() == "HTTP-EQUIV":
          heq = True
        if a[0].upper() == "CONTENT" and heq == True:
          self.foundmeta = True
          self.outputurl = a[1]

  def handle_endtag(self, tag):
    print "Encountered an end tag :", tag
    if tag.upper() == "SCRIPT":
      self.inscript=False

  def handle_data(self, data):
    if self.inscript:
      print "SCRIPT: %s" % data
        
# instantiate the parser and fed it some HTML
parser = RedirectParser()
parser.feed(l);

print parser.outputurl





