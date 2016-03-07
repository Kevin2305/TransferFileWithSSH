#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11
COMMANDS = [
            'ls /root/.ssh || mkdir -p /root/.ssh',
            'ls /root/.ssh'
            ]
HOST_FILE = 'fil1e.csv'
IP_RANGE = '10.10.68.51-10.10.68.55'
SRC_FILE = '/root/.ssh/authorized_keys'
DEST_FILE = '/root/.ssh/authorized_keys'
SRC_FILE_HOST = {'host': '10.10.68.213',
                 'username': 'root',
                 'password': 'root@123',
                 'ssh_port': 3389}
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = 'root@123'
TMP_FILE = 'temp'
