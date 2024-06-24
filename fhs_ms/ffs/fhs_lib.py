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
    


def checksnoopBinding(uut,snoop_mac_list):
    #import pdb;pdb.set_trace()

    snoop_mac_list2 = []
    for mac in snoop_mac_list:
        snoop_mac_list2.append(format_mac(mac))

    """
    """
    if 'crash' in uut.execute('show core'):
        print(f"Core found in {uut.name}")
        return False 

    ##import pdb;pdb.set_trace()
    op1 = uut.execute("show ip dhcp snooping binding ")
    for mac in snoop_mac_list2:
        if not mac in op1:
            log.info("++"*10)                
            log.info(f"MAC {mac} not found in {uut.name}")
            log.info(f'snooping table is {op1}')
            log.info("++"*10)     
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

def sviPing(uut1,uut2):
    ip1 = find_svi_ip(uut1,'1005')
    if not ip1:
        return 0
    ip2 = find_svi_ip(uut2,'1005')
    if not ip2:
        return 0
    
        




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
    l2vlan_per_vrf = int(l2_vlan_scale/l3_vlan_scale)
    mcast_group_start = conf_dict['vxlan']['mcast_group_start']
    #range = l2vlan_per_vrf
    uut.configure('no vlan 100-1200')
    uut.configure('no interface nve 1')

    cfg = \
        """
        """

    l2_vlan = l2_vlan_start
    l2_vni = l2_vni_start
    for i in range(l2_vlan_scale):        
        cfg += f'vlan {l2_vlan}\n'
        cfg += f'vn-seg {l2_vni}\n'   
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
            cfg += f'ipv6 address  {ipv6address}/96\n'
            cfg += f'fabric forwarding mode anycast-gateway\n'
            ipaddress = ip_address(ipaddress)+65536
            ipv6address = ip_address(ipv6address)+1024
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
        l3_vni_start = l3_vni_start+1

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']


    cfg += f'member vni {l2_vni_start}\n'
    cfg += f' ingress-replication protocol bgp\n'

    for i in range(l3_vlan_scale):
        cfg += f'member vni {l2_vni_start+1}-{l2_vni_start+l2vlan_per_vrf-1}\n'
        cfg += f'mcast-group {mcast_group_start}\n'
        mcast_group_start = ip_address(mcast_group_start)+1
        l2_vni_start = l2_vni_start+l2vlan_per_vrf-1

    uut.configure(cfg,timeout=300)

    l2_vlan_start = conf_dict['vxlan']['l2_vlan_start']
    l2_vni_start = conf_dict['vxlan']['l2_vni_start']
    l3_vlan_start = conf_dict['vxlan']['l3_vlan_start']    
    l3_vni_start = conf_dict['vxlan']['l3_vni_start']


    cfg = \
        """
        """
    cfg += f'router bgp 65535\n'
    for i in range(l3_vlan_scale):
        vrf = 'vxlan-'+str(l3_vni_start)
        cfg += f'vrf {vrf}\n'
        cfg += f'address-family ipv4 unicast\n'
        cfg += f'advertise l2vpn evpn\n'
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
            uut.configure(cfg,timeout=300)
        elif "Po" in line:
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
            uut.configure(cfg,timeout=300)
        elif 'Eth' in line:       
            intf = line.split()[0]
            cfg += f" interface {intf} \n"
            cfg +=  "ip pim sparse-mode \n"
    uut.configure(cfg,timeout=300)   



def preSetupVxlan(uut):
    clearIPConf(uut)

    cfg = \
    """
    no feature ospf
    no feature bgp
    no feature nv overlay
    no feature lacp
    no feature pim
    no vlan 2-3000
    no feature dhcp
    clear cores
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
    """
    uut.configure(cfg,timeout=300)
    time.sleep(10)
    uut.configure(cfg2,timeout=300)
    clearVrfConf(uut)
    cleararpConf(uut)
    #cleardhcpConf(uut)
 


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


