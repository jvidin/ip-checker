__author__ = 'jo'

import datetime
import dropbox
import ipgetter
import platform
import ipmemory

app_key = '6u3nzsyr5kj6isq'
app_secret = 'vdv5u7tk04tdqan'
token = 'uMFjOVN-lEIAAAAAAAAB0OIrQuGRX2IfeWdrhFpfRlcWs37a1FcGr3e3NMu9OQoE'

# python 3.4 version


def ip_check():
    ip = ipgetter.myip()
    print('ip_checked is ->{}'.format(ip))
    return ip


def ip_in_memory(ip):
    ip_memory = ipmemory.read_ip()
    comparism = ipmemory.compare_ip(ip_memory, ip)
    if comparism == 1:
        ip_to_dropbox(ip)


def ip_to_dropbox(ip):
    with open('myip_{}.csv'.format(platform.system()), 'a') as f:
        f.write(str(datetime.datetime.now()) + '|' + ip + '|' + platform.python_version() + '|' + platform.system() + '|' + '\n')
        print('actual ip ', ip_check())
    try:
        client = dropbox.client.DropboxClient(token)
        client2 = dropbox.Dropbox(token)
        print('linked account: ', client.account_info())
        dropFile = open('myip_{}.csv'.format(platform.system()), 'rb')
        dropFileResponse = client.put_file('myip_{}.csv'.format(platform.system()), dropFile, overwrite=True)
        print('uploaded', dropFileResponse)

    except Exception as e:
        print(e)
        with open('myip_error_log_{}.csv'.format(platform.system()), 'a') as ferr:
            ferr.write(str(e))


if __name__ == "__main__":

    ip_in_memory(ip_check())
