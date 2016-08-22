__author__ = 'jo'
# python 3.4 version

import datetime
import dropbox
import ipgetter
import platform
import json
import logging
import os
import config


app_key = config.keys['app_key']
app_secret = config.keys['app_secret']
token = config.keys['token']


def get_logger():
    logger = logging.getLogger("logging_ipchecker")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("ip_checker.log")
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def read_ip_mem():
    with open(os.path.join(os.getcwd(), 'ip_in_memory.json'), 'r') as ip:
        ip_memory = json.load(ip)
        logger.debug('ip_in_memory is ->{}'.format(ip_memory['ip']))
        return ip_memory


def compare_ip(ip_memory, ip):
    if ip_memory['ip'] != ip:
        logger.debug('ip_in_memory changed to->{}'.format(ip))
        write_ip_mem(ip)
        return 1
    else:
        logger.debug('ip_checked-> {} same as  ip_in_memory-> {}'.format(ip, ip_memory['ip']))
        return 0


def write_ip_mem(ip):
        with open('ip_in_memory.json', 'w') as f:
            ipJSON = {'ip': ip}
            json.dump(ipJSON, f)
            return 1

def ip_check():
    ip = ipgetter.myip()
    logger.debug('ip_checked is ->{}'.format(ip))
    return ip


def ip_in_memory(ip):
    ip_memory = read_ip_mem()
    comparism = compare_ip(ip_memory, ip)
    if comparism == 1:
        ip_to_dropbox(ip)


def ip_to_dropbox(ip):
    with open('myip_{}.csv'.format(platform.system()), 'a') as f:
        f.write(str(datetime.datetime.now()) + '|' + ip + '|' + platform.python_version() + '|' + platform.system() + '|' + '\n')
        logger.debug('actual ip ->{}'.format(ip))
    try:
        client = dropbox.client.DropboxClient(token)
        dropFile = open('myip_{}.csv'.format(platform.system()), 'rb')
        dropFileResponse = client.put_file('myip_{}.csv'.format(platform.system()), dropFile, overwrite=True)
        logger.debug('uploaded {}'.format(dropFileResponse))

    except Exception as e:
        with open('myip_error_log_{}.csv'.format(platform.system()), 'a') as ferr:
            ferr.write(str(e))


if __name__ == "__main__":
    logger = get_logger()
    ip = ip_check()
    ip_in_memory(ip)
