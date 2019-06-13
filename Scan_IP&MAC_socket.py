import socket
import threading
import time

import Get_Organization
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1

host = '192.168.0'


def get_local_net_socket():
    # 获取主机名
    hostname = socket.gethostname()
    print(hostname)
    # 获取主机的局域网ip
    # localip = socket.gethostbyname_ex(hostname)
    info = socket.gethostbyname_ex(hostname)
    ipinfo = info[2]
    if len(info[2]) > 1:
        print(info[2])
    for ip in ipinfo:
        if host in ip:
            localip = ip
            break
    #     # else:
    #     #     exit()
    print(localip)
    print('---------------------------------------------------------')
    localipnums = localip.split('.')
    # print(localipnums)
    localipnums.pop()
    # print(localipnums)
    localipnet = '.'.join(localipnums)
    # print(localipnet)
    # exit()
    return localipnet


localnet = get_local_net_socket()


def get_vlan_ip_and_mac(start=0, stop=255):
    # result = []
    for ipFix in range(start, stop):
        ip = localnet + "." + str(ipFix)
        # print(str(ip))
        # 组合协议包
        arpPkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        res = srp1(arpPkt, timeout=5, verbose=0)
        # print(res)
        if res:
            # result.append({"localIP": res.psrc, "mac": res.hwsrc})
            mac = str(res.hwsrc).upper()
            macr = mac.replace(':', '-')
            result = Get_Organization.get_mac_organization(macr)
            organization = result[0]
            addr = result[1]
            print("IP:" + res.psrc + "\nMAC:" + macr + "\nORGANIZATION:" + organization)  # + '\nADDRESS:' + addr)
            print('---------------------------------------------------------')
    # return result


if __name__ == '__main__':
    start = time.time()
    k = 15
    # 开17个线程
    for i in range(int(255 / k)):
        t = threading.Thread(target=get_vlan_ip_and_mac, args=(i * k, (i + 1) * k))
        t.setDaemon(True)
        t.start()
    t.join()
    stop = time.time()
    print(str(stop - start))
