#!/usr/bin/env python

# python
import logging
import unittest
from unittest.mock import Mock
from randmac import RandMac
import macaddress
import json    
import time
import os
from IxNetwork import IxNet
from ats.log.utils import banner

from pyats.async_ import pcall
from ixia_dhcp_lib import *
import sys

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# xBU-shared genie pacakge
from genie.libs.conf.interface import TunnelTeInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv6Interface, IPv4Address, IPv6Address
from genie.libs.conf.interface import Layer, L2_type, IPv4Addr, IPv6Addr,NveInterface
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface.nxos import Interface
from genie.conf.base.attributes import UnsupportedAttributeWarning
from netaddr.ip import IPNetwork, IPAddress

# Vpc
from genie.libs.conf.vpc import Vpc
from genie.libs.conf.interface.nxos import LoopbackInterface
from genie.libs.conf.interface.nxos import SubInterface

from genie.libs.conf.ospf import Ospf

logger = logging.getLogger(__name__)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# import genie.libs
from genie.libs.conf.bgp import Bgp
import time
from ipaddress import *   
 

import re


def disableDhcpTrust(uut,port):
    cfg = \
        f"""
        interface {port}
        no ip dhcp snooping trust
        ip verify source dhcp-snooping-vlan
        no ip arp inspection trust 
        """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    


def enableDhcpTrust(uut,port):
    cfg = \
        f"""
        interface {port}
        ip dhcp snooping trust
        no ip verify source dhcp-snooping-vlan
        ip arp inspection trust 
        """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    



def clearRouteAll(uut):
    cfg = \
    """
    clear mac add dynamic
    clear ip arp vrf all 
    clear ip route vrf all * 
    clear bgp l2 evpn *
    """ 
    try:  
        uut.configure(cfg,timeout=300)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    




def fhsCliCheck(uut):
    op = uut.execute("show run dhcp")
    for cli in ['ip verify source dhcp-snooping-vlan','evpn','ip verify source dhcp-snooping-vlan','ip arp inspection vlan ']:
        if not cli in op:
            return 0
    return 1    
def format_mac(mac: str) -> str:
    mac = re.sub('[.:-]', '', mac).lower()  # remove delimiters and convert to lower case
    mac = ''.join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    return mac


def ipsgDaiCheck(sw,sw_svi_mac):
    sw.configure("clear ip arp force-delete")
    sw.configure("ping 4.5.0.1") 
    if not '0000.2222.3333' in sw.configure("show ip arp"):
        log.info("GW ARP Not resolved")
        return 0
    if not '64 bytes from 4.5.0.15: icmp_seq=2' in sw.configure("ping 4.5.0.15"):
        log.info("Non E2E traffic ")
        return 0         
    cfg1 = \
    """
    interface vlan 1005
    no ip address dhcp
    ip address 4.5.0.99/16
    no sh
    """    
    cfg2 = \
    """
    interface vlan 1005
    no ip address  
    no sh
    ip address dhcp
    """   

    sw.configure(cfg1)
    sw.configure("clear ip arp force-delete")

    countdown(10)

    sw.configure("ping 4.5.0.1") 
    if '0000.2222.3333' in sw.configure("show ip arp"):
        #sw.configure(cfg2)
        accessSWSviConf(sw,sw_svi_mac)
        return 0    
    if '64 bytes from 4.5.0.15: icmp_seq=2' in sw.configure("ping 4.5.0.15"):
        #sw.configure(cfg2)
        accessSWSviConf(sw,sw_svi_mac)
        return 0   
    accessSWSviConf(sw,sw_svi_mac)
    return 1
    #Verify DAI functionality	Send 2 ARP requests \
    #- one from the source matching DHCP snooping DB and another from source not matching the DB 

    #def ipsgC  heck(uut,snoopDict,leaf_uut_list):
        #Verify IPSG functionality	Send 2 traffic flows -
        #one flow from the source matching DHCP snooping DB and another flow from source not matching the DB


def ipsgCliCheck(uut,ip_address,interface):
    op1= uut.execute(f"sh ip verify source interface {interface}")
    if not ip_address in op1:
        return 0
    return 1

 

def clearIpDhcpBinding(leaf1,sw1):
    cfg1 = \
    """
    interface vlan 1005
    no ip address dhcp
    ip address 4.5.0.99/16
    no sh
    sleep 2
    no ip address 4.5.0.99/16
    ip address dhcp  
    """    

    sw1.configure(cfg1)
    #sw.configure("clear ip arp force-delete")
    countdown(30)

    leaf1.configure('clear ip dhcp snooping binding interface port-channel11')
    sw1.configure("ping 4.5.0.1") 
    if '0000.2222.3333' in sw1.configure("show ip arp"):
        #sw.configure(cfg2)
        #accessSWSviConf(sw,sw_svi_mac)
        sw1.configure(cfg1)
        return 0    
    if '64 bytes from 4.5.0.15: icmp_seq=2' in sw1.configure("ping 4.5.0.15"):
        #sw.configure(cfg2)
        #accessSWSviConf(sw,sw_svi_mac)
        sw1.configure(cfg1)
        return 0  
    sw1.configure(cfg1)    
    return 1   
 


def checkdhcpBinding(uut,snoopDict,leaf_uut_list):
    """
    >>> ll
    ['00:00:00:29:ab:1a', '4.1.4.201', 'infinite', 'static', '1005', 'port-channel11']
    >>> ll[0]
    '00:00:00:29:ab:1a'
    >>> ll[2]
    'infinite'
    >>> ll[1]
    '4.1.4.201'
    >>> ll[2]
    'infinite'
    >>> ll[3]
    'static'
    >>> ll[4]
    '1005'
            for key in staticDict.keys():
            ip_address = key
            mac_address = format_mac(staticDict[key])
    """
    ##import pdb;pdb.set_trace()
    for leaf in leaf_uut_list:
        op1 = leaf.execute("show ip dhcp snooping binding | inc static")
        for line in op1.splitlines():
            if 'static' in line or 'dhcp-snoop' in line :
                mac1 = line.split()[0]
                ip1 = line.split()[1]
                leasetime = line.split()[2]
                type = line.split()[3]
                vlan = line.split()[4]
                inteface = line.split()[5]
                if ip1 in snoopDict.keys(): 
                    if mac1 == format_mac(snoopDict[ip1]):
                        print("Found Snooping entry")
                    else:
                        #import pdb;pdb.set_trace()
                        return False


    return True  
                         
 
def checkCore(uut):
    op = uut.execute('sh core | excl PID | exc --')
    if 'core' in op:
        print(f"Core found in {uut.name}")
        return False 
    return 1
    


def checksnoopBinding(uut,count):
    op1 = uut.execute("sh ip dh sn binding dyn")
    op2 = uut.execute("sh l2route fhs all")
    ip_list1 = []
    ip_list2 = []
    for line in op1.splitlines():
        if 'dhcp-snoop' in line:
            ip1 = line.split()[1]
            ip_list1.append(ip1)
            if not ip1 in op2:
                log.info(f"IP {ip1} not seen in l2route fhs {op2}")
                return False

    for line in op2.splitlines():
        if 'dyn' in line:
            ip2 = line.split()[1]
            ip_list2.append(ip1)
            if not ip2 in op1:
                log.info(f"IP {ip2} not seen in snoop table {op1}")
                return False

    if int(uut.execute("sh ip dh sn binding  evpn | inc dhcp-snoop | count")) < count:
        return False
    elif int(uut.execute("sh ip dh sn binding dyn | inc dhcp-snoop | count")) < count:
        return False               
    return True  
                        
    '''

    for line in op1.splitlines():
        if 'static' in line or 'dhcp-snoop' in line :
            mac1 = line.split()[0]
            ip1 = line.split()[1]
            leasetime = line.split()[2]
            type = line.split()[3]
            vlan = line.split()[4]
            inteface = line.split()[5]
            if not format_mac(mac1) in snoop_mac_list2:
                ##import pdb;pdb.set_trace()
                log.info("++"*10)                
                log.info(f"MAC {mac1} not found in {uut.name}")
                log.info(f'snooping table is {op1}')
                log.info("++"*10)     
                return False                   
    return True  
                        
    '''


def removeAddBgp(uut):
    cfg = uut.execute("sh run bgp  | b feature")
    uut.configure("no feature bgp")
    countdown(2)
    uut.configure(cfg)    
    countdown(2)

def removeAddBgpNeighbor(uut):
    cfg = \
    """
    router bgp 65001
    """
    cfg1 = uut.execute("sh run bgp  | b feature")
    for line in cfg1.splitlines():
        if 'neighbor' in line:
            cfg += f'no {line} \n'
            cfg += f'sleep 4 \n'
            cfg += f'{line} \n'
    uut.configure(cfg1)    
    countdown(2)


def removeArpSuppress(uut):
    cfg = \
    """
    interface nve1
    """
    cfg2 = \
    """
    interface nve1
    """
    cfg1 = uut.execute("sh run int nve 1 | be shut")
    for line in cfg1.splitlines():
        cfg += f'{line} \n'
        if 'suppress-arp' in line:
            cfg += f'no {line} \n'
        cfg += f'{line} \n'            
    uut.configure(cfg)    
    countdown(2)
    return(cfg2)


def CreateDhcpClient(chassisIP):
    pass


def saveConf(uut):
    uut.configure('end')
    uut.execute('copy run start')


def fhsCliEnable(uut,conf_dict):
    """
    2) Enable DHCP snoooping on all leafs , 
    feature dhcp
    ip dhcp snooping vlan <vlan-list> evpn
    3) Enable DAI, IPSG
    ip arp inspection vlan <vlan>
    interface Ethernet1/2
    ip verify source dhcp-snooping-vlan
    4) Enable new bgp AF across the leaf & spine"	"Verify that no error/irrelevant log is seen while configureing the CLI, 
    Reload the UUT after saving configuration
    Verify new CLI's are not lost after reload"

    vxlan_fhs:
      fx301:
        vlan : 1005
            port_list : ['Po11','Po21','Po31']   

    no ip arp inspection vlan 1001 logging dhcp-bindings all
    no ip source binding 4.1.1.7 0000.4114.4117 vlan 1001 interface Ethernet1/7
    no ip source binding 4.1.1.5 0000.4115.4115 vlan 1001 interface Ethernet1/5
    no ip source binding 4.1.1.6 0000.4116.4116 vlan 1001 interface Ethernet1/6
    no ip source binding 4.1.1.8 0000.4118.4118 vlan 1001 interface Ethernet1/8


    """
    vlan_list = conf_dict['vxlan_fhs'][uut.name]['vlan_list']
    port_list = conf_dict['vxlan_fhs'][uut.name]['port_list']
    test_vlan = vlan_list[0]
    #port_list = []
    #for line in uut.execute(f'show span vl {test_vlan} | inc FWD').splitlines():
    #    if not 'peer-link' in line:
    #        port = line.split()[0]
    #        port_list.append(port)


    uut.configure('feature dhcp')
    uut.configure('ip dhcp snooping')
    for vlan in vlan_list:
        uut.configure(f'ip dhcp snooping vlan {vlan} evpn')

    for vlan in vlan_list:
        uut.configure(f'ip arp inspection vlan  {vlan}')

    cfg1 = \
        """
        """
    for port in port_list:
        cfg1 +=f'interface {port} \n'
        cfg1 +=f'ip verify source dhcp-snooping-vlan \n'

    uut.configure(cfg1,timeout=300)




