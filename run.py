#!/usr/bin/python3
#coding:utf-8

import os
import sys
from init import group
#from init import analyze



def run():
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    os.chdir(dirname)
    group.GroupMessage().main()


if __name__ == '__main__':
    run()

