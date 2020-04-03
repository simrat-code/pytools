#
# Author    : Simrat Singh
# Date      : Apr-2020
#

import threading
import socket
import select


def nextValueOf(text, src_list):
    print(src_list)
    x = len(src_list)
    flag = 0
    for i in range(x):
        if (flag == 1): return src_list[i]
        #
        # pattern found, now need to return the next value
        # set flag to return on next value
        #
        if (src_list[i] == text): flag = 1      
    raise ValueError


def portForService(protocol):
    if ("http" == protocol):
        return 80
    elif ("https" == protocol):
        return 443


class clientHandlerThread(threading.Thread):
    static_resp = ("HTTP/1.0 200 OK \r\n"
            "Date: Thu, 14 Mar 2019 16:28:53 GMT\r\n"
            "Server: Apache/2.2.14 (Win32)\r\n"
            "Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\r\n"
            "Content-Length: 0\r\n"
            "Content-Type: text/html\r\n"
            "\r\n")


    def __init__(self, thread_id, conn, addr, data=""):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.conn = conn
        self.addr = addr
        self.data = data


    def run(self):        
        #
        # to avoid WinError 10035: 
        # "A non-blocking socket operation could not be completed immediately"
        # which occurs during conn.recv() call
        #
        self.conn.setblocking(False)

        if not self.data:
            print("[=] receiving data!!!")
            data = self.conn.recv(8192)
            self.data = data.decode("utf-8")

        # print("[{0:03d}] recv data ----------[ {0} ]\n==>{1}<==\n".format(self.thread_id, self.data))
        try:
            self._processRequest()
           
        except socket.error as e:
            print("[{:03d}] exception occurs 01: {}".format(self.thread_id, e))
        except ValueError as e:
            print("[{:03d}] exception occurs 02: {}".format(self.thread_id, e))
        except IndexError as e:
            print("[{:03d}] exception occurs 03: {}".format(self.thread_id, e))            
        finally:
            if (self.conn): 
                print("[{:03d}] closing client connection".format(self.thread_id) )
                self.conn.close()
                

    def _processRequest(self):
        # ============ Sample Request Format =======================================================
        # CONNECT null-byte.wonderhowto.com:443 HTTP/1.1
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
        # Proxy-Connection: keep-alive
        # Connection: keep-alive
        # Host: null-byte.wonderhowto.com:443        
        # ==========================================================================================

        # self.conn.send(self.static_resp.encode("utf-8"))
        
        webserver = ""
        port = -1
        protocol = ""

        #
        # Fetching webserver address and port from 
        # the very first line of request        
        #
        first_line = self.data.split('\n')[0]

        #
        # item at index 1 of first-line is the webserver/website/target server address
        #
        url = first_line.split(' ')[1]

        temp_index = url.find("://")
        if (temp_index != -1):
            #
            # skip "://" and get the rest of url
            # the 'url' may be like
            # <ip-address>:<port>
            #
            protocol = url[:temp_index]
            url = url[(temp_index + 3):]
            
        index_p = url.find(":")
        index_r = url.find("/")
        if (index_r == -1): index_r = len(url)

        if (index_p == -1):
            #
            # do not found the port index ':' in url
            # webserver is considered upto location of '/'
            # absense of port means default 'port-80'
            #
            webserver = url[:index_r]
            port = portForService(protocol)
        else:
            #
            # port index has been found
            #
            webserver = url[:index_p]
            port = int(url[index_p + 1:index_r] )

        #
        # connecting to remote server (ie destination webserver)
        # pass self.data ie original request to it
        # and send back the response to client
        #
        self.targetHTTPServer(webserver, port)
        # self.proxyServer("10.144.1.11", 8080)


    def targetHTTPServer(self, webserver, port):
        print("[{:03d}] connecting: server => {} : {}".format(self.thread_id, webserver, str(port)) )
        try:
            sock_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_web.setblocking(False)
            sock_web.connect((webserver, port))
            sock_web.sendall(str.encode(self.data))

            while True:
                ready = select.select([sock_web], [], [], 5)
                if ready[0]:                
                    reply = sock_web.recv(4096)
                    if (len(reply) > 0):
                        self.conn.send(reply)
                        dar = float(len(reply))
                        dar = float(dar / 1024)
                        dar = "%.3s" % (str(dar))
                        dar = "%s KB" % (dar)
                        print("[{:03d}] request done: {} => {} <=".format(self.thread_id, str(self.addr[0]), str(dar)) )
                    else:
                        print("[{0:03d}] recv complete, breaking the loop -----[ {0:d} ]".format(self.thread_id))
                        break
        except socket.error as e:
            print("[{:03d}] exception occurs: {}".format(self.thread_id, e))
        # except:
        #     print("[{:03d}] exception occurs: unknown exception".format(self.thread_id))
        finally:
            print("[{:03d}] closing webserver socket".format(self.thread_id))
            sock_web.close()