def dhcpStaticBinding(uut,conf_dict):
    """
    no ip arp inspection vlan 1001 logging dhcp-bindings all
    no ip source binding 4.1.1.7 0000.4114.4117 vlan 1001 interface Ethernet1/7
    no ip source binding 4.1.1.5 0000.4115.4115 vlan 1001 interface Ethernet1/5
    no ip source binding 4.1.1.6 0000.4116.4116 vlan 1001 interface Ethernet1/6
    no ip source binding 4.1.1.8 0000.4118.4118 vlan 1001 interface Ethernet1/8
    dhcp_static:
    fx301:
        vlan:
        1005:
            interface_list: ['Po11','Po21','Po31'] 
            ip_address_start: '4.1.4.1' 
            scale: 10
    """
    
    ##import pdb;pdb.set_trace()

    vlan = conf_dict['dhcp_static'][uut.name]['profile1']['vlan']
    intf = conf_dict['dhcp_static'][uut.name]['profile1']['interface']  
    ipaddress = conf_dict['dhcp_static'][uut.name]['profile1']['ip_address_start']
    scale = conf_dict['dhcp_static'][uut.name]['profile1']['scale']
    cfg = \
        """
        """
    staticDict = {}    
    mac = macGenerator()
    for i in range(scale):
        mac1 = mac
        cfg += f"ip source binding {ipaddress} {mac} vlan {vlan} interface {intf} \n"
        staticDict[str(ipaddress)] = mac  
        ipaddress = ip_address(ipaddress)+1
        mac = macGenerator()
        if mac == mac1:
            mac = macGenerator()  
                    

    print(cfg)
    uut.configure(cfg,timeout=300)
    print(conf_dict)
    return(staticDict)



def hostMoveSetup(uut,conf_dict):
    vlan_list = conf_dict['host_move'][uut.name]['vlan_list']
    port_list = conf_dict['host_move'][uut.name]['port_list']

    test_vlan = vlan_list[0]
    port_list_all = []
    for line in uut.execute(f'show span vl {test_vlan} | inc FWD').splitlines():
        if not 'peer-link' in line:
            port = line.split()[0]
            port_list_all.append(port)
    cfgnone = \
        """
        """
    for port in port_list_all:
        cfgnone += f'interface {port} \n'
        cfgnone += f'switchport trunk allowed vlan none \n'

    uut.configure(cfgnone) 

    cfg1 = \
        """
        """
    for port in port_list:
        for vlan in vlan_list:
            cfg1 += f'interface {port} \n'
            cfg1 += f'switchport trunk allowed vlan {vlan} \n'

    uut.configure(cfg1) 


def macGenerator():
    mac1 = str(RandMac("00:00:00:00:00:00", True)).replace("'","")
    segments = mac1.split(':')
    groups = [segments[0:2], segments[2:4], segments[4:]]
    a = [''.join(group) for group in groups]
    mac = '.'.join(a)
    return mac 


def countdown(t):
    t1 = t
    logger.info(f'Start countdown for {t} seconds')
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print("Countdown - ",timeformat, end='\r')
        time.sleep(1)
        t -= 1
    logger.info(f'Completed countdown for {t1} seconds')



def confBgp(dev,conf_dict): 
    """   
    bgp:
    ibgp:
        as_number : 65535
        fx301:
        router_id : '1.1.1.11'
        neigh_list : ['1.1.1.101']
        fx302:
    """ 
    as_number = conf_dict['bgp']['ibgp']['as_number']
    router_id = conf_dict['bgp']['ibgp'][dev.name]['router_id']
    neigh_list = conf_dict['bgp']['ibgp'][dev.name]['neigh_list']


    bgp = Bgp(bgp_id=as_number)
    af_name = 'l2vpn evpn'
    vrf = Vrf('default')
    bgp.device_attr[dev].vrf_attr[vrf].address_family_attr[af_name].af_advertise_pip = True
    neighbor_id = '10.0.0.1'
    for neighbor_id in neigh_list:
        bgp.device_attr[dev].vrf_attr[vrf].neighbor_attr[neighbor_id].nbr_remote_as = as_number
        bgp.device_attr[dev].vrf_attr[vrf].neighbor_attr[neighbor_id].nbr_update_source = 'loopback0'
        bgp.device_attr[dev].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name].nbr_af_send_community = 'both'

    if 'spine' in dev.name:
        bgp1.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name].nbr_af_route_reflector_client = True

    dev.add_feature(bgp)
    cfgs = bgp.build_config(apply=False)
    ##import pdb;pdb.set_trace()
    
    #bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].\
    #                nbr_peer_type = Bgp.NBR_PEER_TYPE.fabric_border_leaf
    # bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name]. \
    #        nbr_af_rewrite_evpn_rt_asn = True
    #    bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id].address_family_attr[af_name].\
    #        nbr_af_disable_peer_as_check = True

    # Defining attributes
    af_name = 'ipv4 mvpn'
    vrf = Vrf('default')


def accessSWSviConf(uut,mac):
    cfg =\
    """
    feature interface-vlan
    no interface vlan 1005
    interface vlan 1005
    no shut
    sleep 2
    mac-address {mac}
    ip address dhcp

    """
    uut.configure(cfg.format(mac=mac))



def find_svi_ip(uut,svi):
    cmd = uut.execute("show int vlan {vlan} | json-pretty".format(vlan=svi))
    if not "svi_ip_addr" in str(cmd):
        log.info('svi_ip_addr found,Test failed')
        return 0
                
    else: 
        test1=json.loads(cmd)   
        ip = test1["TABLE_interface"]["ROW_interface"]["svi_ip_addr"]
        return ip 

def findLoopIp(uut,loop_id):
    cmd = uut.execute(f"show inter loop {loop_id} | json-pretty")
    if not "eth_ip_addr" in str(cmd):
        log.info('eth_ip_addr found,Test failed')
        return 0
                
    else: 
        test1=json.loads(cmd)   
        ip = test1["TABLE_interface"]["ROW_interface"]["eth_ip_addr"]
        return ip 

def sviPing(uut1,uut2):
    ip1 = find_svi_ip(uut1,'1005')
    if not ip1:
        return 0
    ip2 = find_svi_ip(uut2,'1005')
    if not ip2:
        return 0
    

def find_loop_ip(uut,loop):
    cmd = uut.execute("show int loopb {loop} | json-pretty".format(loop=loop))
    if not "eth_ip_addr" in str(cmd):
        log.info('svi_ip_addr found,Test failed')
        return 0
                
    else: 
        test1=json.loads(cmd)   
        ip = test1["TABLE_interface"]["ROW_interface"]["eth_ip_addr"]
        return ip        

def enableV6forVxlan(uut):
    #add ipv4 address
    #loop
    #svi
    #L3
    # int vl 1005
    # ipv6 address 2001::1/64

    # interface Vlan100
    # ipv6 address use-link-local-only # the same purpose as IP FORWARD
    # vrf context RED 
    # address-family ipv6 unicast
    # route-target both auto
    # route-target both auto evpn

    # router bgp 65000
    # vrf RED
    # address-family ipv6 unicast
    # advertise l2vpn evpn
    # vpc domain 1
    # ipv6 nd synchronize
    #2002:1:1:1:1:100:405:1
    cfg = \
    """
    """
    op1 = uut.execute("show ip inter brief vrf all  | inc Vla")
    for line in op1.splitlines():
        if 'Vlan' in line:
            if not 'forward-enabled' in line:
                vlan = line.split()[0]
                IP = line.split()[1]
                op2 = uut.execute(f"show run interface {vlan}")
                cfg3 = \
                f"""
                interface {vlan}
                """
                for line in op2.splitlines():
                    if 'ipv6 address' in line:
                        cfg3+= f'no {line} \n'
                uut.configure(cfg3) 
                ipv6_add = IPv6Address('2002:1:1:1:1::' + IP).compressed
                cfg += f"interface {vlan} ; ipv6 address {ipv6_add}/112 \n"
            else:
                vlan = line.split()[0]
                cfg += f"interface {vlan} ; ipv6 address use-link-local-only \n"

    op1 = uut.execute("show vrf")
    for line in op1.splitlines():
        if 'vxlan' in line:
            vrf = line.split()[0]
            cfg += f"vrf context {vrf} \n"
            cfg += f"address-family ipv6 unicast \n"
            cfg += f"route-target both auto\n"
            cfg += f"route-target both auto evpn \n"
            cfg += f"router bgp 65001 \n" 
            cfg += f"vrf  {vrf} \n"  
            cfg += f"address-family ipv6 unicast \n"
            cfg += f"advertise l2vpn evpn \n"  

    op1 = uut.execute("show feature | inc vpcf") 
    if 'enabled' in op1:
        cfg += f"vpc domain 1 \n"
        cfg += f"ipv6 nd synchronize\n"
 
    uut.configure(cfg)

def bpduFilter(uut,port):
    uut.configure(f'interface {port} ; spanning-tree bpdufilter enable \n')
 
def enableV6forVxlan2(uut):
    #add ipv4 address
    #loop
    #svi
    #L3
    # int vl 1005
    # ipv6 address 2001::1/64

    # interface Vlan100
    # ipv6 address use-link-local-only # the same purpose as IP FORWARD
    # vrf context RED 
    # address-family ipv6 unicast
    # route-target both auto
    # route-target both auto evpn

    # router bgp 65000
    # vrf RED
    # address-family ipv6 unicast
    # advertise l2vpn evpn
    # vpc domain 1
    # ipv6 nd synchronize
    #2002:1:1:1:1:100:405:1

    vlan_list1 = ['1001','1002','1003','1004','1005','1006','1007','1008','1009','1010']
    vlan_list2 = ['101','102','103','104','105','106','107','108','109','110']
    vrf_list = ['vxlan-900101','vxlan-900102','vxlan-900103','vxlan-900104','vxlan-900102']
    cfg = \
    f"""
    """
    for vlan in vlan_list1:
        IP = find_svi_ip(uut,vlan)        
        ipv6_add = IPv6Address('2002:1:1:1:1::' + IP).compressed
        cfg += f"interface vlan {vlan} ; ipv6 address {ipv6_add}/112 \n"


    for vlan in vlan_list2:      
        cfg += f"interface vlan {vlan} ; ipv6 address use-link-local-only \n"


 

    for vrf in vrf_list:   
        cfg += f"vrf context {vrf} \n"
        cfg += f"address-family ipv6 unicast \n"
        cfg += f"route-target both auto\n"
        cfg += f"route-target both auto evpn \n"
        cfg += f"router bgp 65001 \n" 
        cfg += f"vrf  {vrf} \n"  
        cfg += f"address-family ipv6 unicast \n"
        cfg += f"advertise l2vpn evpn \n"  

    op1 = uut.execute("show feature | inc vpcf") 
    if 'enabled' in op1:
        cfg += f"vpc domain 1 \n"
        cfg += f"ipv6 nd synchronize\n"
 
    uut.configure(cfg)



