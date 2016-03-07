#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11

import telnetlib
import logging
import paramiko


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
        return
    finally:
        if test:
            test.close()
    return 1


def execute_commands(ssh_client, commands):
    for i in range(len(commands)):
        stdin, stdout, stderr = ssh_client.exec_command(commands[i])
    err_list = stderr.readlines()
    if len(err_list) > 0:
        logging.error('command: %s :has errors: %s' % (commands[i], err_list[0]))
        return
    else:
        return 1


def upload_file_via_ssh(ssh_client, lfile, rfile):
    try:
        sftp = ssh_client.open_sftp()
        sftp.put(lfile, rfile)
        logging.info('Sent file %s' % lfile)
        return 1
    except Exception, e:
        logging.error('upload error')
        logging.error(e)
        return


def download_file_via_ssh(ssh_client, rfile, lfile):
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(rfile, lfile)
        logging.info('Got file %s' % rfile)
        return 1
    except Exception, e:
        logging.error('download error')
        logging.error(e)
        return


def open_ssh_connection(host, username, password, ssh_port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=ssh_port, username=username, password=password)
        logging.info(host + ' ssh connected')
        return client
    except Exception, e:
        logging.error(host + ' ssh connection error')
        logging.error(e)
        return


def close_ssh_connection(ssh_client):
    ssh_client.close()
    logging.info('SSH closed')
