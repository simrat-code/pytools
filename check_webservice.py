#!/usr/bin/env python

import httplib
import sys

def CheckWebservice(address, port, resource):
  #if not resource.startswith('/'):
  #  resource = '/' + resource

  try:
    conn = httplib.HTTPConnection(address, port)
    print "[*] http connection created successfully"
    req = conn.request('GET', resource)
    print "[=] request for %s successful" % resource
    response = conn.getresponse()
    print "response status: %s" % response.status
  except socket.error, e:
    print "[=] http connection failed: %s" % e
    return False
  finally:
    conn.close()
    print "[=] http conn closed successful"
    
  if response.status in [200, 301]:
    return True
  else:
    return False
    
if __name__ == "__main__":
  #check = CheckWebservice('192.168.56.1', 3128, 'www.google.co.in')
  check = CheckWebservice('192.168.56.1', 3128, 'www.ipchicken.com') 
  print "[=] function returned %s" % check
  sys.exit( not check)
