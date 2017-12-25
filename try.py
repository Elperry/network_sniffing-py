import socket
import struct
import textwrap
from scapy.all import *
from winpcapy import *
import ifaddr



def main():
    #HOST = socket.gethostbyname(socket.gethostname())
	HOST='192.168.2.5'
	print(HOST)
	# create a raw socket and bind it to the public interface
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
	s.bind((HOST, 0))
	s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	raw_data , addr =s.recvfrom(65565)
	dest , src , proto , data = ethernet_frame(raw_data)
	print('\nEthernet Frame: ')
	print('dest: {} , src: {} , Protocol: {}'.format(dest , src , proto))
	s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


#unpack ethernet frame
def ethernet_frame(data):
    dest_mac,src_mac,proto = struct.unpack('! 6s 6s H',data[:14])
    return mac(dest_mac),mac(src_mac),socket.htons(proto),data[14:]

# return proper mac address
def mac(bytes_addr):
    bytes_str=map('{:02x}'.format,bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

main()
