"""
import sys
from scapy.all import *
from scapy.all import conf

a=show_interfaces()
b=a.split(' ')
print (b)
"""
import psutil
d = psutil.net_if_stats()
h=[]
for i in d.keys():
    if "Loopback" not in i:
          #  print (i)
            h.append(i)
