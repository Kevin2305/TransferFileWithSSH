#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11
import os
import sys

def str2List(s,char=' '):
    # input a string
    # convert to a python list
    # remove the rear \n
    # return this list
    s = s.split(char)
    return map(lambda x : x.replace('\n','') , s)

def convert2CSV(s):
    # input a list
    # convert to CSV format
    csv = ''
    for i in range(0,len(s)):
        if i == len(s)-1:
            csv = csv + s[i]
            break
        csv = csv + s[i] + ','
    return csv