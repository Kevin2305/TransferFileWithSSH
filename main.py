#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11
import paramiko
import logging
import commfunction
import Globals

logging.basicConfig(level=logging.DEBUG)


def open_ssh_connection(user, password, host, ssh_port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=ssh_port, username=user, password=password)
        print('SSH connected')
        return client
    except Exception, e:
        print e
        return


def execute_commands(ssh_client, commands):
    for i in range(len(commands)):
        stdin, stdout, stderr = ssh_client.exec_command(commands[i])
    err_list = stderr.readlines()
    if len(err_list) > 0:
        print('command: %s :has errors: %s' % (commands[i], err_list[0]))
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
        print('Sent file %s' % lfile)
        print('Sent file')
        return 0
    except Exception as e:
        print(e)
        return 1


def download_file_via_ssh(ssh_client, rfile, lfile):
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(rfile, lfile)
        print('Got file %s' % rfile)
        print('Got file')
        return 0
    except Exception as e:
        print(e)
        return 1


def close_ssh_connection(ssh_client):
    ssh_client.close()
    print("SSH closed")


def get_host_file_content(file_path):
    result = []
    item = {}
    with open(file_path, 'r') as f:
        titles = commfunction.str2list(f.readline(), ',')
        logging.debug(titles)
        content = f.readline()
        while content:
            content = commfunction.str2list(content, ',')
            logging.debug(content)
            if len(titles) == len(content):
                for i in range(len(titles)):
                    item[titles[i]] = content[i]
                result.append(item)
            else:
                return
            content = f.readline()
        return result


def main():
    ssh_info101 = {'host': '10.10.68.213',
                   'ssh_port': 3389,
                   'user': 'root',
                   'password': 'root@123'}
    conn_client101 = open_ssh_connection(**ssh_info101)
    if conn_client101:
        if not execute_commands(conn_client101, Globals.COMMANDS):
            close_ssh_connection(conn_client101)


if __name__ == '__main__':
    print commfunction.get_all_network_id(Globals.IP_RANGE)
    commfunction.telnet_host_connection('10.10.10.10')
