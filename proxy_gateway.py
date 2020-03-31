import socket
import select
import sys
import threading
import time
import enum

"""
https://null-byte.wonderhowto.com/how-to/sploit-make-proxy-server-python-0161232/

Types of Proxy:
1) PHP Proxy
2) CGI Proxy
3) HTTP Proxy
4) Gateway Proxy    <== [the one implementing here]
5) DNS Proxy
6) Anonymous HTTPS Proxy
7) Suffix Proxy
8) TOR Proxy
9) I2P Anonymous Proxy

https://www.geeksforgeeks.org/creating-a-proxy-webserver-in-python-set-1/

"""

class ProxyType(enum.Enum):
    direct = 1
    proxy = 2


def nextValueOf(text, src_list):
    print(src_list)
    x = len(src_list)
    flag = 0
    for i in range(x):
        if (flag == 1): return src_list[i]
        if (src_list[i] == text): flag = 1      # pattern found, now need to return the next value 
    raise ValueError


def portForService(protocol):
    if ("http" == protocol):
        return 80
    elif ("https" == protocol):
        return 443
  

class clientThread(threading.Thread):
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
        if not self.data:
            print("[=] receiving data!!!")
            data = self.conn.recv(8192)
            self.data = data.decode("utf-8")

        print("[{0:03d}] recv data ----------[ {0} ]\n==>{1}<==\n".format(self.thread_id, self.data))
        try:
            """
            CONNECT null-byte.wonderhowto.com:443 HTTP/1.1
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
            Proxy-Connection: keep-alive
            Connection: keep-alive
            Host: null-byte.wonderhowto.com:443
            """
            # first_line = self.data.split('\n')[0]
            # url = first_line.split(' ')[1]

            self.conn.send(self.static_resp.encode("utf-8"))
            
            webserver = ""
            port = -1
            protocol = "http"

            # url = nextValueOf("CONNECT", self.data.split('\n')[0].split(' ') )
            first_line = self.data.split('\n')[0]
            url = first_line.split(' ')[1]
            temp_index = url.find("://")
            temp_url = ""

            if (temp_index == -1):
                # if do not found "://" then 
                # nextValue of "CONNECT" is the url
                temp_url = url
            else:
                # skip "://" and get the rest of url
                temp_url = url[(temp_index + 3):]   
                protocol = url[:temp_index]
                
            index_p = temp_url.find(":")
            index_r = temp_url.find("/")
            if (index_r == -1): index_r = len(temp_url)

            # if (index_p == -1 or index_r < index_p):
            if (index_p == -1):
                # do not found the port index ':' in url
                # webserver is considered upto location of '/'
                webserver = temp_url[:index_r]
                port = portForService(protocol)
            else:
                # port index has been found
                webserver = temp_url[:index_p]
                port = int(temp_url[index_p + 1:index_r] )

            # print("[{:03d}] connecting=> {}:{}".format(self.thread_id, webserver, port))

            #
            # code added on 31-Mar-2020
            # connecting to remote server (ie destination webserver)
            # pass self.data ie original request to it
            # and send back the response to client
            #
            self.targetHTTPServer(webserver, port)
            # self.proxyServer("10.144.1.11", 8080)
           
        except socket.error as e:
            print("[{:03d}] exception occurs 01: {1}".format(self.thread_id, e))
        except ValueError as e:
            print("[{:03d}] exception occurs 02: {1}".format(self.thread_id, e))
        except IndexError as e:
            print("[{:03d}] exception occurs 03: {1}".format(self.thread_id, e))            
        finally:
            if (self.conn): 
                print("[{:03d}] closing client connection".format(self.thread_id) )
                self.conn.close()


    def targetHTTPServer(self, webserver, port):
        print("[{:03d}] connecting: server => {} : {}".format(self.thread_id, webserver, str(port)) )
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.sendall(str.encode(self.data))

            while True:
                reply = s.recv(8192)
                if (len(reply) > 0):
                    self.conn.send(reply)
                    dar = float(len(reply))
                    dar = float(dar / 1024)
                    dar = "%.3s" % (str(dar))
                    dar = "%s KB" % (dar)
                    print("[{:03d}] request done: {} => {} <=".format(self.thread_id, str(addr[0]), str(dar)) )
                else:
                    print("[{0:03d}] issue occur, breaking the loop -----[ {0:d} ]".format(self.thread_id))
                    break
        except socket.error as e:
            print("[{:03d}] exception occurs: {}".format(self.thread_id, e))
        except:
            print("[{:03d}] exception occurs: unknown exception".format(self.thread_id))
        finally:
            if (s): s.close()
            self.conn.close()
            

if __name__ == "__main__":

    max_connection = 5
    buf_size = 8192
    port = 3139
    proxy_type = ProxyType.direct
    id = 0
    inputs = []
    outputs = []

    try:
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_server.bind(('', port))
        sock_server.listen(max_connection)
        sock_server.setblocking(False)
        print("[=] server started successfully on port {}".format(port))

        inputs.append(sock_server)
        # inputs.append(sys.stdin)
        while inputs:
            print("[=] waiting for new request")
            #
            # need to implement select
            #
            readable, writable, exceptional = select.select (inputs, outputs, inputs, 20)
            for s in readable:
                if s is sock_server:
                    id = id + 1
                    print("[{:03d}] accepting new request".format(id))
                    conn, addr = s.accept()
                    conn.setblocking(True)
                    # data = conn.recv(buf_size)
                    # if (data == "exit" or data == "quit"):
                    #     break

                    # start new thread
                    # clientThread(id, conn, addr, data.decode("utf-8")).start()
                    clientThread(id, conn, addr).start()
                    # print("[=] {} thread started".format(id))

    except KeyboardInterrupt as e:
        print("[=] user interrupt")
        sys.exit(1)

    # except:
    #     print("[-] unknown exception occurs")

    finally:
        if (sock_server):
            sock_server.close()
            print("[=] socket closed")
# --end--