def dhcpCleanup(uut):
    op = uut.execute("sh run | inc 'ip source bindin'")
    for line in op.splitlines():
        if 'binding' in line:
            uut.configure(f"no {line}")
    uut.configure("clear ip dhcp snooping binding")


def snoop(uut):
    cfg = \
    """
    conf t
    
    hardware access-list tcam region ing-racl 256
    hardware access-list tcam region egr-racl 256
    hardware access-list tcam region ing-sup 768

    feature dhcp
    ip dhcp snooping vlan 1001 evpn

    copy run start
    y
    reload
    y

    """
def spineBgpConf(spine):
    #####
    cfg =\
        """
        router bgp 65535
        router-id 1.1.1.102

        template peer leaf_nodes
        bfd
        update-source loopback1
        address-family l2vpn evpn
        send-community both
        route-reflector-client
        neighbor 1.1.1.12 remote-as 65535
        inherit peer leaf_nodes
        neighbor 1.1.1.22 remote-as 65535
        inherit peer leaf_nodes
        neighbor 1.1.1.32 remote-as 65535
        inherit peer leaf_nodes
        neighbor 1.1.1.42 remote-as 65535
        inherit peer leaf_nodes
        neighbor 1.1.1.52 remote-as 65535
        inherit peer leaf_nodes
        """
    spine.configure(cfg)





def esgConfAdd(uut,conf_dict): 
    ip_list = conf_dict['esg'][uut.name]['ipv4_address']
    esg_start = conf_dict['esg'][uut.name]['esg_start']
    scale = conf_dict['traffic']['scale']
    cfg = \
    """

    """

    tag_list = []

    if len(ip_list) == 2:
        #for in int range(len(ip_list)):       
        start_ip1 =  ip_list[0]
        start_ip2 =  ip_list[1] 
        for i in range(scale):
            SG = str(esg_start)
            cfg += f'security-group  {SG}  name SG{SG} \n'
            cfg += f'match host vrf vxlan-900101 ipv4 {start_ip1}/32   \n'
            cfg += f'match host vrf vxlan-900101 ipv4 {start_ip2}/32   \n'
            esg_start = esg_start+1
            tag_list.append(SG)
            start_ip1 = str(ip_address(start_ip1)+1)
            start_ip2 = str(ip_address(start_ip2)+1)
    else:
        start_ip =  ip_list[0]
        for i in range(scale):
            SG = str(esg_start)
            cfg += f'security-group  {SG}  name SG{SG} \n'            
            cfg += f'match host vrf vxlan-900101 ipv4 {start_ip}/32   \n'
            esg_start = esg_start+1
            tag_list.append(SG)
            start_ip = str(ip_address(start_ip)+1)

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    

    return tag_list   


def esgConfRemove(uut): 
    op1 = uut.execute("show running-config security-group")   
    cfg = \
    """

    """
    tag_list = []
    for line in op1.splitlines():
        if not 'feature' in line:
            if 'security-group' in line:
                if not 'Command' in line:
                    cfg += f'no {line}  \n'   
        
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())      
    countdown(5)   


def addBgpPip(uut): 

    cfg = \
    """
    int nve 1
    advertise virtual-rmac
    router bgp 65001
    address-family l2 evp
    advertise-pip    
    """ 

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())      
    countdown(5)   





def esgclassPolicyConf(uut,start_ip,group):
    
    cfg = \
        """
        class-map type security match-any ESG1
        match ipv4
        policy-map type security ESGP
        class ESG1
            deny
            log
        """
    for i in range(scale):
        SG = string(group)
        cfg += f'security-group  {SG}  name SG{SG} \n'
        cfg += f'match host vrf vxlan-900101 ipv4 4.5.0.{start_ip}/32   \n'
        group = group+1
    
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())     
    countdown(10)

 


def checkArpTable(uut,ip_start,vrf):
    if not ip_start in uut.execute(f"show ip arp vrf {vrf}"):
        log.info(f"IP address {ip_start} not found in {uut.name} ARP Table")
        return 0
    else:
        return 1

def vni2kvrf500(uut,conf_dict):
    uut.configure("no interface nve 1")

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']
    l2vlan_per_vrf = 4
    l3_vlan_scale = 500
    mcast_group_start = '239.1.1.1'

    cfg = \
        """
        """

    cfg += f'interface nve1\n'
    cfg += f'no shutd\n'
    cfg += f'source-interface loopback0\n'
    cfg += f'host-reachability protocol bgp\n'

    for i in range(l3_vlan_scale):
        cfg += f'member vni {l3_vni_start} associate-vrf\n'
        l3_vni_start = l3_vni_start+1

    uut.configure(uut)

    cfg =\
    """
    """


    cfg += f'member vni {l2_vni_start}\n'
    cfg += f' ingress-replication protocol bgp\n'
    # Danish


    for i in range(l3_vlan_scale):
        cfg += f'member vni {l2_vni_start+1}-{l2_vni_start+l2vlan_per_vrf}\n'
        cfg += f'mcast-group {mcast_group_start}\n'
        mcast_group_start = ip_address(mcast_group_start)+1
        l2_vni_start = l2_vni_start+l2vlan_per_vrf
    uut.configure(uut)
            
def vxlanRouteAdd(uut,conf_dict):
    cmd = uut.execute("sh bgp all summary | json-pretty ")
    test1=json.loads(cmd)   
    as_number = test1["TABLE_vrf"]["ROW_vrf"]["vrf-local-as"]
    interface = conf_dict['vxlan_route'][uut.name]['interface']
    ip_address = conf_dict['vxlan_route'][uut.name]['ip_address']
    vrf = conf_dict['vxlan_route'][uut.name]['vrf']

    cfg = \
        """
        """
    cfg += f'interface {interface}\n'
    cfg += f'vrf member {vrf}\n'
    cfg += f'ip address {ip_address}\n'
    cfg += f'no shut\n'
    cfg += f'router bgp {as_number}\n'
    cfg += f'vrf {vrf}\n'
    cfg += f'address-family ipv4 unicast\n'
    cfg += f'network {ip_address}\n'
 
    uut.configure(cfg,timeout=300) 

def vxlanVrfRouteleak(uut):
    cfg = \
    """
    vrf context vxlan-900101  
    address-family ipv4 unicast
        no route-target both auto
        no route-target both auto mvpn
        no route-target both auto evpn
        route-target import 100:100
        route-target export 100:200
        route-target import 100:100 evpn
        route-target export 100:200 evpn 
    address-family ipv6 unicast
        no route-target both auto
        no route-target both auto evpn
        route-target import 100:100
        route-target export 100:200
        route-target import 100:100 evpn
        route-target export 100:200 evpn 

    vrf context vxlan-900102  
    address-family ipv4 unicast
        no route-target both auto
        no route-target both auto mvpn
        no route-target both auto evpn
        route-target import 100:200 
        route-target import 100:200  evpn
        route-target export 100:100
        route-target export 100:100 evpn
    address-family ipv6 unicast
        no route-target both auto
        no route-target both auto evpn
        route-target import 100:200 
        route-target import 100:200  evpn
        route-target export 100:100
        route-target export 100:100 evpn
    """
    uut.configure(cfg,timeout=300) 


