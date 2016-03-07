#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11
import paramiko
import logging
import os
import commfunction
import Globals
from multiprocessing import Process, Queue

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug_log.log',
                    filemode='w')


def open_ssh_connection(host, username, password, ssh_port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=ssh_port, username=username, password=password)
        logging.info(host + ' SSH connected')
        return client
    except Exception, e:
        logging.error(host + ' ssh connection error')
        logging.error(e)
        return


def execute_commands(ssh_client, commands):
    for i in range(len(commands)):
        stdin, stdout, stderr = ssh_client.exec_command(commands[i])
    err_list = stderr.readlines()
    if len(err_list) > 0:
        logging.error('command: %s :has errors: %s' % (commands[i], err_list[0]))
        return 1
    else:
        return 0


def upload_file_via_ssh(ssh_client, lfile, rfile):
    try:
        '''
        conn = paramiko.Transport((hostname, port))
        conn.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(conn)
        '''
        sftp = ssh_client.open_sftp()
        sftp.put(lfile, rfile)
        logging.info('Sent file %s' % lfile)
        return 0
    except Exception, e:
        logging.error('upload error')
        logging.error(e)
        return 1


def download_file_via_ssh(ssh_client, rfile, lfile):
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(rfile, lfile)
        logging.info('Got file %s' % rfile)
        return 0
    except Exception, e:
        logging.error('download error')
        logging.error(e)
        return 1


def close_ssh_connection(ssh_client):
    ssh_client.close()
    logging.info('SSH closed')


def get_host_file_content(file_path):
    result = []
    with open(file_path, 'r') as f:
        f.readline()
        content = f.readline()
        while content:
            content = commfunction.str2list(content, ',')
            logging.info(content)
            result.append(content)
            content = f.readline()
        return result


def get_origin_file(src_path, dest_path, kwargs):
    conn_client = open_ssh_connection(**kwargs)
    if conn_client:
        download_file_via_ssh(conn_client, src_path, dest_path)
        close_ssh_connection(conn_client)


def distribute_file():
    get_origin_file(Globals.SRC_FILE, Globals.TMP_FILE, Globals.SRC_FILE_HOST)
    hosts = get_host_file_content(Globals.HOST_FILE)
    with open('distribute_result.txt', 'w') as f:
        for x in range(len(hosts)):
            if not commfunction.test_host_connection(hosts[x][0]):
                client = open_ssh_connection(hosts[x][0], hosts[x][1], hosts[x][2])
                if client:
                    if not execute_commands(client, Globals.COMMANDS):
                        if not upload_file_via_ssh(client, Globals.TMP_FILE, Globals.DEST_FILE):
                            f.write(hosts[x][0] + ' OK\n')
                            close_ssh_connection(client)
                            continue
            f.write(hosts[x][0] + ' Failed\n')
    os.remove(Globals.TMP_FILE)


def scan_available_hosts():
    get_origin_file(Globals.SRC_FILE, Globals.TMP_FILE, Globals.SRC_FILE_HOST)
    ips = commfunction.get_all_network_id(Globals.IP_RANGE)
    with open('scan_result.txt', 'w') as f:
        for ip in ips:
            if not commfunction.test_host_connection(ip):
                client = open_ssh_connection(ip, Globals.USERNAME, Globals.PASSWORD)
                if client:
                    if not execute_commands(client, Globals.COMMANDS):
                        if not upload_file_via_ssh(client, Globals.TMP_FILE, Globals.DEST_FILE):
                            f.write(ip + ' OK\n')
                            close_ssh_connection(client)
                            continue
            f.write(ip + ' Failed\n')
    os.remove(Globals.TMP_FILE)


if __name__ == '__main__':
    #distribute_file()
    scan_available_hosts()

