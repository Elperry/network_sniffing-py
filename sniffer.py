import time
import _thread
import ifaddr
import socket
import struct
import datetime
import binascii
from PyQt5.QtWidgets import QTableWidgetItem
# ip Protocols
# 1-> ICMP
# 2-> IGMP
# 6-> TCP
# 9-> IGRP
# 17->UDP
# 47->GRE
# 50->ESP
# 51->AH
# 57->SKIP
# 88->EIGRP
# 89->OSPF
# 115->L2TP


#unpack ICMP Packet
def icmp_packet(data):
    icmp_type,code,checksum = struct.unpack('! B B H',data[:4])
    return icmp_type , code , checksum , data[4:]

# unpack TCP
def tcp_segment(data):
    (src_port,dest_port,seqN , ack , offset_reserved_flags)=struct.unpack('! H H L L H',data[:14])
    offset = (offset_reserved_flags>>12)*4
    flag_urg=(offset_reserved_flags & 32)>>5
    flag_ack=(offset_reserved_flags & 16)>>4
    flag_psh=(offset_reserved_flags & 8)>>3
    flag_rst=(offset_reserved_flags & 4)>>2
    flag_syn=(offset_reserved_flags & 2)>>1
    flag_fin=(offset_reserved_flags & 1)
    return src_port , dest_port , seqN , ack,flag_urg,flag_ack,flag_psh,flag_rst,flag_syn,data[offset:]

#format multi line get_data
def format_multi_line(prefix , string , size=80):
    size -=len(prefix)
    if isinstance(string,bytes):
        string=''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2 :
            size -= 1
    return '\n'.join([prefix+line for line in textwrap.warp(string,size)])

def udp_segment(data):
    src_port , dest_port , size = struct.unpack('! H H 2x H',data[:8])
    return src_port , dest_port , size , data[8:]
def ethernet_frame(data):
    dest_mac,src_mac,proto = struct.unpack('! 6s 6s H',data[:14])
    src_mac =mac(src_mac)
    return mac(dest_mac),src_mac,socket.htons(proto),data[14:]

# return proper mac address
def mac(bytes_addr):
    bytes_str=map('{:02x}'.format,bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

def ipv4(addr):
    return '.'.join(map(str,addr))

def ipv4_packet(data):
    version_header_length =data[0]
    version =version_header_length>>4
    header_length = (version_header_length & 15)*4
    ttl , proto , src , dest = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    src=ipv4(src)
    dest=ipv4(dest)
    return version,header_length,ttl,proto,src,dest,data[header_length:]

class sniffer:
    # this class contains the data and the function
    def __init__(self):
        self.interface = ""
        self.filter = ""
        self.run = False

    def findInterfaces(self):
        #out in form [interfacename , ip]
        out=[]
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            x= (adapter.nice_name)
            for ip in adapter.ips:
                y= (ip.ip)
            out.append([x,y])
        return out
    def selectInterface(self,i):
        self.interface=i
    def setFilter(self,f):
        self.filter=f
    def start(self,uiform):
            try:
               _thread.start_new_thread(self.sniff,(uiform,))
            except Exception as e:
               print ("Error: unable to start thread" , e)
    def sniff(self,uiform):
        try:
            uiform.Ui.tableWidget.setRowCount(0)
            rowNum=0
            while self.run:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                s.bind((self.interface, 0))
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
                raw_data , addr =s.recvfrom(65565)
                dest_mac,src_mac ,protocol , data =ethernet_frame(raw_data)
                print("src: ",src_mac , "dst:",dest_mac)
                version,headerL,ttl,proto,src,dest,data=ipv4_packet(raw_data)
                # add data to tableWidget
                if(proto == 6):
                    proto='TCP'
                else:
                    if(proto == 17):
                        proto='UDP'
                    else:
                        if(proto==1):
                            proto="ICMP"
                        else:
                            if(proto==115):
                                proto='L2TP'
                self.filter=self.filter.upper()
                if(self.filter == "" or self.filter == proto):
                    uiform.Ui.tableWidget.insertRow(rowNum)
                    uiform.Ui.tableWidget.setItem(rowNum,0,QTableWidgetItem(str(datetime.datetime.now())))
                    uiform.Ui.tableWidget.setItem(rowNum,1,QTableWidgetItem(str(src)))
                    uiform.Ui.tableWidget.setItem(rowNum,2,QTableWidgetItem(str(dest)))
                    uiform.Ui.tableWidget.setItem(rowNum,3,QTableWidgetItem(str(proto)))
                    uiform.Ui.tableWidget.setItem(rowNum,4,QTableWidgetItem(str(len(data))))
                    uiform.Ui.tableWidget.setItem(rowNum,5,QTableWidgetItem(str(data)))
                    rowNum +=1
                #s.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        except Exception as e:
            print("err :", e)
        return 5