def configVxlanLeaf(uut,conf_dict):
    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vlan_scale = conf_dict['vxlan']['l2_vlan_scale']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vlan_scale = conf_dict['vxlan']['l3_vlan_scale']
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']
    #l3_vlan_scale = conf_dict['vxlan']['l3vlan_scale']
    #l3vn_seg_start = conf_dict['vxlan']['l3vn_seg_start']
    ipaddress = conf_dict['vxlan']['ip_address']
    ipv6address = conf_dict['vxlan']['ipv6_address']
 
    mcast_group_start = conf_dict['vxlan']['mcast_group_start']
    #range = l2vlan_per_vrf
    uut.configure('no vlan 100-1200')
    uut.configure('no interface nve 1')
    l2vlan_per_vrf = conf_dict['vxlan']['l2vlan_per_vrf']

    cfg = \
        """
        feature interface-vlan
        feature lacp
        feature bfd
        feature nv overlay
        nv overlay evpn        
        feature vn-segment-vlan-based
        """

    l2_vlan = l2_vlan_start
    l2_vni = l2_vni_start
    if 'N9K' in uut.execute("show module"):
        cfg += f'feature fabric forwarding\n'

    for i in range(l2_vlan_scale):        
        cfg += f'vlan {l2_vlan}\n'
        cfg += f'vn-seg {l2_vni}\n'   
        cfg += f'sleep 1\n'   
        l2_vni = l2_vni+1 
        l2_vlan = l2_vlan+1

    uut.configure(cfg,timeout=300)

    cfg = \
        """
        """

    l3_vlan = l3_vlan_start
    l3_vni = l3_vni_start

    for i in range(l3_vlan_scale):
        cfg += f'vlan {l3_vlan}\n'
        cfg += f'vn-seg {l3_vni}\n' 
        cfg += f'sleep 1\n'  
        l3_vlan = l3_vlan+1  
        l3_vni = l3_vni+1 
 
    uut.configure(cfg,timeout=300)
 
    cfg = \
        """
        """

    l3_vni = l3_vni_start
    l3_vlan = l3_vlan_start

    vrf_list = []
    for i in range(l3_vlan_scale):
        vrf = 'vxlan-'+str(l3_vni)
        vrf_list.append(vrf)
        cfg += f'vrf context {vrf}\n'
        cfg += f'vni {l3_vni}\n'
        cfg += f'rd auto\n'
        cfg += f'address-family ipv4 unicast\n'
        cfg += f'route-target both auto\n'
        cfg += f'route-target both auto evpn\n'
        cfg += f'address-family ipv6 unicast\n'
        cfg += f'route-target both auto\n'
        cfg += f'route-target both auto evpn\n'
        cfg += f'interface Vlan {l3_vlan}\n'
        cfg += f'no shutdown\n'
        cfg += f'vrf member {vrf}\n'
        cfg += f'ip forward\n'
        cfg += f'sleep 1\n'  
        l3_vni = l3_vni+1  
        l3_vlan = l3_vlan+1 

    uut.configure(cfg,timeout=300)

    cfg = \
        """
        """
        
    l2_vlan = l2_vlan_start
    l2_vni = l2_vni_start
    l3_vlan = l3_vlan_start
    l3_vni = l3_vni_start

    vrf_vlan_dict = {}

    for i in range(l3_vlan_scale):
        vrf = 'vxlan-'+str(l3_vni)
        vlan_list = []
        for j in range(l2vlan_per_vrf): 
            #vlan_list.append(l2_vlan)
            #l2_vlan = l2_vlan+1
            #vrf_vlan_dict[vrf] = vlan_list
            cfg += f'no interface Vlan {l2_vlan}\n'
            cfg += f'interface Vlan {l2_vlan}\n'
            cfg += f'no shutdown\n'
            cfg += f'vrf member {vrf}\n'
            cfg += f'ip address {ipaddress}/16\n'
            #cfg += f'ipv6 address  {ipv6address}/112\n'
            cfg += f'fabric forwarding mode anycast-gateway\n'
            cfg += f'sleep 1\n'  
            ipaddress = ip_address(ipaddress)+65536
            ipv6address = ip_address(ipv6address)+65536
            l2_vlan = l2_vlan+1
        l3_vni = l3_vni+1
        #l2_vlan = l2_vlan+l2vlan_per_vrf

    uut.configure(cfg,timeout=300)


    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']


    cfg = \
        """
        """
    cfg += f'no interface nve1\n'
    cfg += f'interface nve1\n'
    cfg += f'no shutd\n'
    cfg += f'source-interface loopback0\n'
    cfg += f'host-reachability protocol bgp\n'

    for i in range(l3_vlan_scale):
        cfg += f'member vni {l3_vni_start} associate-vrf\n'
        cfg += f'sleep 1\n'  
        l3_vni_start = l3_vni_start+1

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']
    l2vlan_per_vrf = conf_dict['vxlan']['l2vlan_per_vrf']


    cfg += f'member vni {l2_vni_start}\n'
    cfg += f' ingress-replication protocol bgp\n'
    # Danish
    l2_vni_start = l2_vni_start +  1
    for i in range(l3_vlan_scale):
        cfg += f'member vni {l2_vni_start}-{l2_vni_start+l2vlan_per_vrf}\n'
        cfg += f'mcast-group {mcast_group_start}\n'
        cfg += f'sleep 1\n'  
        mcast_group_start = ip_address(mcast_group_start)+1
        l2_vni_start = l2_vni_start+l2vlan_per_vrf+1

    uut.configure(cfg,timeout=300)

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']

    cmd = uut.execute("sh bgp all summary | json-pretty ")
    test1=json.loads(cmd)   
    as_number = test1["TABLE_vrf"]["ROW_vrf"]["vrf-local-as"]
 
    cfg = \
        """
        """
    cfg += f'router bgp {as_number}\n'

    for i in range(l3_vlan_scale):
        vrf = 'vxlan-'+str(l3_vni_start)
        cfg += f'vrf {vrf}\n'
        cfg += f'address-family ipv4 unicast\n'
        cfg += f'advertise l2vpn evpn\n'
        cfg += f'sleep 1\n'  
        l3_vni_start = l3_vni_start+1


    uut.configure(cfg,timeout=300)

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']

    '''
    cfg = \
        """
        """

    cfg += f'evpn\n'
    for i in range(l2_vlan_scale):
        cfg += f' vni {l2_vni_start} l2\n'
        cfg += f' rd auto\n'  
        cfg += f'route-target import auto\n'  
        cfg += f'route-target export auto\n'  
    
    uut.configure(cfg,timeout=300)
    '''
 
    cfg = \
        """
        evpn
        """
    l2_vni = l2_vni_start
    for i in range(l2_vlan_scale):        
        cfg += f'vni {l2_vni} l2\n'   
        cfg += f'rd auto\n' 
        cfg += f'route-target import auto\n' 
        cfg += f'route-target export auto\n' 
        cfg += f'sleep 1\n'  
        l2_vni = l2_vni+1 

    uut.configure(cfg,timeout=300)

def leafConfig(leaf):

    op = leaf.execute("sh run int lo0")

    cfg = \
        """
        router bgp 65535
        neighbor 1.1.1.102 remote-as 65535
            bfd
            update-source loopback1
            address-family l2vpn evpn
            send-community both
            router bgp 65535
            address-family ipv4 unicast

        """
    for line in op.splitlines():
        if 'address' in line:
            network = line.split()[2]
            #cfg += f"network {network} \n"
            pass


    leaf.configure(cfg)



def dciebgpConfigure(uut,conf_dict):
    #import pdb;pdb.set_trace()
    router_id = conf_dict['bgp']['ebgp'][uut.name]['router_id']
    as_number = conf_dict['bgp']['ebgp'][uut.name]['as_number']
    neigh_list = conf_dict['bgp']['ebgp'][uut.name]['neigh_list'].keys()
 
    cfg = \
        """
        ip prefix-list redistribute-direct-underlay seq 5 permit 0.0.0.0/0 le 32
        route-map redistribute-direct-underlay permit 10
        match ip address prefix-list redistribute-direct-underlay 
        """
    cfg+= f"router bgp {as_number}\n"
    cfg+= f"router-id {router_id}\n"
    cfg+= "address-family ipv4 unicast\n"
    cfg+= "redistribute direct route-map redistribute-direct-underlay\n"

    for neighbor in neigh_list:
        remote_as = conf_dict['bgp']['ebgp'][uut.name]['neigh_list'][neighbor]['remote_as']
        update_source = conf_dict['bgp']['ebgp'][uut.name]['neigh_list'][neighbor]['update_source']
        cfg+= f"neighbor {neighbor} remote-as {remote_as}\n"
        cfg+= "bfd\n"
        cfg+= f"update-source {update_source}\n"
        cfg+= "address-family ipv4 unicast\n"

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    


def dcievpnbgpConfigure(uut,conf_dict):
    #import pdb;pdb.set_trace()
    #router_id = conf_dict['bgp']['ebgp'][uut.name]['router_id']
    as_number = conf_dict['bgp']['ebgpl2vpn'][uut.name]['as_number']
    neigh_list = conf_dict['bgp']['ebgpl2vpn'][uut.name]['neigh_list'].keys()
 
    cfg = \
        """
        feature bgp
        route-map unchanged permit 10
        set ip next-hop unchanged
        """
    cfg+= f"router bgp {as_number}\n"
    cfg+= "address-family l2vpn evpn\n"
    cfg+= "retain route-target all\n"

    for neighbor in neigh_list:
        remote_as = conf_dict['bgp']['ebgpl2vpn'][uut.name]['neigh_list'][neighbor]['remote_as']
        update_source = conf_dict['bgp']['ebgpl2vpn'][uut.name]['neigh_list'][neighbor]['update_source']
        cfg+= f"neighbor {neighbor} remote-as {remote_as}\n"
        cfg+= f"update-source {update_source}\n"
        cfg+= "ebgp-multihop 255\n"
        cfg+= "address-family l2vpn evpn\n"
        cfg+= "route-map unchanged out\n"        
        cfg+= "ebgp-multihop 255\n"
        if 'bgw' in uut.name:
            cfg+= "peer-type fabric-external\n"
        cfg+= "address-family l2vpn evpn\n"
        cfg+= "send-community\n"
        cfg+= "send-community extended\n"
        cfg+= "rewrite-evpn-rt-asn\n"        
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    



def bgpmvpnConfigure(uut,conf_dict):
    #import pdb;pdb.set_trace()
    #router_id = conf_dict['bgp']['ebgp'][uut.name]['router_id']
    if uut.name in conf_dict['bgp']['mvpn'].keys():
        if not str(31) in uut.name:
            as_number = conf_dict['bgp']['mvpn'][uut.name]['as_number']
            neigh_list = conf_dict['bgp']['mvpn'][uut.name]['neigh_list'].keys()    
            #import pdb;pdb.set_trace()   
            cfg = \
                """
                router bgp {as_number}
                address-family ipv4 mvpn
                maximum-paths 32
                retain route-target all
                """
            for neighbor in neigh_list:
                remote_as = conf_dict['bgp']['mvpn'][uut.name]['neigh_list'][neighbor]['remote_as']
                cfg+= f"neighbor {neighbor} remote-as {remote_as}\n"
                cfg+= "address-family ipv4 mvpn\n"
                cfg+= "send-community\n"
                cfg+= "send-community extended\n"
                if 'spine' in uut.name:
                    cfg+= "route-reflector-client \n"
                elif 'fx001' in uut.name:
                    cfg+= "route-reflector-client \n"
                elif 'fx002' in uut.name:
                    cfg+= "route-reflector-client \n"
            
            uut.configure(cfg.format(as_number=as_number),timeout=3000)


def bgwmultisiteconfig(uut,conf_dict):
    as_number = conf_dict['multisite'][uut.name]['as_number']
    #multisite_loop = conf_dict['multisite'][uut.name]['multisite_loop']
    dci_intf_list = []
    #conf_dict['multisite'][uut.name]['dci_intf_list']
    fabric_intf_list = []
    #conf_dict['multisite'][uut.name]['fabric_intf_list']

    op1 = uut.execute("show ip ospf nei")
    for line in op1.splitlines():
        if 'FULL' in line:
            intf = line.split()[-1]
            fabric_intf_list.append(intf)

    op2 = uut.execute("show ip interface brief")
    for line in op2.splitlines():
        if '44.1' in line:
            intf = line.split()[0]
            dci_intf_list.append(intf)

    cfg = \
        """
        """

    cfg+= f"evpn multisite border-gateway {as_number}\n"
    cfg+= f"delay-restore time 30 \n"

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    
 
    cfg = \
        """
        interface nve1
        multisite border-gateway interface loopback88
        member vni 201002-201010
            multisite ingress-replication
        member vni 201011-201019
            multisite ingress-replication
        member vni 900101 associate-vrf
        member vni 900102 associate-vrf
        """
    for intf in dci_intf_list:
        cfg+= f"interface {intf} \n"
        cfg+= f"evpn multisite dci-tracking\n"   
        cfg+= f"no shut\n"                  
    for intf in fabric_intf_list:
        cfg+= f"interface {intf} \n"
        cfg+= f"evpn multisite fabric-tracking\n"       
        cfg+= f"no shut\n"   

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())     



def dccdciebgpConfigure(uut,conf_dict):
    router_id = conf_dict['bgp']['ebgp'][uut.name]['router_id']
    as_number = conf_dict['bgp']['ebgp'][uut.name]['as_number']
    neigh_list = conf_dict['bgp']['ebgp'][uut.name]['neigh_list'].keys()
 
    cfg = \
        """
        ip prefix-list redistribute-direct-underlay seq 5 permit 0.0.0.0/0 le 32
        route-map redistribute-direct-underlay permit 10
        match ip address prefix-list redistribute-direct-underlay 
        """
    cfg+= f"router bgp {as_number}\n"
    cfg+= f"router-id {router_id}\n"
    cfg+= "address-family ipv4 unicast\n"
    cfg+= "redistribute direct route-map redistribute-direct-underlay\n"

    for neighbor in neigh_list:
        remote_as = conf_dict['bgp']['ibgp'][uut.name]['neigh_list'][neighbor]['remote_as']
        update_source = conf_dict['bgp']['ibgp'][uut.name]['neigh_list'][neighbor]['update_source']
        cfg+= f"neighbor {neighbor} remote-as {remote_as}\n"
        cfg+= "bfd\n"
        cfg+= f"update-source {update_source}\n"
        cfg+= "address-family ipv4 unicast\n"

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    


