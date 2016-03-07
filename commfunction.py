#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11

import telnetlib
import logging


def str2list(s, char=' '):
    # input a string
    # convert to a python list
    # remove the rear \n
    # return this list
    s = s.split(char)
    return map(lambda x: x.replace('\n', ''), s)


def convert2csv(s):
    # input a list
    # convert to CSV format
    csv = ''
    for i in range(0, len(s)):
        if i == len(s)-1:
            csv = csv + s[i]
            break
        csv = csv + s[i] + ','
    return csv


def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]


def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)


def get_all_network_id(ip_range):
    start, end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start, end+1) if num & 0xff]


def test_host_connection(host, port=22, timeout=3):
    # test if the host is able to be connected via port
    try:
        test = None
        test = telnetlib.Telnet(host, port, timeout)
    except Exception, e:
        logging.warning('Telnetting Host %s on PORT %s Error: %s' % (host, port, e))
        return 1
    finally:
        if test:
            test.close()
    return 0
