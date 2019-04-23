#!/usr/bin/env python3

import http.client
import sys
import socket
import optparse

#proxy = 'http://192.168.56.1:3128'
#os.environ['http_proxy'] = proxy
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

class WebService:
#(address, port, resource, https_enable, print_enable):
    #if not resource.startswith('/'):
    #    resource = '/' + resource
    def __init__(self, address, port, resource="/", https_enable=False, verbose=False):
        self.address  = address
        self.port     = port
        self.resource = resource
        self.https    = https_enable
        self.verbose  = verbose

        self.conn = None

        self.print_msg ("[=] addr -" + self.address + "-")
        self.print_msg ("[=] port -" + str(self.port) + "-")
        self.print_msg ("[=] rsrc -" + self.resource + "-")


    def set_address(self, address):
        self.address = address


    def set_port(self, port):
        self.port = port


    def set_resource(self, resource):
        self.resource = resource


    def set_https(self, choice):
        self.https = choice


    def set_verbose(self, choice):
        self.verbose = choice


    def print_msg(self, msg):
        if self.verbose is True:
            print(msg)


    def process(self):
        try:
            if self.https is True:
                self.conn = http.client.HTTPSConnection(self.address, self.port, timeout=20)
                self.print_msg("[=] HTTPS connection created successfully")
            else:
                self.conn = http.client.HTTPConnection(self.address, self.port, timeout=20)
                self.print_msg( "[=] HTTP connection created successfully")
            
            req = self.conn.request('GET', self.resource)
            self.print_msg( "[=] request for: " + self.resource)

            response = self.conn.getresponse()
            self.print_msg( "[=] response status: "+ str(response.status) +" :"+ response.reason)
            self.print_msg ("[=] response string start:")
            print(response.read())
            self.print_msg ("[=] response string end:")
        except socket.error as e:
            print("[=] HTTP connection failed: %s" % e)
            return False
        except http.client.HTTPException as e:
            print("[=] exception occured: %s " % e)
            return False
        except:
            print("[=] unhandled exception occured")
            return False
        finally:
            if self.conn is not None:
                self.print_msg ("[=] connection closed")
                self.conn.close()
    
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
    parser.add_option("-s", "--ssl", dest="https", default=False, action="store_true", 
            help="enable HTTPS",
            metavar="HTTPS")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
            help="verbose output")
    (options, args) = parser.parse_args()

    if options.address == None or options.port == None:
        print("some required options are not set: address/port")
        parser.print_usage()
        sys.exit(0)

    #check = WebService('192.168.56.1', 3128, 'http://www.google.co.in')
    ws = WebService(options.address, options.port, options.resource, options.https, options.verbose)
    check = ws.process()
    ws.print_msg( "[=] return status of WebService: " + str(check))
    sys.exit(not check)
# -- end --