def ibgpConfigure(uut,conf_dict):
 
    router_id = conf_dict['bgp']['ibgp'][uut.name]['router_id']
    as_number = conf_dict['bgp']['ibgp'][uut.name]['as_number']
    neigh_list = conf_dict['bgp']['ibgp'][uut.name]['neigh_list']
 
    cfg = \
        """
        feature bgp
        """
    cfg+= f"no router bgp {as_number}\n"
    cfg+= f"router bgp {as_number}\n"
    cfg+= f"router-id {router_id}\n"
    for neighbor in neigh_list:
        cfg+= f"neighbor {neighbor} remote-as {as_number}\n"
        cfg+= "bfd\n"
        cfg+= "update-source loopback1\n"
        cfg+= "address-family l2vpn evpn\n"
        cfg+= "send-community both\n"
        if 'spine' in uut.name:
            cfg+= "route-reflector-client \n"
        elif 'fx001' in uut.name:
            cfg+= "route-reflector-client \n"
        elif 'fx002' in uut.name:
            cfg+= "route-reflector-client \n"

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    



def clearMac(uut):
    uut.execute('clear mac address-table dynamic ')


def pimConfig(uut,conf_dict):

    ssm_range = conf_dict['pim']['ssm_range']
    pim_rp_address = conf_dict['pim']['pim_rp_address']

    cfg =\
    f"""    
    ip pim rp-address {pim_rp_address} group-list 224.0.0.0/4
    ip pim ssm range {ssm_range}
    """
    op1= uut.execute("show ip interf brie")
    intf_list = []
        
    for line in op1.splitlines():
        if "Lo" in line:
            # or "Po" in line or 'Eth' in line:   
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"   
            uut.configure(cfg,timeout=300)

        elif "Po" in line:
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"   
            uut.configure(cfg,timeout=300)
        elif 'Eth' in line:       
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"               
            uut.configure(cfg,timeout=300)   


def pimConfigMs(uut,ssm_range,pim_rp_address):

    #ssm_range = conf_dict['pim']['ssm_range']
    #pim_rp_address = conf_dict['pim']['pim_rp_address']

    cfg =\
    f"""    
    ip pim rp-address {pim_rp_address} group-list 224.0.0.0/4
    ip pim ssm range {ssm_range}
    """
    op1= uut.execute("show ip interf brie")
    intf_list = []
        
    for line in op1.splitlines():
        if "Lo" in line:
            # or "Po" in line or 'Eth' in line:   
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"   
            uut.configure(cfg,timeout=300)

        elif "Po" in line:
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"   
            uut.configure(cfg,timeout=300)
        elif 'Eth' in line:       
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            cfg+= f"no shut\n"               
            uut.configure(cfg,timeout=300)   


def addSecGrpTemplate(uut):
    if not 'Applied System Routing Mode: Security-Groups Support' in uut.execute("show system routing mode"):
        uut.configure('system routing template-security-groups')
        uut.execute('copy run start')
        uut.reload()
        countdown(120)

def preSetupVxlan(uut):

    cfg = \
    """
    no feature ospf
    no feature bgp
    no feature nv overlay
    no feature vpc
    no feature lacp
    no feature pim
    no vlan 2-3000
    no feature dhcp
    no feature interface-vlan
    no feature vn-segment-vlan-based
    clear cores
    spanning-tree mode rapid-pvst
    cdp en
    """
    cfg2 = \
    """
    vlan 1001-1101
    no shut
    feature ospf
    feature bgp
    feature nv overlay
    feature lacp
    feature pim
    nv overlay evpn
    feature interface-vlan
    feature vn-segment-vlan-based
    fabric forwarding anycast-gateway-mac 0000.2222.3333
    feature bfd
    bfd interval 300 min_rx 300 multiplier 3
    bfd multihop interval 999 min_rx 999 multiplier 10
    ntp server 10.64.58.51 use-vrf management 
    ntp server 72.163.32.44 use-vrf management 
    system jumbomtu 9216
    spanning-tree mode rapid-pvst
    cdp en
    """
    uut.configure(cfg,timeout=300)
    time.sleep(10)
    uut.configure(cfg2,timeout=300)
    clearVrfConf(uut)
    cleararpConf(uut)
    clearIPConf(uut)
    unshutAllintf(uut)
 

def SwCleanupConfigs(uut):

    cfg = \
    """
    no feature ospf
    no feature bgp
    no feature vpc
    no feature lacp
    no feature pim
    no vlan 2-3000
    no feature dhcp
    no feature interface-vlan
    clear cores
        cdp en
    """
    cfg2 = \
    """
    vlan 1001-1101
    no shut
    feature lacp
    feature interface-vlan
    system jumbomtu 9216
    cdp en
    spanning-tree mode rapid-pvst
    """
    uut.configure(cfg,timeout=300)
    time.sleep(10)
    uut.configure(cfg2,timeout=300)
    clearVrfConf(uut)
    cleararpConf(uut)
    clearIPConf(uut)
    unshutAllintf(uut)
    swCleanup(uut)



def cleararpConf(uut):
    cfg3 = \
    """
    """
    for line in uut.execute('sh run | inc arp').splitlines():
        if 'inspection' in line:
            cfg3 +=f'no {line}'

    uut.configure(cfg3,timeout=300)   

def cleardhcpConf(uut):
    uut.configure('no feature dhcp',timeout=300)   
 
 
def clearVrfConf(uut):
    cfg3 = \
    """
    """
    for line in uut.execute('show vrf').splitlines():
        if 'vxlan' in line:
            vrf = line.split()[0]
            cfg3 +=f'no vrf context {vrf} \n'

    uut.configure(cfg3,timeout=300)        


def pimConfig(l3_device_list,conf_dict):
    ssm_range = conf_dict['pim']['site1']['ssm_range']
    pim_rp_address1 = conf_dict['pim']['site1']['pim_rp_address']

    ssm_range_1 = []
    rp_add1 = []

    for elem in  l3_device_list:
        ssm_range_1.append(ssm_range)
        rp_add1.append(pim_rp_address1)

    pcall(pimConfigMs, uut=tuple(l3_device_list),ssm_range=tuple(ssm_range_1),pim_rp_address=tuple(rp_add1)) 
 

def pimConfigSpine(uut,conf_dict):
    pim_rp_address1 = conf_dict['pim']['site1']['pim_rp_address']
    ip1 = conf_dict['interfaces']['fx001']['loopback']['loopback1']['ip_add']
    ip2 = conf_dict['interfaces']['fx002']['loopback']['loopback1']['ip_add']         

    cfg = \
    f"""
    ip pim anycast-rp {pim_rp_address1} {ip1}
    ip pim anycast-rp {pim_rp_address1} {ip2}
    """

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())    
 


def clearIPConf(uut):
    #import pdb;pdb.set_trace()
    op1= uut.execute("show interf brie")
    intf_list = []
    eth_intf_list = []
    cfg = \
        """
        """        
    for line in op1.splitlines():
        if "Lo" in line:
            intf = line.split()[0]
            intf_list.append(intf)
        elif "Po" in line:
            intf = line.split()[0]
            intf_list.append(intf)
        elif "Vlan" in line:
            intf = line.split()[0]
            intf_list.append(intf)
        elif 'Eth' in line:      
            if not 'XCVR' in line: 
                intf = line.split()[0]
                cfg1 = f" default interface {intf} "
                uut.configure(cfg1,timeout=300)
                cfg2 = f"interface {intf} ; no shut"
                uut.configure(cfg2,timeout=300)

    for intf in intf_list:
            cfg +=  f"no interface {intf} \n"

    uut.configure(cfg,timeout=300)        



def configureLoopInterface1(uut,conf_dict):
   for intf in conf_dict['interfaces'][uut.name]['loopback']:
        ip_add = conf_dict['interfaces'][uut.name]['loopback'][intf]['ip_add']
        description = conf_dict['interfaces'][uut.name]['loopback'][intf]['Description']
        prefix_length = conf_dict['interfaces'][uut.name]['loopback'][intf]['prefix_length']        
        #ipv6_address = conf_dict['interfaces'][uut.name]['loopback'][intf]['ipv6_address'] 

        Loopif = SubInterface(name=intf,device=uut)    
        Loopif.description = description
        Loopif.ipv4 = ip_add
        Loopif.ipv4.netprefix_length = prefix_length
        Loopif.shutdown = False
        #Loopif.ipv6 = ipv6_address
        #Loopif.ipv4_secondary = True
        #Loopif.ipv4 = IPv4Address('192.168.1.2')
        #ipv4b.prefix_length = '24'

        cfgs = Loopif.build_config(apply=False)

        if 'ip_add_secondary' in conf_dict['interfaces'][uut.name]['loopback'][intf]:
            ip_add_secondary = conf_dict['interfaces'][uut.name]['loopback'][intf]['ip_add_secondary']
            cfgs += f"\n ip address {ip_add_secondary} secondary\n "
            
        uut.configure(cfgs)


def configureLoopInterface(uut,conf_dict):
   for intf in conf_dict['interfaces'][uut.name]['loopback']:
        intf1 = Interface(name=intf, device=uut)
        ip_add = conf_dict['interfaces'][uut.name]['loopback'][intf]['ip_add']
        description = conf_dict['interfaces'][uut.name]['loopback'][intf]['Description']
        prefix_length = conf_dict['interfaces'][uut.name]['loopback'][intf]['prefix_length']      
        ipv4a = IPv4Addr(device=uut)
        ipv4a.ipv4 = IPv4Address(ip_add)
        ipv4a.prefix_length = prefix_length
        #ipv4a.redirect = False
        intf1.add_ipv4addr(ipv4a)
        intf1.shutdown = False
        # make intf2 as L3 interface
        #intf1.switchport_enable = False
        #cfgs = intf1.build_config(apply=False)
        
        cfgs = intf1.build_config(apply=True)

        if 'ip_add_secondary' in conf_dict['interfaces'][uut.name]['loopback'][intf]:
            ip_add_secondary = conf_dict['interfaces'][uut.name]['loopback'][intf]['ip_add_secondary']        
            ipv4b = IPv4Addr(device=uut)
            ipv4b.ipv4 = IPv4Address(ip_add_secondary)
            ipv4b.prefix_length = prefix_length
            ipv4b.ipv4_secondary = True
            #ipv4b.redirect = False
            intf1.add_ipv4addr(ipv4b)
        
        cfgs = intf1.build_config(apply=True)
        #uut.configure(cfgs)

