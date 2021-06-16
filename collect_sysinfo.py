#!/usr/bin/python3

import subprocess

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
    if not isinstance(cmd, list): return False
    print("CMD: \t", end='')
    print(*cmd, sep=" ")
    return True


def execute_command(cmd):
    print("=" * 60)
    if not show_command(cmd):
        print("[x] expect List, but provided {}".format(type(cmd)))
        return
    out = err = None
    try:
        p = subprocess.Popen(cmd,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        out, err = p.communicate(timeout = 20)
    except subprocess.TimeoutExpired:
        # https://docs.python.org/3/library/subprocess.html
        # The child process is not killed if the timeout expires, 
        # so in order to cleanup properly a well-behaved application should 
        # kill the child process and finish communication
        print("[=] timeout occured")
        p.kill()
        out, err = p.communicate()
    except FileNotFoundError as e:
        err = "exception: {}".format(e).encode()
    except:
        err = "[x] unhandled exception occurs".encode()
    finally:
        if out: print("OUTPUT:\n{}".format(out.decode('utf-8')))
        else: print("ERROR: {}".format(err.decode('utf-8')))


if __name__ == "__main__":
    list(map(execute_command, cmd_list))
    # for c in cmd_list:
    #     try:
    #         execute_command(c)
    #     except FileNotFoundError as e:
    #         print("[X] Exception: {}".format(e))


