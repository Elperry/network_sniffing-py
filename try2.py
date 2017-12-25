import ifaddr

adapters = ifaddr.get_adapters()

for adapter in adapters:
    print (adapter.nice_name)
    for ip in adapter.ips:
        print (ip.ip)


import socket

# the public network interface
HOST = socket.gethostbyname(socket.gethostname())
#HOST='192.168.2.2'
print(HOST)
# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# receive a package
print(s.recvfrom(65565))

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