def clearIPConf(uut):
    op1= uut.execute("show interf brie")
    intf_list = []
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
        #elif 'Eth' in line:       
        #    intf = line.split()[0]
        #    cfg += f" interface {intf} \n"
        #    cfg +=  "no ip address \n"
        #    uut.configure(cfg,timeout=300)

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
        ip_add = conf_dict['interfaces'][uut.name]['layer3'][intf]['ip_add']
        description = conf_dict['interfaces'][uut.name]['layer3'][intf]['Description']
        if 'loopback' in ip_add:
            intf1 = Interface(name=intf,device=uut)  
            intf1.description = description        
            intf1.unnumbered_intf_ref  = ip_add
            intf1.medium = 'p2p'
        else:
            prefix_length = conf_dict['interfaces'][uut.name]['layer3'][intf]['prefix_length']   
            #ipv6_address = conf_dict['interfaces'][uut.name]['layer3'][intf]['ipv6_address']         
            intf1.ipv4 = ip_add
            intf1.ipv4.netprefix_length = prefix_length

        intf1.shutdown = False    
        intf1.enabled = True
        intf1.switchport_enable = False
        intf1.mtu = 9126

        if 'port_channel' in intf: 
            intf1.channel_group_mode = 'active'
            intf_name = conf_dict['interfaces'][uut.name]['layer3'][intf]['name']            
            for member in conf_dict['interfaces'][uut.name]['layer3'][intf]['members']:
                intf2 = Interface(name=member,device=uut)
                intf1.add_member(intf2)
        # Build config
        cfgs = intf1.build_config(apply=True)


def configureL2Interface(uut,conf_dict): 
    ##import pdb;pdb.set_trace()
    #import pdb; pdb.set_trace()

    if 'layer2' in conf_dict['interfaces'][uut.name]:
        for intf in conf_dict['interfaces'][uut.name]['layer2']:    
            if 'Po' in intf:    
                print(intf)
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
                    print(member)  
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
                    
                uut.configure(cfgs2,timeout=300)

            elif 'Eth' in intf:  
                print(intf)
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

                uut.configure(cfgs,timeout=300)  
                # Build config
                
                #cfgs = intf1.build_config(apply=False)
                
                #cfgs2 = cfgs.replace("mode on","force mode on") 
                #uut.configure(cfgs,timeout=300)


def intfUnshut(uut,intf):
    intf1 = Interface(name=intf,device=uut)
    intf1.shutdown = False
    cfg = intf1.build_config(apply=True)

def getEthIntfList(uut):
    intf_list = []
    for line in uut.execute("show interface brief").splitlines():
        if not "VLAN" in line:
            if "Eth" in line:
                intf_list.append(line.split()[0])
    return(intf_list)  

def unshutAllintf(uut):
    intf_list1 = getEthIntfList(uut)
    for intf in intf_list1:
        intfUnshut(uut,intf)


def addVpcConfig(uut,conf_dict):
    if 'vpc' in conf_dict['interfaces'][uut.name]:    
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
  

def ProcessRestart(uut,proc):
    """ function to configure vpc """
    logger.info(banner("Entering proc to restart the processes"))
    try:
        uut.configure('feature bash-shell',timeout=40)
    except:
        log.error('bash enable failed for %r',uut)
        log.error(sys.exc_info())

    try:
        log.info('-----Proc State before Restart-----')
        config_str = '''sh system internal sysmgr service name {proc} '''
        out=uut.execute(config_str.format(proc=proc),timeout=40)
        log.info('----------------------------------------')
        config_str = '''sh system internal sysmgr service name {proc} | grep PID'''
        out=uut.execute(config_str.format(proc=proc),timeout=40)
        pid  = out.split()[5].strip(',')
        #uut.transmit('run bash \r',timeout=40)
        #uut.receive('bash-4.4$',timeout=40)
        #uut.transmit('sudo su \r',timeout=40)
        #uut.receive('bash-4.4$',timeout=40)
        #uut.transmit('kill %s\r' %pid,timeout=40)
        #uut.receive('bash-4.4$',timeout=40)
        #uut.transmit('exit \r',timeout=40)
        #uut.receive('bash-4.4$',timeout=40)
        #uut.transmit('exit \r',timeout=40)
        #uut.receive('#',timeout=40)
        uut.transmit('run bash \r',timeout=60)
        uut.receive('bash-4.4$')
        uut.transmit('sudo su \r',timeout=60)
        uut.receive('bash-4.4#')
        uut.transmit('kill %s\r' %pid,timeout=60)
        uut.receive('bash-4.4#')
        uut.transmit('exit \r',timeout=180)
        uut.receive('bash-4.4$',timeout=180)
        uut.transmit('exit \r')        
        uut.receive('#')
        log.info('-----Proc State AFTER Restart-----')
        config_str = '''sh system internal sysmgr service name {proc} '''
        out=uut.execute(config_str.format(proc=proc),timeout=40)
        log.info('----------------------------------------')
    except:
        log.error('proc restart test failed for %r',proc)
        log.error(sys.exc_info())


