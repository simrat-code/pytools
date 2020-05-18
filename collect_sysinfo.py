#!/usr/bin/python3

import subprocess
import types
import time

cmd_date = ["date", "+%a %d-%b-%Y %H:%M"]
cmd_kernel = ["uname", "-r"]
cmd_release = ["lsb_release", "-a"]
cmd_free = ["free", "-m"]
cmd_uptime = ["uptime"]
cmd_ip_a = ["ip", "a"]
cmd_ip_r = ["ip", "r"]

cmd_list = [
        cmd_date,
        cmd_kernel,
        cmd_release,
        cmd_uptime,
        cmd_free,
        cmd_ip_r,
        cmd_ip_a
        ]

def show_command(cmd):
    if type(cmd) != list:
        raise TypeError
    print("CMD: \t", end='')
    print(*cmd, sep=" ")


def execute_command(cmd):
    try:
        show_command(cmd)
    except TypeError:
        print("expect List, but provided {}".format(type(cmd)))
        return

    p = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    try:
        out, err = p.communicate(timeout = 20)
    except TimeoutExpired:
        print("[=] timeout occured")
        p.kill()
        out, err = p.communicate()

    if out:
        print("OUTPUT:\n{}".format(out.decode('utf-8')))
    else:
        print("ERROR:\n{}".format(err.decode('utf-8')))


def separator():
    print("=" * 60)


if __name__ == "__main__":
    for c in cmd_list:
        separator()
        execute_command(c)


