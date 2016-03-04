#!/usr/bin/python
# -*- coding: utf-8 -*-
# python 2.7.11
import paramiko
import telnetlib
import logging
import commfunction
import Globals

#logging.basicConfig(level=logging.DEBUG)


def open_ssh_connection(user, password, host, ssh_port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=ssh_port, username=user, password=password)
        print('SSH connected')
        return client
    except Exception as e:
        print(e)
        return


def execute_commands(ssh_client, commands):
    for i in range(len(commands)):
        stdin, stdout, stderr = ssh_client.exec_command(commands[i])
    err_list = stderr.readlines()
    if len(err_list) > 0:
        print('%s has errors %s' % (commands[i], err_list[0]))
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


def test_host_connection(host, port=22, timeout=3):
    # test if the host is able to be connected via port
    try:
        test = None
        test = telnetlib.Telnet(host, port, timeout)
    except Exception as e:
        logging.debug('Host Testing Connection %s' % e)
        return 1
    finally:
        if test:
            test.close()
    return 0


def get_host_file_content(file_path):
    result = []
    item = {}
    with open(file_path, 'r') as f:
        titles = commfunction.str2List(f.readline(), ',')
        logging.debug(titles)
        content = f.readline()
        while content:
            content = commfunction.str2List(content, ',')
            logging.debug(content)
            if len(titles) == len(content):
                for i in range(len(titles)):
                    item[titles[i]] = content[i]
                result.append(item)
            else:
                return
            content = f.readline()
        return result


def get_all_network_id(start_id, end_id, mask):
    start_addr = commfunction.str2List(start_id, '.')
    end_addr = commfunction.str2List(end_id, '.')
    mask_addr = commfunction.str2List(mask, '.')

    ip_list = [int(start_addr[0]), int(start_addr[1]), int(start_addr[2]), int(start_addr[3])]
    ip_flag = [0, 0, 0, 0]
    for i in range(4):
        if ip_list[i] != (int(start_addr[i]) & int(mask_addr[i])):
            ip_flag[i] = 1

    a, b, c, d = 0, 1, 2, 3
    while ip_list[d] < 255 and ip_flag[d] == 1:
        ip_list[d] = ip_list[d] + 1
        ip_addr = str(ip_list[a]) + str(ip_list[b]) + str(ip_list[c]) + str(ip_list[d])





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
    print get_host_file_content(Globals.FILEPATH)
