import json


def read_ip():
    with open('ip_in_memory.json', 'r') as ip:
        ip_memory = json.load(ip)
        print('ip_in_memory is ->{}'.format(ip_memory['ip']))
        return ip_memory


def compare_ip(ip_memory, ip_check):
    if ip_memory['ip'] != ip_check:
        print('ip in memory changed to->{}'.format(ip_memory))
        write_ip(ip_check)
        return 1
    else:
        print('ip_checked->{} same as  ip_in_memory->{}'.format(ip_check, ip_memory))
        return 0


def write_ip(ip_check):
        with open('ip_in_memory.json', 'w') as f:
            ipJSON = {'ip': ip_check}
            json.dump(ipJSON, f)

            return 1


if __name__ == "__main__":
    read_ip()
    compare_ip(read_ip(), ip_check="85.138.189.219")