def configureL3Interface(uut,conf_dict):

    for intf in conf_dict['interfaces'][uut.name]['layer3']:
        cfg = \
        """
        interface {intf}
        no switchport
        """
        uut.configure(cfg.format(intf=intf))

        ip_add = conf_dict['interfaces'][uut.name]['layer3'][intf]['ip_add']
        description = conf_dict['interfaces'][uut.name]['layer3'][intf]['Description']
        uut.configure(cfg.format(intf=intf))
        if 'loopback' in ip_add:
            intf1 = Interface(name=intf,device=uut)  
            intf1.description = description        
            intf1.unnumbered_intf_ref  = ip_add
            intf1.medium = 'p2p'
            intf1.shutdown = False    
            intf1.enabled = True
            intf1.switchport_enable = False
            intf1.mtu = 9126
            cfgs = intf1.build_config(apply=True)

        else:        
            intf1 = Interface(name=intf,device=uut)         
            prefix_length = conf_dict['interfaces'][uut.name]['layer3'][intf]['prefix_length']   
            #ipv6_address = conf_dict['interfaces'][uut.name]['layer3'][intf]['ipv6_address']         
            intf1.ipv4 = ip_add
            intf1.ipv4.netprefix_length = prefix_length
            cfg += f'ip address {ip_add}/{prefix_length}\n'
            cfg += 'mtu 9216\n'
            uut.configure(cfg.format(intf=intf))

        if 'port_channel' in intf: 
            intf1.channel_group_mode = 'active'
            intf_name = conf_dict['interfaces'][uut.name]['layer3'][intf]['name']            
            for member in conf_dict['interfaces'][uut.name]['layer3'][intf]['members']:
                intf2 = Interface(name=member,device=uut)
                intf1.add_member(intf2)
            cfgs = intf1.build_config(apply=True)


def configureL2Interface(uut,conf_dict): 
    ##import pdb;pdb.set_trace()
    #import pdb; pdb.set_trace()
    uut.configure("spanning-tree mode rapid-pvst")

    if 'layer2' in conf_dict['interfaces'][uut.name]:
        for intf in conf_dict['interfaces'][uut.name]['layer2']:   
            #import pdb;pdb.set_trace() 
            if 'Po' in intf:    
                log.info(f"Interface is {intf}")
                intf_name = conf_dict['interfaces'][uut.name]['layer2'][intf]['name'] 
                description = conf_dict['interfaces'][uut.name]['layer2'][intf]['Description']
                switchport_mode = conf_dict['interfaces'][uut.name]['layer2'][intf]['switchport_mode']
                switchport_vlan = conf_dict['interfaces'][uut.name]['layer2'][intf]['switchport_vlan']
                intf1 = Interface(name=intf_name,device=uut)    
                intf1.description = description
                intf1.switchport_mode = switchport_mode
                if 'access' in switchport_mode:
                    intf1.access_vlan = switchport_vlan
                elif 'trunk' in switchport_mode:
                    intf1.trunk_vlans = switchport_vlan
                intf1.shutdown = False
                intf1.channel_group_mode = 'active'
                intf1.enabled = True
                intf1.switchport_enable = True
 
                for member in conf_dict['interfaces'][uut.name]['layer2'][intf]['members']:
                    log.info(f"member is {member}") 
                    intf2 = Interface(name=member,device=uut)
                    intf1.add_member(intf2)

                # Build config
                
                cfgs = intf1.build_config(apply=False)
                
                cfgs2 = cfgs.replace("mode active","force mode active") 

                if 'vpc' in conf_dict['interfaces'][uut.name]['layer2'][intf]:
                    uut.configure('feature vpc')
                    vpc1 = conf_dict['interfaces'][uut.name]['layer2'][intf]['vpc']
                    cfgs2 += f"\ninterface  {intf_name}\n "
                    cfgs2 += f"\n vpc {vpc1}\n "
                countdown(5)    
                uut.configure(cfgs2,timeout=300)
                countdown(1)    
            elif 'Eth' in intf:  
                log.info(f"Interface is {intf}")
                intf_name = conf_dict['interfaces'][uut.name]['layer2'][intf]['name'] 
                description = conf_dict['interfaces'][uut.name]['layer2'][intf]['Description']
                switchport_mode = conf_dict['interfaces'][uut.name]['layer2'][intf]['switchport_mode']
                switchport_vlan = conf_dict['interfaces'][uut.name]['layer2'][intf]['switchport_vlan']
                intf1 = Interface(name=intf_name,device=uut)    
                intf1.switchport_enable = True
                intf1.shutdown = False
                intf1.enabled = True
                intf1.description = description
                intf1.switchport_mode = switchport_mode                
                if 'access' in switchport_mode:
                    intf1.access_vlan = switchport_vlan
                    intf1.switchport_mode = 'access'
                elif 'trunk' in switchport_mode:
                    intf1.trunk_vlans = switchport_vlan

                cfgs = str(intf1.build_config(apply=False))
                if 'access' in switchport_mode:
                    cfgs += f"\ninterface  {intf_name}\n "
                    cfgs += f"\n switchport access vlan {switchport_vlan}\n "

                elif 'trunk' in switchport_mode:
                    cfgs += f"\ninterface  {intf_name}\n "
                    cfgs += f"\n switchport trunk allowed vlan add {switchport_vlan}\n "                    
                countdown(7)    
                uut.configure(cfgs,timeout=300)  
                countdown(1)    
 
def intfUnshut(uut,intf):
    intf1 = Interface(name=intf,device=uut)
    intf1.shutdown = False
    cfg = intf1.build_config(apply=True)

def getEthIntfList(uut):
    intf_list = []
    for line in uut.execute("show interface brief | ex XCVR").splitlines():
        if not "VLAN" in line:
            if "Eth" in line:
                intf_list.append(line.split()[0])
    return(intf_list)  

def getOspfIntfList(uut):
    intf_list = []
    for line in uut.execute("show ip os neighbors").splitlines():
        if  "FULL" in line:
            if "Eth" in line:
                intf_list.append(line.split()[-1])
    return(intf_list)  

def unshutAllintf(uut):    
    intf_list1 = getEthIntfList(uut)
    for intf in intf_list1:
        intfUnshut(uut,intf)

def ospfIntfFlap(uut):
    intf_list = getOspfIntfList(uut)
    for intf in intf_list:
        intfUnshut(uut,intf)
        intfUnshut(uut,intf)

def coreInterfaceFlap(uut):
    log.info(banner("Starting L3InterfaceFlap "))
    for uut in [uut]:
        if 'router ospf' in uut.execute("show run | inc ospf"):
            cmd = uut.execute("show ip ospf neigh | json-pretty")
            op=json.loads(cmd)
            op11 = op["TABLE_ctx"]['ROW_ctx']
            if 'list' in str(type(op11)):
                op1 = op11[0]["TABLE_nbr"]['ROW_nbr']
                nbrcount = op11[0]['nbrcount']
                core_intf_list = []
                if int(nbrcount) == 1:
                    intf = op1[0]["intf"]
                    core_intf_list.append(intf)
                else:
                    for i in range(0,len(op1)):
                        intf = op1[i]["intf"]
                        core_intf_list.append(intf)
            else:
                op1 = op["TABLE_ctx"]['ROW_ctx']["TABLE_nbr"]['ROW_nbr']
                nbrcount = op["TABLE_ctx"]['ROW_ctx']['nbrcount']
                core_intf_list = []

                if int(nbrcount) == 1:
                    intf = op1["intf"]
                    core_intf_list.append(intf)
                else:
                    for i in range(0,len(op1)):
                        intf = op1[i]["intf"]
                        core_intf_list.append(intf)

        elif 'router isis' in uut.execute("show run | inc isis"):
            core_intf_list = []
            op = uut.execute('show isis adjacency')
            op1 = op.splitlines()
            for line in op1:
               if 'UP' in line:
                   intf = line.split()[-1] 
                   core_intf_list.append(intf)  

        for i in range(1,4):
            for intf in core_intf_list:
                cfg = \
                """
                interface {intf}
                shut
                """
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('L3InterfaceFlap failed @ 11')
                    return 0

            countdown(1)
            for intf in core_intf_list:
                cfg = \
                """
                interface {intf}
                no shut
                """
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('L3InterfaceFlap failed @ 12')
                    return 0
    log.info(banner("END L3InterfaceFlap "))
    return 1


def icmpPingTest(uut):
    ip1 = '100.1.1.100'
    ip2 = '100.1.1.11'
    try:
        op1 = uut.execute(f'ping {ip1}')
        if '100.00% packet loss' in op1:
            log.info(f'ping test failed for {uut}')
            return 0
        #op2 = uut.execute('ping {ip2}')
        #if '100.00% packet loss' in op2:

        #    log.info(f'ping test failed for {uut}')
        #    return 0
    except:
        log.info(f"PING FAILED for UUT {uut}")
        return 0 
    return 1
    

def vxlanAllReset(uut):
    log.info(banner("starting VxlanStReset"))

   # for uut in uut_list:
        #log.info(banner('remove add nve in VxlanStReset uut %r',uut))
    nve_conf = uut.execute('show run int nve 1 | be nve1')
    uut.configure(nve_conf)

    cfg_shut =  \
    """
    interface {intf}
    shut
    """
    cfg_no_shut =  \
    """
    interface {intf}
    no shut
    """

 
    op = uut.execute('show port-channel summary | incl Eth',timeout = 180)
    op1 = op.splitlines()
    po_list = []
    for line in op1:
        if line:
            if not 'Po1(SU)' in line:
                if 'Eth' in line:
                    if 'Po' in line:
                        po = line.split()[1].split('(')[0]
                        po_list.append(po)

    for intf in po_list+["nve1"]:
        uut.configure(cfg_shut.format(intf=intf),timeout = 180)

    countdown(60)

    op = uut.execute('show port-channel summary | incl Eth',timeout = 180)
    op1 = op.splitlines()
    po_list = []
    for line in op1:
        if line:
            if not 'Po1(SU)' in line:
                if 'Eth' in line:
                    if 'Po' in line:
                        po = line.split()[1].split('(')[0]
                        po_list.append(po)

    for intf in po_list+["nve1"]:
        uut.configure(cfg_no_shut.format(intf=intf),timeout = 180)


    coreInterfaceFlap(uut)

    intf_list = []
    for intf in [*uut.interfaces.keys()]:
        if 'Eth' in uut.interfaces[intf].intf:
            if 'bgw' in uut.interfaces[intf].alias:
                intf=uut.interfaces[intf].intf
                intf_list.append(intf)                 
            elif 'leaf' in uut.interfaces[intf].alias:
                intf=uut.interfaces[intf].intf
                intf_list.append(intf)    
    
    for intf in intf_list:
        cfg = \
        """
        interface {intf}
        shut
        sleep 1
        no shut
        """
        uut.configure(cfg.format(intf=intf))


    countdown(200)

    for feature in ['pim','bgp']:
        test1 = leafProtocolCheck(uut,[feature])
        if not test1:
            log.info('Feature %r neigborship on device %r Failed ',feature,str(uut))
            return 0

    log.info(banner("Passed VxlanStReset"))
    return 1



