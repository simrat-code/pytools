#!/usr/bin/env python

import subprocess


def fetch_private_ip():
    #
    # command: ip addr | grep inet | grep -v inet6
    #
    try:
        p1 = subprocess.Popen(["ip", "addr"],
                                stderr = subprocess.STDOUT,
                                stdout = subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "inet"],
                                stdin = p1.stdout,
                                stderr = subprocess.STDOUT,
                                stdout = subprocess.PIPE)
        p3 = subprocess.Popen(["grep", "-v", "inet6"],
                                stdin = p2.stdout,
                                stdout = subprocess.PIPE)
        output = p3.stdout.read()
    except:
        output = "failed to execute command.\r\n"
    return output.decode('utf-8')


def fetch_public_ip():
    cmd = ['/opt/pytools/check_webservice.py',
           '-a', 'myip.dnsdynamic.org',
           '-p', '80',
           '-r', '/']
    p1 = subprocess.Popen(cmd,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)
    out, err = p1.communicate()

    if not out:
        return err
    else:
        return out


if __name__ == "__main__":
    print "\n"
    print "---------------------------------------------------------------------------"
    print "Private IP detail:"
    print "---------------------------------------------------------------------------"
    for line in fetch_private_ip().splitlines():
        print line.strip()

    print "\n"
    print "---------------------------------------------------------------------------"
    print "Public IP detail:"
    print "---------------------------------------------------------------------------"
    print fetch_public_ip()
    
# -- end --        


