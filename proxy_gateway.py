import socket
import select
import sys
import time
import enum

from simx_http.client_handler import clientHandlerThread
# import simxHTTP.httpClient

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
                    clientHandlerThread(id, conn, addr).start()
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