def leafProtocolCheck(uut,protocol_list):
    for proto in protocol_list:
        fail_list = []
        if 'isis' in proto:
            try:
               cmd = uut.execute("sh isis adjacency | incl N/A")
            except:
                log.info("ISIS ADJ check failed")
                return 0
            
            if 'Invalid' in str(cmd):
                log.info('Invalid ISIS neighbor found,Test failed for uut/neighbor %r',uut)
                return 0
                
            op = cmd.splitlines()
            for line in op:
                if line:
                    if not '  UP ' in line:
                        log.info('isis neighbor found,Test failed for uut/neighbor %r',uut)
                        fail_list.append('fail')
            
            if 'fail' in fail_list:
                log.info('isis neighbor test FAIL for uut/neighbor %r',uut)
                return 0
            else:
                log.info('isis neighbor test PASS for uut/neighbor %r',uut)
                return 1            

        elif 'vpc' in proto:
            op=uut.execute('show port-channel summary | incl Eth')
            op1=op.splitlines()
            for line in op1:
                if line:
                    if not "(P)" in line:
                        log.info('VPC Bringup Failed on device %r',str(uut))
                        uut.execute('show port-channel summary')
                        return 0
    
        elif 'ospf' in proto:
            try:
                cmd = uut.execute("show ip ospf neighbors | json-pretty")
            except:
                log.info("OSPF ADJ check failed")
                return 0            

            if not "addr" in str(cmd):
                log.info('No OSPF neighbor found,Test failed for uut/neighbor %r',uut)
                return 0
            elif 'Invalid' in str(cmd):
                log.info('Invalid OSPF neighbor found,Test failed for uut/neighbor %r',uut)
                return 0

            else:
                test1=json.loads(cmd)
                test11 = test1["TABLE_ctx"]["ROW_ctx"]
                if 'list' in str(type(test11)):
                    neig_list = test11[0]["TABLE_nbr"]["ROW_nbr"]
                    neig_count =  str(neig_list).count('addr')
                    if neig_count == 1:
                        if not 'FULL' in (neig_list)[0]['state']:
                            log.info('OSPF neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            if not 'FULL' in (neig_list)[i]['state']:
                                log.info('OSPF neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1

                else:
                    neig_list= test1["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"]
                    neig_count =  str(neig_list).count('addr')
                    if neig_count == 1:
                        if not 'FULL' in (neig_list)['state']:
                            log.info('OSPF neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            if not 'FULL' in (neig_list)[i]['state']:
                                log.info('OSPF neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1


        elif 'bgp' in proto:
            cmd = uut.execute(" show bgp l2 evpn summary | json-pretty |inc state")
            if not "state" in str(cmd):
                log.info('No BGP neighbor found,Test failed for uut/neighbor %r',uut)
                return 0
            '''
            else:
                test1=json.loads(cmd)
                test11 = test1["TABLE_vrf"]["ROW_vrf"]
                if 'list' in str(type(test11)):
                    neig_list= test11[0]["TABLE_af"]["ROW_af"][0]["TABLE_saf"][ "ROW_saf"][0]["TABLE_neighbor"]["ROW_neighbor"]
                    neig_count =  str(neig_list).count('neighborid')
                    if neig_count == 1:
                        if not 'Established' in (neig_list)[0]['state']:
                            log.info('BGP neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            if not 'Established' in (neig_list)[i]['state']:
                                log.info('BGP neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1

                else:
                    neig_list= test1["TABLE_vrf"]["ROW_vrf"]["TABLE_af"]["ROW_af"]["TABLE_saf"][ "ROW_saf"]["TABLE_neighbor"]["ROW_neighbor"]
                    neig_count =  str(neig_list).count('neighborid')
                    if neig_count == 1:
                        if not 'Established' in (neig_list)['state']:
                            log.info('BGP neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            if not 'Established' in (neig_list)[i]['state']:
                                log.info('BGP neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1
            '''

            op = cmd.splitlines()
            for line in op:
                if 'state' in line:
                    if not "Established" in line:
                        log.info("BGP neighbor check passed for uut %r",uut)
                        return 0
 
            log.info('BGP neighbor check passed for uut -------------- :')
            return 1

        elif 'pim' in proto:
            cmd = uut.execute("show ip pim neighbor | json-pretty ")
            if not "vrf" in str(cmd):
                if not "nbr-add" in str(cmd):
                    log.info('No PIM neighbor found,Test failed for uut/neighbor %r',uut)
                    return 0
                else:
                    return 1

            elif "vrf" in str(cmd):
                test1=json.loads(cmd)
                test11 = test1["TABLE_vrf"]["ROW_vrf"]
                if 'list' in str(type(test11)):
                    neig_list= test11[0]["TABLE_neighbor"]["ROW_neighbor"]
                    neig_count =  str(neig_list).count('nbr-addr')
                    if neig_count == 1:
                        uptime = (neig_list)[0]['uptime']
                        uptime = uptime.replace(":","")
                        uptime = uptime.replace("d","")
                        uptime = uptime.replace("h","")
                        uptime = uptime.replace("s","")
                        if not int(uptime) > 1:
                            log.info('PIM neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            uptime = (neig_list)[i]['uptime']
                            uptime = uptime.replace(":","")
                            uptime = uptime.replace("d","")
                            uptime = uptime.replace("h","")
                            uptime = uptime.replace("s","")
                            if not int(uptime) > 1:
                                log.info('PIM neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1

                else:
                    neig_list= test1["TABLE_vrf"]["ROW_vrf"]["TABLE_neighbor"]["ROW_neighbor"]
                    neig_count =  str(neig_list).count('nbr-addr')
                    if neig_count == 1:
                        uptime = (neig_list)['uptime']
                        uptime = uptime.replace(":","")
                        uptime = uptime.replace("d","")
                        uptime = uptime.replace("h","")
                        uptime = uptime.replace("s","")
                        if not int(uptime) > 1:
                            log.info('PIM neighbor check failed for uut/neighbor %r',uut)
                            return 0
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            uptime = (neig_list)[i]['uptime']
                            uptime = uptime.replace(":","")
                            uptime = uptime.replace("d","")
                            uptime = uptime.replace("h","")
                            uptime = uptime.replace("s","")
                            if not int(uptime) > 1:
                                log.info('PIM neighbor check failed for uut/neighbor %r',uut)
                                return 0
                            else:
                                return 1
            else:
                pass

            log.info('PIM Neighbor check passed for uut --------------')

        elif 'nve-peer' in proto:
            #if not 'UnicastBGP' in uut.execute('show nve peers ')
            cmd = uut.execute("show nve peers | json-pretty")
            if not "peer-state" in str(cmd):
                log.info('No NVE neighbor found,Test failed for uut/neighbor,11111')
                time.sleep(20)
                cmd = uut.execute("show nve peers | json-pretty")
                if not "peer-state" in str(cmd):
                    log.info('No NVE neighbor found,Test failed for uut/neighbor,2222')
                    time.sleep(20)
                    cmd = uut.execute("show nve peers | json-pretty")
                    if not "peer-state" in str(cmd):
                        log.info('No NVE neighbor found,Test failed for uut/neighbor,33333')
                        cmd = uut.execute("show nve peers")
                        return 0
            else:
                test1=json.loads(cmd)
                test11 = test1["TABLE_nve_peers"]["ROW_nve_peers"]
                if 'list' in str(type(test11)):
                    neig_list= test11
                    neig_count =  str(neig_list).count('peer-ip')
                    if neig_count == 1:
                        state = (neig_list)[0]['peer-state']
                        if not 'Up' in state:
                            log.info('NVE Peer check failed for uut/neighbor %r',uut)
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            state = (neig_list)[i]['peer-state']
                            if not 'Up' in state:
                                log.info('NVE Peer check failed for uut/neighbor %r',uut)
                            else:
                                log.info('NVE Peer check passed for uut --------------')
                                return 1


                else:
                    neig_list= test1["TABLE_nve_peers"]["ROW_nve_peers"]
                    neig_count =  str(neig_list).count('peer-ip')
                    if neig_count == 1:
                        state = (neig_list)['peer-state']
                        if not 'Up' in state:
                            log.info('NVE Peer check failed for uut/neighbor %r',uut)
                        else:
                            return 1

                    elif neig_count > 1:
                        for i in range(0,neig_count-1):
                            state = (neig_list)[i]['peer-state']
                            if not 'Up' in state:
                                log.info('NVE Peer check failed for uut/neighbor %r',uut)
                            else:
                                log.info('NVE Peer check passed for uut --------------')
                                return 1

        elif 'nve-vni' in proto:
            cmd = uut.execute("show nve vni")
            #test1=json.loads(uut.execute(cmd))
            if not "nve1" in str(cmd):
                log.info('No NVE VNI found,Test failed for uut/neighbor %r',uut)
                return 0

            if "Down" in str(cmd):
                log.info(' NVE VNI Down,Test failed for uut/neighbor %r',uut)
                return 0

            else:
                return 1

    log.info('Protocol check passed for uut -------------- :')

def po11Flap(uut,timegap):
    cfg1 = \
    f"""
    interf Po 11
    shut
    """

    cfg2 = \
    f"""
    interf Po 11
    no shut
    """
    uut.configure(cfg1)
    countdown(timegap)
    uut.configure(cfg2)    




def addVpcConfig(uut,conf_dict):
    if 'vpc' in conf_dict['interfaces'][uut.name]:  
        #import pdb;pdb.set_trace()  
        domain_id = conf_dict['interfaces'][uut.name]['vpc']['domain_id']
        keepalive_dst_ip = conf_dict['interfaces'][uut.name]['vpc']['keepalive_dst_ip']
        keepalive_src_ip =conf_dict['interfaces'][uut.name]['vpc']['keepalive_src_ip']
    
        vpc = Vpc()
        dev = uut
        dev.add_feature(vpc)
        maxDiff = None

        vpc.enabled = True
        vpc.device_attr[dev].enabled = True
        vpc.device_attr[dev].domain_attr[domain_id]
        vpc.device_attr[dev].domain_attr[domain_id].keepalive_dst_ip = keepalive_dst_ip
        vpc.device_attr[dev].domain_attr[domain_id].keepalive_src_ip = keepalive_src_ip
        vpc.device_attr[dev].domain_attr[domain_id].keepalive_vrf = 'management'

        cfgs = vpc.build_config(apply=True)



def addOspfConfig(uut,conf_dict):
    dev1 = uut
    router_id = conf_dict['igp']['ospf'][uut.name]['router_id']   
    intf1_list = conf_dict['igp']['ospf'][uut.name]['intf1_list']   
    #router_id = find_loop_ip(uut,'0')
    # Create OSPF object
    ospf1 = Ospf()
    ospf1.device_attr[dev1].enabled = True
    vrf0 = Vrf('default')

    # Add OSPF configuration to vrf default
    ospf1.device_attr[dev1].vrf_attr[vrf0].instance = 'UNDERLAY'
    ospf1.device_attr[dev1].vrf_attr[vrf0].enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].router_id = router_id
    #ospf1.device_attr[dev1].vrf_attr[vrf0].bfd_enable = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes = True
    ospf1.device_attr[dev1].vrf_attr[vrf0].log_adjacency_changes_detail = True
    # Add area configuration to VRF default
    ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].area_te_enable = True
    for intf1 in intf1_list:
        #intf1 = Interface(name=intf,device=dev1)
        if 'loop' in intf1:
            ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
        else:
            # Add interface configuration to VRF default
            ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_admin_control = True
            ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_type = 'point-to-point'
            #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_enable = True
            #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_interval = 999
            #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_min_interval = 999
            #ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_bfd_multiplier = 7
            ospf1.device_attr[dev1].vrf_attr[vrf0].area_attr['0'].interface_attr[intf1].if_mtu_ignore = True

    # Add OSPF to the device
    dev1.add_feature(ospf1)
    
    # Build config
    cfgs = ospf1.build_config(apply=True)

def addBgpConfig(uut,conf_dict):
    dev1 = uut
    router_id = conf_dict['bgp'][uut.name]['router_id']   
    neigh_list = conf_dict['bgp'][uut.name]['neigh_list']   

    bgp = Bgp(bgp_id=100)
    af_name = 'l2vpn evpn'
    af_name1 = 'ipv4 unicast'
    vrf = Vrf('default')
    bgp.device_attr[dev1].vrf_attr[vrf].address_family_attr[af_name].af_advertise_pip = True
    bgp.device_attr[dev1]
    dev1.add_feature(bgp)
    cfgs = bgp.build_config(apply=False)
    neighbor_id = '10.0.0.1'
    bgp2.device_attr[dev1].vrf_attr[vrf].neighbor_attr[neighbor_id]
  



def vlanFlap(uut):
    cfg1 = \
    """
    vlan 1005-1006
    shut
    exit
    """
    cfg2 = \
    """
    vlan 1005-1006
    no sh
    exit 
    """
    for i in range(1,5):
        try:
            uut.configure(cfg1)
            countdown(2)
            uut.configure(cfg2)
        except:
            log.info("vlanflapp Failed")
            return 0
    return 1  

def nodeIsolate(uut):
    log.info(banner('S T A R T nodeIsolate'))
    cfg = \
    """
    interface {intf}
    shut
    """
    for uut in [uut]:
        for intf in uut.interfaces.keys():           
            if 'Eth' in uut.interfaces[intf].intf:
                intf=uut.interfaces[intf].intf
                log.info('shutting intf %r @ uut %r',intf,uut)
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('intf %r shut @ uut %r failed',intf,uut)
                    return 0

            elif 'loopback' in uut.interfaces[intf].intf:
                intf=uut.interfaces[intf].intf
                log.info('shutting intf %r @ uut %r',intf,uut)
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('intf %r shut @ uut %r failed',intf,uut)
                    return 0

    log.info(banner('E N D nodeIsolate'))
    return 1


def nodeNoIsolate(uut):
    log.info(banner('S T A R T nodeNoIsolate'))
    cfg = \
    """
    interface {intf}
    no shut
    """
    for uut in [uut]:
        for intf in uut.interfaces.keys():           
            if 'Eth' in uut.interfaces[intf].intf:
                intf=uut.interfaces[intf].intf
                log.info('UN shutting intf %r @ uut %r',intf,uut)
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('intf %r NO shut @ uut %r failed')
                    return 0

            elif 'loopback' in uut.interfaces[intf].intf:
                intf=uut.interfaces[intf].intf
                log.info('UN shutting intf %r @ uut %r',intf,uut)
                try:
                    uut.configure(cfg.format(intf=intf))
                except:
                    log.info('intf %r NO shut @ uut %r failed')
                    return 0

    log.info(banner('E N D nodeNoIsolate'))
    return 1

 
def sviFlap(uut):
    cfg1 = \
    """
    interface vlan 1005 
    shut
    interface vlan 1006
    shut
    """
    cfg2 = \
    """
    interface vlan 1005 
    no shut
    interface vlan 1006
    no shut
    """
    for i in range(1,5):
        try:
            uut.configure(cfg1)
            countdown(2)
            uut.configure(cfg2)
        except:
            log.info("vlanflapp Failed")
            return 0
    return 1  


def loopInterfaceFlap(uut):
    uut.configure("interface loopback 0 ; shut ; sleep 5 ; no shut") 

def secodaryIpRemoveAdd(uut):
    log.info(banner("starting VxlanStReset"))


    op = uut.execute('show run inter lo0 | incl secondary')
    for line in op.splitlines():
        if 'secondary' in line:
            ip_sec = line
            cfg = \
            f"""
            interface loopback0
            no {ip_sec}
            """
            uut.configure(cfg)  
            countdown(2)
            cfg2 = \
            f"""
            interface loopback0
            {ip_sec}
            """
            uut.configure(cfg2)  

def vPCMemberFlap(uut,po_list):
    log.info(banner("Starting vPCMemberFlap "))
    for po in po_list:
        cmd = uut.execute("show interface po {po} | json-pretty ".format(po=po))
        op=json.loads(cmd)
        op1=op["TABLE_interface"]["ROW_interface"]["eth_members"]
        intf_list = []
        if len(op1.split()) > 1:
            for mem in op1.split():
                if mem:
                    mem1 = mem.strip(",""")
                    intf_list.append(mem1)
        else:
            intf_list.append(op1)


    cfg = \
        """
        interface {intf}
        shut
        sleep 1
        no sh
        """

    for intf in intf_list:
        for i in range(1,3):
            try:
                uut.configure(cfg.format(intf=intf))
            except:
                log.info('Trigger4CoreIfFlapStaticPo failed @ 11')
                return 0
    return 1


def triggerLoopIfFlapOspf(uut):
    log.info(banner("Starting triggerLoopIfFlapOspf "))
    intf_list = []
    cmd = uut.execute("show ip ospf int brie | be Area")
    op=cmd.splitlines()
    for line in op:
        if line:
            if not 'Area' in line:
                if 'LOOPBACK' in line:
                    intf = line.split()[0]
                    intf_list.append(intf)

    #for intf in intf_list:
    for i in range(1,4):
        for intf in intf_list:
            cfg = \
            """
            interface {intf}
            shut
            """
            try:
                uut.configure(cfg.format(intf=intf))
            except:
                log.info('TriggerCoreIfFlapOspf failed @ 11')
                return 0

        countdown(1)
        for intf in intf_list:
            cfg = \
            """
            interface {intf}
            no shut
            """
            try:
                uut.configure(cfg.format(intf=intf))
            except:
                log.info('Trigger4CoreIfFlapStaticPo failed @ 11')
                return 0

    log.info(banner("END - TriggerCoreIfFlapOspf "))
    return 1


def swCleanup(uut):
    cfg = \
    """
    no feature nv overlay
    no nv overlay evpn
    no  feature vn-segment-vlan-based    
    """
    uut.configure(cfg,timeout=300)


def processRestartTest(uut,proc):
    """ function to configure vpc """
    logger.info(banner("Entering proc to restart the processes"))
    try:
        if not 'bash-shell' in uut.execute("sh run | inc feature"): 
            uut.configure('feature bash-shell',timeout=40)
    except:
        log.error('bash enable failed for %r',uut)
        log.error(sys.exc_info())

    try:
        log.info('-----Proc State before Restart-----')
        config_str = '''sh system internal sysmgr service name {proc} '''
        out=uut.execute(config_str.format(proc=proc),timeout=30)
        log.info('----------------------------------------')
        config_str = '''sh system internal sysmgr service name {proc} | grep PID'''
        out=uut.execute(config_str.format(proc=proc),timeout=30)
        pid  = out.split()[5].strip(',')
        uut.transmit('run bash sudo su\r',timeout=30)
        uut.receive('bash-4.4$')
        #uut.transmit('sudo su \r',timeout=20)
        #uut.receive('bash-4.4#')
        uut.transmit('kill %s\r' %pid,timeout=30)
        uut.receive('bash-4.4#')
        uut.transmit('exit \r',timeout=30)
        #uut.receive('bash-4.4$',timeout=20)
        #uut.transmit('exit \r')        
        uut.receive('#')
        log.info('-----Proc State AFTER Restart-----')
        config_str = '''sh system internal sysmgr service name {proc} '''
        out=uut.execute(config_str.format(proc=proc),timeout=20)
        log.info('----------------------------------------')
    except:
        log.error('proc restart test failed for %r',proc)
        log.error(sys.exc_info())


def configureTrm1(uut):
    cfg = \
    """
    feature ngmvpn 
    ip pim pre-build-spt
    ip igmp snooping vxlan

    route-map ssm-1 permit 10
    match ip multicast group 232.0.0.0/8
    route-map ssm-1 permit 11
    match ip multicast group 233.0.0.0/8 
    route-map no-pim-neighbor deny 10
    match ip address prefix-list anyip 

    interface loopback111
    description Overlay VRF RP Loopback interface
    vrf member vxlan-900101
    ip address 1.2.3.111/32
    no sh

    interface loopback112
    description Overlay VRF RP Loopback interface
    vrf member vxlan-900102
    ip address 1.2.3.112/32 
    ip pim sparse-mode
    no sh


    vrf context vxlan-900101
    vni 900101
    ip pim rp-address 1.2.3.111 group-list 224.0.0.0/4
    ip pim ssm route-map ssm-1
    rd auto
    address-family ipv4 unicast
        route-target both auto
        route-target both auto mvpn
        route-target both auto evpn
    address-family ipv6 unicast
        route-target both auto
        route-target both auto evpn
    
    vrf context vxlan-900102
    vni 900102
    ip pim rp-address 1.2.3.111 group-list 224.0.0.0/4
    ip pim ssm route-map ssm-1
    rd auto
    address-family ipv4 unicast
        route-target both auto
        route-target both auto mvpn
        route-target both auto evpn
    address-family ipv6 unicast
        route-target both auto
        route-target both auto evpn

    interface Vlan101-102
    ip pim sparse-mode


    interface Vlan1001-1020
    no shutdown
    ip pim sparse-mode
    ip pim neighbor-policy no-pim-neighbor
    fabric forwarding mode anycast-gateway

    interface nve1
    member vni 900101 associate-vrf
     mcast-group 225.3.3.3
    member vni 900102 associate-vrf
     mcast-group 225.3.3.4
        
            """
    if not 'paris' in uut.name:
        uut.configure(cfg,timeout=3000)

    cfg2 = \
    """
    interface nve1
    member vni 900101 associate-vrf
    multisite ingress-replication optimized
    member vni 900102 associate-vrf
    multisite ingress-replication optimized
    """    
    if 'bgw' in uut.name:
        uut.configure(cfg2,timeout=3000)  

