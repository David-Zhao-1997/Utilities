#!/usr/bin/python
import os
import platform
import subprocess
import sys


def killProcessWin(port):
    p = subprocess.Popen("cmd.exe /c" + "netstat -aon|findstr \"" + str(port) + "\"", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    curLine = p.stdout.readline()
    while curLine != b'':
        lineArr = curLine.split(" ".encode())
        pid = int(lineArr[-1].replace(os.linesep.encode(), "".encode()))
        try:
            if pid != 0:
                subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i" % pid, shell=True)
                print("pid : " + str(pid), "", "killed")
            else:
                print("nothing to kill")
        except OSError:
            pass
        curLine = p.stdout.readline()
    p.wait()


def killProcessUnix(port):
    p = subprocess.Popen("lsof -P -i:" + str(port)+" | grep \""+str(port)+"\"", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, shell=True)
    curLine = p.stdout.readline()
    while curLine != b'':
        lineArr = curLine.split()
        pid = lineArr[1].replace(os.linesep.encode(), "".encode())
        result = os.system("kill -9 " + pid)
        if result == 0:
            print("pid : " +pid +" killed")
        else:
           pass
        curLine = p.stdout.readline()
    p.wait()


def killByPlatform(port):
    sysStr = platform.system()
    if sysStr == "Windows":
        killProcessWin(port)
    elif sysStr == "Linux":
        killProcessUnix(port)
    elif sysStr == "Darwin":
        killProcessUnix(port)
    else:
        print("Platform not supported yet!")


killByPlatform(sys.argv[1])
