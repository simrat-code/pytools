#!/usr/bin/env python

import httplib
import sys
import socket
import optparse

#proxy = 'http://192.168.56.1:3128'
#os.environ['http_proxy'] = proxy
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

def WebService(address, port, resource):
    #if not resource.startswith('/'):
    #    resource = '/' + resource

    try:
        conn = httplib.HTTPConnection(address, port)
        print "[=] HTTP connection created successfully"
        #conn.set_tunnel('192.168.56.1', 3128)
        req = conn.request('GET', resource)
        print "[=] request success for: %s" % resource
        response = conn.getresponse()
        print "[=] response status: %s" % response.status
    except socket.error, e:
        print "[=] HTTP connection failed: %s" % e
        return False
    finally:
        conn.close()

    if response.status in [200, 301]:
        return True
    else:
        return False


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-a", "--address", dest = "address", default = "localhost",
            help = "address for server|proxy", 
            metavar = "ADDRESS")
    parser.add_option("-p", "--port", dest="port", default=80,
            help="port of webserver", 
            metavar="PORT")
    parser.add_option("-r", "--resource", dest="resource", default="/",
            help="resource to GET",
            metavar="RESOURCE")
    (options, args) = parser.parse_args()

    #check = WebService('192.168.56.1', 3128, 'http://www.google.co.in')
    check = WebService(options.address, options.port, options.resource)
    print "[=] return status of WebService: %d" % check
    sys.exit(not check)
# -- end --

