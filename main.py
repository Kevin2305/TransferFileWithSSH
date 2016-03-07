#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11

import os
from commfunction import *
import Globals

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug_log.log',
                    filemode='w')


def get_host_file_content(file_path):
    result = []
    try:
        with open(file_path, 'r') as f:
            f.readline()
            content = f.readline()
            while content:
                content = str2list(content, ',')
                logging.info(content)
                result.append(content)
                content = f.readline()
            return result
    except Exception, e:
        logging.error('Get Host File Error')
        logging.error(e)
        return


def download_origin_file(src_path, dest_path, kwargs):
    conn_client = open_ssh_connection(**kwargs)
    if conn_client:
        if download_file_via_ssh(conn_client, src_path, dest_path):
            logging.info('source file: ' + src_path)
            logging.info('destination file: ' + dest_path)
            close_ssh_connection(conn_client)
            return 1
        else:
            return
    else:
        return


def distribute_file():
    hosts = get_host_file_content(Globals.HOST_FILE)
    if not hosts or not download_origin_file(Globals.SRC_FILE, Globals.TMP_FILE, Globals.SRC_FILE_HOST):
        logging.error('Download origin file failed')
        return
    with open('distribute_result.txt', 'w') as f:
        for x in range(len(hosts)):
            if test_host_connection(hosts[x][0]):
                client = open_ssh_connection(hosts[x][0], hosts[x][1], hosts[x][2])
                if client:
                    if execute_commands(client, Globals.COMMANDS):
                        if upload_file_via_ssh(client, Globals.TMP_FILE, Globals.DEST_FILE):
                            f.write(hosts[x][0] + ' OK\n')
                            close_ssh_connection(client)
                            continue
            f.write(hosts[x][0] + ' Failed\n')
    if os.path.exists(Globals.TMP_FILE):
        os.remove(Globals.TMP_FILE)


def scan_ip_range_to_add_trust():
    ips = get_all_network_id(Globals.IP_RANGE)
    if not len(ips) or not download_origin_file(Globals.SRC_FILE, Globals.TMP_FILE, Globals.SRC_FILE_HOST):
        logging.error('Download origin file failed')
        return
    with open('scan_result.txt', 'w') as f:
        for ip in ips:
            if not test_host_connection(ip):
                client = open_ssh_connection(ip, Globals.DEFAULT_USERNAME, Globals.DEFAULT_PASSWORD)
                if client:
                    if not execute_commands(client, Globals.COMMANDS):
                        if not upload_file_via_ssh(client, Globals.TMP_FILE, Globals.DEST_FILE):
                            f.write(ip + ' OK\n')
                            close_ssh_connection(client)
                            continue
            f.write(ip + ' Failed\n')
    if os.path.exists(Globals.TMP_FILE):
        os.remove(Globals.TMP_FILE)


if __name__ == '__main__':
    distribute_file()
    scan_ip_range_to_add_trust()

