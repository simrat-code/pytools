#!/usr/bin/env python3

import subprocess
#import paramiko
import argparse
import sys
import os

cmd_listkey = ['ssh-add','-l']
cmd_pull = ['git', 'pull']
cmd_status = ['git', 'status', '-s']
cmd_push = ['git', 'push']

git_repo = []

def loadRepoPath():
    if 'HOME' in os.environ:
        home_path = os.environ['HOME']
    elif 'UserProfile' in os.environ:
        home_path = os.environ['UserProfile']
    else:
        raise KeyError('Please set environment variable, HOME or UserProfile')
    fname = home_path +'/.simx/git-local-repo.conf'
    with open(fname, 'r') as fp:
        while True:
            line = fp.readline().strip()
            if not line: break
            if line[0] == '#': continue
            git_repo.append(line)

def runCommand(cmd, path="."):
    subprocess.run(cmd,
            cwd = path,
            timeout = 10,
            stdout = sys.stdout,
            stderr = sys.stdout)

def gitPull(path):
    printSep()
    print("[=] git pull ->", path.rpartition('/')[2])
    runCommand(cmd_pull, path)

def gitPush(path):
    printSep()
    print("[=] git push ->", path.rpartition('/')[2])
    runCommand(cmd_push, path)

def gitStatus(path):
    printSep()
    print("[=] git status ->", path.rpartition('/')[2])
    runCommand(cmd_status, path)

def showKey():
    print('\n[=] following keys are added:')
    runCommand(cmd_listkey)

def printSep():
    print('-' * 37)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull", 
            action = "store_true",
            help="fetch from and integrate with local branch")
    parser.add_argument("--status", 
            action = "store_true",
            help="show the working tree status")
    parser.add_argument("--show",
            action = "store_true",
            help="show local repo paths")
    parser.add_argument("--push",
            action = "store_true",
            help="push local changes to master")
    args = parser.parse_args()

    loadRepoPath()
    longest = max([len(r) for r in git_repo])

    if args.pull:
        showKey()
        if input("[git pull <- master] continue <y/n>: ") in ['y','Y']:
            list(map(gitPull, git_repo))
            printSep()
        else:
            print('exiting...')
    
    elif args.push:
        showKey()
        if input("[git push -> master] continue <y/n>: ") in ['y','Y']:
            # list(map(gitPush, git_repo))
            # ask which repo to push
            printSep()
            for i, s in enumerate(git_repo):
                print(f"\t{i} : {s:{longest}} : {i}")
            printSep()
            try:
                choice = int(input("[=] repo-id to PUSH -> master: "))
                gitPush(git_repo[choice])
                printSep()
            except:
                print("[x] operation skipped")
        else:
            print('exiting...')
    
    elif args.status:
        list(map(gitStatus, git_repo))
        printSep()
    
    elif args.show:
        showKey()
        print("\n".join(git_repo))
    
    else:
        parser.print_help()

# 0xAA55
