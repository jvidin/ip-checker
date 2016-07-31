__author__ = 'jo'

import datetime
import dropbox
import ipgetter
import platform
import json
import logging

app_key = '6u3nzsyr5kj6isq'
app_secret = 'vdv5u7tk04tdqan'
token = 'uMFjOVN-lEIAAAAAAAAB0OIrQuGRX2IfeWdrhFpfRlcWs37a1FcGr3e3NMu9OQoE'

# python 3.4 version

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
    with open('ip_in_memory.json', 'r') as ip:
        ip_memory = json.load(ip)
        #print('ip_in_memory is ->{}'.format(ip_memory['ip']))
        logger.debug('ip_in_memory is ->{}'.format(ip_memory['ip']))
        return ip_memory


def compare_ip(ip_memory, ip):
    if ip_memory['ip'] != ip:
        #print('ip in memory changed to->{}'.format(ip_memory))
        logger.debug('ip_in_memory changed to->{}'.format(ip))
        write_ip_mem(ip)
        return 1
    else:
        #print('ip_checked->{} same as  ip_in_memory->{}'.format(ip_check, ip_memory))
        return 0


def write_ip_mem(ip):
        with open('ip_in_memory.json', 'w') as f:
            ipJSON = {'ip': ip}
            json.dump(ipJSON, f)
            return 1

def ip_check():
    ip = ipgetter.myip()
    #print('ip_checked is ->{}'.format(ip))
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
        #print('actual ip ', ip_check())
        logger.debug('actual ip ->{}'.format(ip))
    try:
        client = dropbox.client.DropboxClient(token)
        #print('linked account: ', client.account_info())
        dropFile = open('myip_{}.csv'.format(platform.system()), 'rb')
        dropFileResponse = client.put_file('myip_{}.csv'.format(platform.system()), dropFile, overwrite=True)
        #print('uploaded', dropFileResponse)
        logger.debug('uploaded', dropFileResponse)

    except Exception as e:
        #print(e)
        with open('myip_error_log_{}.csv'.format(platform.system()), 'a') as ferr:
            ferr.write(str(e))


if __name__ == "__main__":
    logger = get_logger()
    ip = ip_check()
    ip_in_memory(ip)
