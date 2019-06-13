# Scan-IP-MAC

用于扫描局域网下存活的主机IP地址以及MAC地址

```python
Scan_IP&MAC_socket.py
```

利用socket模块

```python
Scan_IP&MAC_netifaces.py
```

利用netiface模块

### 已知bug

Scan_IP&MAC_socket.py 在有虚拟网卡的时候无法确定正确的网关地址