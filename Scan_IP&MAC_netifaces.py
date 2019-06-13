import threading
import time

import Get_Organization
import netifaces
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1


def get_local_net_netifaces():
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
            except KeyError:
                pass
    print('LocalIP:\t' + routingIPAddr)
    print('---------------------------------------------------------')
    localipnums = routingIPAddr.split('.')
    # print(localipnums)
    localipnums.pop()
    # print(localipnums)
    localipnet = '.'.join(localipnums)
    # print(localipnet)
    return localipnet


localnet = get_local_net_netifaces()


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
