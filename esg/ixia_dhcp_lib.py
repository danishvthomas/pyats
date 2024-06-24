#!/usr/bin/env python

# python
import logging
import unittest
from unittest.mock import Mock
from randmac import RandMac
import macaddress
from pyats.async_ import pcall            
import time
import os
from IxNetwork import IxNet
from vxlan3_lib import *

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# xBU-shared genie pacakge
from genie.libs.conf.interface import TunnelTeInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv4Interface, IPv4Address, IPv4Address
from genie.libs.conf.interface import Layer, L2_type, IPv4Addr, IPv4Addr,NveInterface
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
from ixiaPyats_lib import *

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError
import ixiaPyats_lib
ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

import random

import ixiaPyats_lib
#ixLib = ixiaPyats_lib.ixiaPyats_lib()

from vxlan3_lib import *
import sys
import os
try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)


def ixiaConnect(client_port_list):

    ixia_port_list =  " "

    for port in client_port_list:
         ixia_port_list = ixia_port_list+" "+port
         
    #srv_port+" "+client_port1+" "+client_port2+" "+client_port3+" "+client_port4
    ixia_chassis_ip = '10.197.127.16'
    ixia_tcl_server = '10.197.127.23'
    ixia_tcl_port = '8009'
 
    connect_status = ixiangpf.connect(
        reset                  = 1,
        device                 = ixia_chassis_ip,
        port_list              = ixia_port_list,
        ixnetwork_tcl_server   = ixia_tcl_server,
        tcl_server             = ixia_chassis_ip,
    )
    if connect_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('connect', connect_status)

    port_handle = connect_status['vport_list']
    return (port_handle)

def ixiaDhcpConfTest(port_list,server_port): 

    mac_start1 = macGenerator()
    mac_start2 = macGenerator() 
    mac_start3 = macGenerator() 
    mac_start4 = macGenerator() 
    mac_start5 = macGenerator() 
    mac_start6 = macGenerator()   

    port_list.remove(server_port)
    port_list.insert(0, server_port)


    port_handle = ixiaConnect(port_list)    

 
    countdown(20)
    ##import pdb;pdb.set_trace()            
    server_port_hdl = port_handle.split(' ')[0]
    client_port_hdl1 = port_handle.split(' ')[1]
    client_port_hdl2 = port_handle.split(' ')[2]
    client_port_hdl3 = port_handle.split(' ')[3]       
    client_port_hdl4 = port_handle.split(' ')[4]      
    client_port_hdl5 = port_handle.split(' ')[5]   
   

    client_hdl_list = [client_port_hdl1,client_port_hdl2,client_port_hdl3,client_port_hdl4,client_port_hdl5]

    ##import pdb;pdb.set_trace()        
    #dhcp_server = dhcpServerSetup(server_port_hdl) 
    #import pdb;pdb.set_trace()  

    dhcp_server = dhcpServerBringUp(server_port_hdl,1)

    #import pdb;pdb.set_trace()    
    
    #import pdb;pdb.set_trace()  
    client_topo_handle1,dhcp_client1 = dhcpClientSetup(client_port_hdl1,mac_start1)
    client_topo_handle2,dhcp_client2 = dhcpClientSetup(client_port_hdl2,mac_start2)
    client_topo_handle3,dhcp_client3 = dhcpClientSetup(client_port_hdl3,mac_start3)
    client_topo_handle4,dhcp_client4 = dhcpClientSetup(client_port_hdl4,mac_start4)
    client_topo_handle5,dhcp_client5 = dhcpClientSetup(client_port_hdl5,mac_start5)

 
    countdown(10)
    dhcpClientTrafficl(client_topo_handle1,client_topo_handle5)
    dhcpClientTrafficl(client_topo_handle5,client_topo_handle1)
    countdown(10)  
 
    for port_handle in client_hdl_list:        
        if not checkClientBindingStatsIxia(port_handle):
            ##import pdb;pdb.set_trace()    
            countdown(40)
            if not checkClientBindingStatsIxia(port_handle):
                log.info("checkClientBindingStatsIxia failed")
                #import pdb; pdb.set_trace()
                return 0


    trafficControll('run')
    countdown(30)
    
    trafficStats = getTrafficStats()
    tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
    rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
    if abs(int(tx)-int(rx)) > 200:
        log.info("Traffic Test failed")
        return 0

    IxiaReset()
    return 1





def esgAllTrafficTest(ixia_port_list,esg_scale):
    
    traffic_rate1 = 20000
    traffic_rate_per_group = int(traffic_rate1/esg_scale)

    scale = esg_scale

    vlan_1005 = '1005'
    vlan_1006 = '1006'

    ip_start_1005_1 = "4.5.0.10"
    ip_start_1005_2 = "4.5.1.100"

    ip_start_1006_1 = "4.6.1.100"
    ip_start_ext = "145.1.1.10"
    ip_prefix_ext = "145.1.0.0/16"
    ip_gw_ext = "145.1.1.1"  
    ip_gw_1005 =  "4.5.0.1"
    ip_gw_1006 =  "4.6.0.1"


    ipv6_start_1005_1 = "2002:1:1:1:1:0:405:10"
    ipv6_start_1005_2 = "2002:1:1:1:1:0:405:aa"
    ipv6_gw_1005_1 = "2002:1:1:1:1:0:405:1"

    ipv6_start_1006_1 = "2002:1:1:1:1:0:406:10"
    ipv6_gw_1006_1 = "2002:1:1:1:1:0:406:1"
    ipv6_gw_ext = "2002:1:1:1:1:0:145:1"  
    ipv6_ext = "2002:1:1:1:1:0:145:10"  

    try:
        log.info("  Host  Config ") 
 
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)    

        port_hdl_tetley1 = port_list.split(' ')[0]
        port_hdl_tetley2 = port_list.split(' ')[1]
        port_hdl_paris11 = port_list.split(' ')[2]
        port_hdl_paris12 = port_list.split(' ')[3]
        port_hdl_paris21 = port_list.split(' ')[4]
        port_hdl_paris22 = port_list.split(' ')[5]
        port_hdl_fx3005 = port_list.split(' ')[6]
        port_hdl_fx3004 = port_list.split(' ')[7]
        
    
        traffic_handle_1005_1 = ixiaHostConfig(port_hdl_tetley1,ip_start_1005_1,ip_gw_1005,scale,vlan_1005,"H_1005_1")
        traffic_handle_1005_2 = ixiaHostConfig(port_hdl_paris11,ip_start_1005_2,ip_gw_1005,scale,vlan_1005,"H_1005_2")
        traffic_handle_1006_1 = ixiaHostConfig(port_hdl_tetley2,ip_start_1006_1,ip_gw_1006,scale,vlan_1006,"H_1006_1")
        traffic_handle_1005_ext = ixiaHostConfig(port_hdl_paris21,ip_start_ext,ip_gw_ext,scale,vlan_1005,"H_1005_ext")


        traffic_handle_1005_v61 = ixiaHostConfigV6(port_hdl_fx3005,ipv6_start_1005_1,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_1_v6")
        traffic_handle_1005_v62 = ixiaHostConfigV6(port_hdl_paris12,ipv6_start_1005_2,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_2_v6")
        traffic_handle_1006_1_v6 = ixiaHostConfigV6(port_hdl_fx3004,ipv6_start_1006_1,ipv6_gw_1006_1,scale,vlan_1006,"H_1006_1_v6")
        traffic_handle_1005_ext_v6 = ixiaHostConfigV6(port_hdl_paris22,ipv6_ext,ipv6_gw_ext,scale,vlan_1005,"H_1005_ext_v6")

        _result_ = ixiahlt.test_control(action='start_all_protocols')

    except:
        log.info("  Host  Config  Failed") 
        return 0 

    log.info("SETUP TRAFFIC IN IXIA")     

    try:
         
        log.info("  TRAFFIC L2 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_2,"L2_Bidir_1005")
        log.info("  TRAFFIC L3 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1006_1,"L3_Bidir_1005_1006")   
        log.info("  TRAFFIC L3 External Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_ext,"L3_EXT_1005_1005")   

 

        log.info("  TRAFFIC L2 V6 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_v62,"L2_Bidir_1005_v6")
        log.info("  TRAFFIC L3 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1006_1_v6,"L3_Bidir_1005_1006_v6")   
        log.info("  TRAFFIC L3 External Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_ext_v6,"L3_EXT_1005_1005_v6")  

    except:
        return 0 
    


def esgAllTrafficTest2(ixia_port_list,esg_scale):
    
    traffic_rate1 = 20000
    traffic_rate_per_group = int(traffic_rate1/esg_scale)

    scale = esg_scale
 

    vlan_1005 = '1005'
    vlan_1006 = '1006'

    ip_start_1005_1 = "4.5.0.10"
    ip_start_1005_2 = "4.5.1.100"

    ip_start_1006_1 = "4.6.1.100"
    ip_start_ext = "145.1.1.10"
    ip_prefix_ext = "145.1.0.0/16"
    ip_gw_ext = "145.1.1.1"  
    ip_gw_1005 =  "4.5.0.1"
    ip_gw_1006 =  "4.6.0.1"


    ipv6_start_1005_1 = "2002:1:1:1:1:0:405:10"
    ipv6_start_1005_2 = "2002:1:1:1:1:0:405:aa"
    ipv6_gw_1005_1 = "2002:1:1:1:1:0:405:1"

    ipv6_start_1006_1 = "2002:1:1:1:1:0:406:10"
    ipv6_gw_1006_1 = "2002:1:1:1:1:0:406:1"
    ipv6_gw_ext = "2002:1:1:1:1:0:145:1"  
    ipv6_ext = "2002:1:1:1:1:0:145:10"  

    try:
        log.info("  Host  Config ") 
 
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)    

        port_hdl_tetley1 = port_list.split(' ')[0]
        port_hdl_tetley2 = port_list.split(' ')[1]
        port_hdl_paris11 = port_list.split(' ')[2]
        port_hdl_paris12 = port_list.split(' ')[3]
        port_hdl_paris21 = port_list.split(' ')[4]
        port_hdl_paris22 = port_list.split(' ')[5]
        port_hdl_fx3004 = port_list.split(' ')[6]

        traffic_handle_1005_1 = ixiaHostConfig(port_hdl_tetley1,ip_start_1005_1,ip_gw_1005,scale,vlan_1005,"H_1005_1")
        traffic_handle_1005_2 = ixiaHostConfig(port_hdl_paris11,ip_start_1005_2,ip_gw_1005,scale,vlan_1005,"H_1005_2")
        traffic_handle_1006_1 = ixiaHostConfig(port_hdl_paris12,ip_start_1006_1,ip_gw_1006,scale,vlan_1006,"H_1006_1")
        traffic_handle_1005_ext = ixiaHostConfig(port_hdl_paris21,ip_start_ext,ip_gw_ext,scale,vlan_1005,"H_1005_ext")


        traffic_handle_1005_v61 = ixiaHostConfigV6(port_hdl_tetley2,ipv6_start_1005_1,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_1_v6")
        traffic_handle_1005_v62 = ixiaHostConfigV6(port_hdl_fx3004,ipv6_start_1005_2,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_2_v6")
        #traffic_handle_1006_1_v6 = ixiaHostConfigV6(port_hdl_fx3004,ipv6_start_1006_1,ipv6_gw_1006_1,scale,vlan_1006,"H_1006_1_v6")
        traffic_handle_1005_ext_v6 = ixiaHostConfigV6(port_hdl_paris22,ipv6_ext,ipv6_gw_ext,scale,vlan_1005,"H_1005_ext_v6")

 

        _result_ = ixiahlt.test_control(action='start_all_protocols')

    except:
        log.info("  Host  Config  Failed") 
        return 0 

    log.info("SETUP TRAFFIC IN IXIA")     

    try:
         
        log.info("  TRAFFIC L2 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_2,"L2_Bidir_1005")
        log.info("  TRAFFIC L3 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1006_1,"L3_Bidir_1005_1006")   
        log.info("  TRAFFIC L3 External Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_ext,"L3_EXT_1005_1005")   

 

        log.info("  TRAFFIC L2 V6 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_v62,"L2_Bidir_1005_v6")
        log.info("  TRAFFIC L3 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_ext_v6,"L3_Bidir_1005_1006_v6")   
        log.info("  TRAFFIC L3 External Config ")
        generateTrafficV6(traffic_handle_1005_v62,traffic_handle_1005_ext_v6,"L3_EXT_1005_1005_v6")  

    except:
        return 0 


def esgAllTrafficTestScale(ixia_port_list,esg_scale):
    
    traffic_rate1 = 20000
    traffic_rate_per_group = int(traffic_rate1/esg_scale)

    scale = esg_scale
 

    vlan_1005 = '1005'
    vlan_1006 = '1006'

    ip_start_1005_1 = "4.5.0.10"
    ip_start_1005_2 = "4.5.1.100"

    ip_start_1006_1 = "4.6.1.100"
    ip_start_ext = "145.1.1.10"
    ip_prefix_ext = "145.1.0.0/16"
    ip_gw_ext = "145.1.1.1"  
    ip_gw_1005 =  "4.5.0.1"
    ip_gw_1006 =  "4.6.0.1"


    ipv6_start_1005_1 = "2002:1:1:1:1:0:405:10"
    ipv6_start_1005_2 = "2002:1:1:1:1:0:405:aa"
    ipv6_gw_1005_1 = "2002:1:1:1:1:0:405:1"

    ipv6_start_1006_1 = "2002:1:1:1:1:0:406:10"
    ipv6_gw_1006_1 = "2002:1:1:1:1:0:406:1"
    ipv6_gw_ext = "2002:1:1:1:1:0:145:1"  
    ipv6_ext = "2002:1:1:1:1:0:145:10"  

    try:
        log.info("  Host  Config ") 
 
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)    

        port_hdl_tetley1 = port_list.split(' ')[0]
        port_hdl_tetley2 = port_list.split(' ')[1]
        port_hdl_paris11 = port_list.split(' ')[2]
        port_hdl_paris12 = port_list.split(' ')[3]
        port_hdl_paris21 = port_list.split(' ')[4]
        port_hdl_paris22 = port_list.split(' ')[5]
        port_hdl_fx3004 = port_list.split(' ')[6]
        port_hdl_fx3003 = port_list.split(' ')[7]

        traffic_handle_1005_1 = ixiaHostConfig(port_hdl_tetley1,ip_start_1005_1,ip_gw_1005,scale,vlan_1005,"H_1005_1")
        traffic_handle_1005_2 = ixiaHostConfig(port_hdl_paris11,ip_start_1005_2,ip_gw_1005,scale,vlan_1005,"H_1005_2")
        traffic_handle_1006_1 = ixiaHostConfig(port_hdl_paris12,ip_start_1006_1,ip_gw_1006,scale,vlan_1006,"H_1006_1")
        traffic_handle_1005_ext = ixiaHostConfig(port_hdl_paris21,ip_start_ext,ip_gw_ext,scale,vlan_1005,"H_1005_ext")


        traffic_handle_1005_v61 = ixiaHostConfigV6(port_hdl_tetley2,ipv6_start_1005_1,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_1_v6")
        traffic_handle_1005_v62 = ixiaHostConfigV6(port_hdl_fx3004,ipv6_start_1005_2,ipv6_gw_1005_1,scale,vlan_1005,"H_1005_2_v6")
        traffic_handle_1006_1_v6 = ixiaHostConfigV6(port_hdl_fx3003,ipv6_start_1006_1,ipv6_gw_1006_1,scale,vlan_1006,"H_1006_1_v6")
        traffic_handle_1005_ext_v6 = ixiaHostConfigV6(port_hdl_paris22,ipv6_ext,ipv6_gw_ext,scale,vlan_1005,"H_1005_ext_v6")

 

        _result_ = ixiahlt.test_control(action='start_all_protocols')

    except:
        log.info("  Host  Config  Failed") 
        return 0 

    log.info("SETUP TRAFFIC IN IXIA")     

    try:
         
        log.info("  TRAFFIC L2 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_2,"L2_Bidir_1005_v4")
        log.info("  TRAFFIC L3 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1006_1,"L3_Bidir_1005_1006_v4")   
        log.info("  TRAFFIC L3 External Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_ext,"L3_EXT_1005_v4")   

 

        log.info("  TRAFFIC L2 V6 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_v62,"L2_Bidir_1005_v6")
        log.info("  TRAFFIC L3 stream Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1006_1_v6,"L3_Bidir_1005_1006_v6")   
        log.info("  TRAFFIC L3 External Config ")
        generateTrafficV6(traffic_handle_1005_v61,traffic_handle_1005_ext_v6,"L3_EXT_1005_v6")  

    except:
        return 0 
    


def broadcastTrafficSetup(ixia_port_list,esg_scale):

    #esg_scale = 1
    scale2 = 1
    
    traffic_rate1 = 20000
    traffic_rate_per_group = int(traffic_rate1/esg_scale)

    scale = esg_scale

    vlan_1005 = '1005'
    vlan_1006 = '1006'

    ip_start_1005_1 = "4.5.0.10"
    ip_start_1005_2 = "4.5.1.100"

    ip_start_1006_1 = "4.6.1.100"
    ip_start_ext = "145.1.1.10"
    ip_prefix_ext = "145.1.0.0/16"
    ip_gw_ext = "145.1.1.1"  
    ip_gw_1005 =  "4.5.0.1"
    ip_gw_1006 =  "4.6.0.1"



    try:
        log.info("  Host  Config ") 
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)    

        port_hdl_paris1 = port_list.split(' ')[0]
        port_hdl_tetley1 = port_list.split(' ')[1]
        port_hdl_tetley2 = port_list.split(' ')[2]
        port_hdl_paris2 = port_list.split(' ')[3]
    
        # traffic_handle_1005_1 = ixiaHostConfig(port_hdl_paris1,ip_start_1005_1,ip_gw_1005,scale,vlan_1005,"H_1005_1")
        # traffic_handle_1005_2 = ixiaHostConfig(port_hdl_tetley1,ip_start_1005_2,ip_gw_1005,scale,vlan_1005,"H_1005_2")
        # traffic_handle_1006_1 = ixiaHostConfig(port_hdl_tetley2,ip_start_1006_1,ip_gw_1006,scale,vlan_1006,"H_1006_1")
        # traffic_handle_1005_ext = ixiaHostConfig(port_hdl_paris2,ip_start_ext,ip_gw_ext,scale,vlan_1005,"H_1005_ext")

        # _result_ = ixiahlt.test_control(action='start_all_protocols')

    except:
        log.info("  Host  Config  Failed") 
        return 0 

    log.info("SETUP TRAFFIC IN IXIA")    

 

    try:
        log.info("  TRAFFIC L2 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_2,"L2_Bidir_1005")
        log.info("  TRAFFIC L3 stream Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1006_1,"L3_Bidir_1005_1006")   
        log.info("  TRAFFIC L3 External Config ")
        generateTraffic(traffic_handle_1005_1,traffic_handle_1005_ext,"L3_EXT_1005_1005")   
    except:
        return 0 
    



def ixiaTrafficSetupEsg(port1,port2,vlan1,vlan2,ip1,ip2,gw1,gw2,scale):
    traffic_handle1 = ixiaHostConfig(port1,ip1,gw1,scale,vlan1,"H1")
    traffic_handle2 = ixiaHostConfig(port2,ip2,gw2,scale,vlan2,"H2")
    _result_ = ixiahlt.test_control(action='start_all_protocols')
    countdown(1)
    log.info("  TRAFFIC L2 stream Config ")
    try:
        TrafficGenAll(traffic_handle1,traffic_handle2,'H1-H2','H2-H1') 
    except:
        return 0 
    return 1


def esgTrafficTest(port_list,server_port): 

    #server_port = fx3001_ixia

    #    ixia_port_list = [fx3001_ixia,fx3002_ixia,fx3003_ixia,paris001_ixia]

    mac_start1 = macGenerator()
    mac_start2 = macGenerator() 
    mac_start3 = macGenerator() 
    #mac_start4 = macGenerator() 
    #mac_start5 = macGenerator() 
    #mac_start6 = macGenerator()   

    port_list.remove(server_port)
    port_list.insert(0, server_port)

    port_handle = ixiaConnect(port_list)    

 
    countdown(20)
    server_port_hdl = port_handle.split(' ')[0]
    client_port_hdl1 = port_handle.split(' ')[1]
    client_port_hdl2 = port_handle.split(' ')[2]
    client_port_hdl3 = port_handle.split(' ')[3]       
    #client_port_hdl4 = port_handle.split(' ')[4]      
    #client_port_hdl5 = port_handle.split(' ')[5]   
   

    client_hdl_list = [client_port_hdl1,client_port_hdl2,client_port_hdl3]
    dhcp_server = dhcpServerBringUp(server_port_hdl,1)

    #    ixia_port_list = [fx3001_ixia,fx3002_ixia,fx3003_ixia,paris001_ixia]

    client_topo_handle1,dhcp_client1 = dhcpClientSetup(client_port_hdl1,mac_start1)
    client_topo_handle2,dhcp_client2 = dhcpClientSetup(client_port_hdl2,mac_start2)
    client_topo_handle3,dhcp_client3 = dhcpClientSetup(client_port_hdl3,mac_start3)
    #client_topo_handle4,dhcp_client4 = dhcpClientSetup(client_port_hdl4,mac_start4)
    #client_topo_handle5,dhcp_client5 = dhcpClientSetup(client_port_hdl5,mac_start5)

 
    countdown(10)
    dhcpClientTrafficl(client_topo_handle1,client_topo_handle3)
    dhcpClientTrafficl(client_topo_handle3,client_topo_handle1)
    dhcpClientTrafficl(client_topo_handle2,client_topo_handle3)
    dhcpClientTrafficl(client_topo_handle3,client_topo_handle2)
    dhcpClientTrafficl(client_topo_handle1,client_topo_handle2)
    dhcpClientTrafficl(client_topo_handle2,client_topo_handle1)
    countdown(10)  
 
    for port_handle in client_hdl_list:        
        if not checkClientBindingStatsIxia(port_handle):
            ##import pdb;pdb.set_trace()    
            countdown(40)
            if not checkClientBindingStatsIxia(port_handle):
                log.info("checkClientBindingStatsIxia failed")
                #import pdb; pdb.set_trace()
                return 0

    trafficControll('run')
    countdown(30)
    
    trafficStats = getTrafficStats()
    tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
    rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
    if abs(int(tx)-int(rx)) > 200:
        log.info("Traffic Test failed")
        return 0

    IxiaReset()
    return 1

                            
def trafficControll(action):    
    #def Ixia_start_Traffic():
    print("Running traffic")
    result = 1
    run_traffic = ixiangpf.traffic_control(
        action = action,
        traffic_generator='ixnetwork_540',
        max_wait_timer='60',
    )

    if run_traffic['status'] != IxiaHlt.SUCCESS:
        result = 0
        #ErrorHandler('test_control', run_traffic)

    return result
 
def getTrafficStats():   
    #import pdb;pdb.set_trace()
    protostats = ixiangpf.traffic_stats (
    mode = 'all',
    traffic_generator = 'ixnetwork_540',
    measure_mode = 'mixed'
    )
    #import pdb;pdb.set_trace()
    return protostats
                            

def IxiaReset():
    ixiangpf.cleanup_session(reset='1')



def HostMovetest(): 
    pass

    #leaf1 to leaf2
    # sw1 none at po11 vlan at po 12
    # leaf 1/2 none at po 11
    # leaf 2/3 none at po 12
    # 
    # initial H1---sw1---leaf2---leaf3---sw3-----H2       
    # Test1 H1---sw1---leaf1---leaf3---sw3-----H2   
    # Test2 H1---sw1---leaf1---leaf3---sw3-----H2   


def printDict(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)

def dhcpServerSetup(srv_port_hdl):
    serv_topology_status = createTopo(srv_port_hdl,1)
    srv_deviceGroup_handle = serv_topology_status['device_group_handle']
    top_handle = serv_topology_status['topology_handle']
    countdown(5)
    dhcp_status = dhcpServerConf(srv_deviceGroup_handle)
    countdown(5)
    dhcp_server = dhcp_status['dhcpv4server_handle']
    dhcpServerControll(dhcp_server,'collect') 
    countdown(10) 
    return(dhcp_server)


def dhcpClientSetup(client_port_hdl,mac_start):

    client_topo_handle,dhcpv4client_handle = ixiaDhcpClient(client_port_hdl,mac_start)

    #ixiaDhcpClient
    #configure_dhcpclient
    log.info("Starting dhcp client....")
    control_status = ixiangpf.emulation_dhcp_control(
        handle 			=	dhcpv4client_handle                            ,
        action = 'bind'						                            ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_control', control_status)


    countdown(30)
    ##import pdb;pdb.set_trace()    

    return(client_topo_handle,dhcpv4client_handle)




def destroyTopo(port_handle,topology_name):
    _result_ = ixiangpf.topology_config(
        topology_name      = topology_name,
        port_handle        = port_handle,
        mode                    =   'destroy'   
    )


def disableHapReset(uut):
    uut.configure('system no hap-reset ')

def ixiatrafficSetup(conf_dict):

    ipv4_address_1005_start1 = conf_dict['traffic']['ipv4_address_1005_start1']
    ipv4_address_1005_start2 = conf_dict['traffic']['ipv4_address_1005_start2']
    ipv4_address_1006_start1= conf_dict['traffic']['ipv4_address_1006_start1']
 
    ipv4_gw_1005=conf_dict['traffic']['ipv4_gw_1005']
    ipv4_gw_1006=conf_dict['traffic']['ipv4_gw_1006']
   
    vlan_1005=conf_dict['traffic']['vlan_1005']
    vlan_1006=conf_dict['traffic']['vlan_1006']

    scale=conf_dict['traffic']['scale']


    gx_paris001_ixia1 =conf_dict['traffic']['gx_paris001_ixia1']
    gx_paris001_ixia2 =conf_dict['traffic']['gx_paris001_ixia2']
    fx33_paris002_ixia1 =conf_dict['traffic']['fx33_paris002_ixia1']
    fx33_paris002_ixia2 =conf_dict['traffic']['fx33_paris002_ixia2']
    fx356_tetley001_ixia1 =conf_dict['traffic']['fx356_tetley001_ixia1']
    fx356_tetley001_ixia2 =conf_dict['traffic']['fx356_tetley001_ixia2']
    fx3005_ixia =conf_dict['traffic']['fx3005_ixia']
    fx3004_ixia =conf_dict['traffic']['fx3004_ixia']


    log.info("**************************************************************************************")
    log.info("TESTING L2 TRAFFIC")
    log.info("**************************************************************************************")

    ixia_port_list = [gx_paris001_ixia1,gx_paris001_ixia2,fx33_paris002_ixia1,\
                      fx33_paris002_ixia2,fx356_tetley001_ixia1,fx356_tetley001_ixia2,fx3005_ixia,fx3004_ixia]

    port_handle_list  = connectIxia(ixia_port_list) 

    traffic_handle_gxgx1_1005 = ixiaHostConfig(port_handle_list[0],ipv4_address_1005_start1,ipv4_gw_1005,\
                                     scale,vlan_1005,"gxgx1_vlan1005")

    traffic_handle_fx3561_1005= ixiaHostConfig(port_handle_list[4],ipv4_address_1005_start2,\
                                     ipv4_gw_1005,scale,vlan_1005,"fx3561_vlan1005")

    traffic_handle_fx3562_1006 = ixiaHostConfig(port_handle_list[5],ipv4_address_1006_start1,\
                                     ipv4_gw_1006,scale,vlan_1006,"fx3562_vlan1006")
  

    _result_ = ixiahlt.test_control(action='start_all_protocols')

    countdown(1)
 
    log.info("  TRAFFIC L2 stream Config ")
    TrafficGenAll(traffic_handle_gxgx1_1005,traffic_handle_fx3561_1005,'L2_GX_FX3','L2_FX3_GX') 
    log.info("  TRAFFIC L3 stream Config ")
    TrafficGenAll(traffic_handle_gxgx1_1005,traffic_handle_fx3562_1006,'L3_GX_FX3','L3_FX3_GX') 
 
 

def ixiaDhcpClient(port_handle,mac_start1):

    _result_ = ixiangpf.topology_config(
        topology_name      = """Topology 2""",
        port_handle        = port_handle,
    )
 
    topology_1_handle = _result_['topology_handle']
    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
    )
    
    deviceGroup_1_handle = _result_['device_group_handle']

 
    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = mac_start1,
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
 
    
    multivalue_1_handle = _result_['multivalue_handle']
    
    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 2""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_1_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
 
    ethernet_1_handle = _result_['ethernet_handle']
    
    _result_ = ixiangpf.emulation_dhcp_group_config(
        dhcp_range_ip_type               = "ipv4",
        dhcp_range_renew_timer           = "0",
        dhcp_range_server_address        = "4.5.0.9",
        dhcp_range_use_first_server      = "1",
        handle                           = ethernet_1_handle,
        use_rapid_commit                 = "0",
        protocol_name                    = """DHCPv4 Client 1""",
        dhcp4_broadcast                  = "0",
        dhcp4_gateway_address            = "0.0.0.0",
        dhcp4_gateway_mac                = "00.00.00.00.00.00",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_group_config', _result_)
    
 
    dhcpv4client_1_handle = _result_['dhcpv4client_handle']





def getDhcpServerstats(port_handle,dhcp_server):
    ##import pdb;pdb.set_trace()    
    ##import pdb;pdb.set_trace()    
    #print "Retrieve statistics"
    dhcp_stats_0 = ixiangpf.emulation_dhcp_server_stats(
        port_handle   = port_handle	                                           ,
        action 	= 'collect'				                                   ,
        execution_timeout = '60'                                              ,
    )
    if dhcp_stats_0['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_stats', dhcp_stats_0)

    #print "\n\nDHCP Server aggregate statistics:\n\n"
    log.info(dhcp_stats_0)

    dhcp_stats_0 = ixiangpf.emulation_dhcp_server_stats(
        dhcp_handle   = dhcp_server	                                           ,
        action =	'collect'				                                       ,
        execution_timeout = '60'                                                  ,
    )
    if dhcp_stats_0['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_stats', dhcp_stats_0)

    #print "\n\nDHCP Server per session statistics:\n\n"
    log.info(dhcp_stats_0)


def checkClientBindingStatsIxia(port_handle):
    client_stats = getDhcpClientstats(port_handle)
    if not client_stats['aggregate']['success_percentage'] == str(100):
        countdown(30)
        if not client_stats['aggregate']['success_percentage'] == str(100):
            return 0
    return 1


def getDhcpClientstats(port_handle):
    ##import pdb;pdb.set_trace()    
    dhcp_stats_0 = ixiangpf.emulation_dhcp_stats(
            port_handle  = port_handle	                                    ,
            mode         = 'aggregate_stats'					            ,
            dhcp_version =	'dhcp4'				                        ,
            execution_timeout = '60'                                       ,
    )
    if dhcp_stats_0['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_stats', dhcp_stats_0)

    #print "\n\nDHCP Client aggregate statistics:\n\n"
    log.info(dhcp_stats_0)
    return dhcp_stats_0

def getDhcpClientstats2(port_handle,dhcp_client):
    dhcp_stats_0 = ixiangpf.emulation_dhcp_stats(
        handle  = dhcp_client	                                        ,
        mode     =     'aggregate_stats'					                ,
        dhcp_version =	'dhcp4'				                            ,
        execution_timeout = '60'                                           ,
    )
    if dhcp_stats_0['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_stats', dhcp_stats_0)

    #print "\n\nDHCP Client aggregate statistics:\n\n"
    log.info(dhcp_stats_0)

    dhcp_stats_0 = ixiangpf.emulation_dhcp_stats(
            handle   = dhcp_client	                                    ,
            mode       =    'session'					                    ,
            dhcp_version  =	'dhcp4'				                        ,
            execution_timeout  = '60'                                       ,
    )
    if dhcp_stats_0['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_stats', dhcp_stats_0)

    #print "\n\nDHCP Client per session statistics:\n\n"
    log.info(dhcp_stats_0)






def createTopo(port_hdl,scale):
    topology_status = ixiangpf.topology_config(
        topology_name            =	port_hdl,
        port_handle              =	port_hdl,
        device_group_multiplier  =	scale,
    )
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)
    return (topology_status)  

def createTopo11(port_hdl,scale):
    topology_status = ixiangpf.topology_config(
        topology_name            =	port_hdl,
        port_handle              =	port_hdl,
        device_group_multiplier  =	scale,
    )
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)
    return (topology_status)  


def dhcpServerConfBK(group_handle):    
    mac = macGenerator()    
    dhcp_status = ixiangpf.emulation_dhcp_server_config(
            handle				=	group_handle              ,
            count				=	1			                            ,
            lease_time             =   '86400'                                ,
            ipaddress_count		=	'2000'			                        ,
            #ip_dns1		=		'10.10.10.10'		                        ,
            #ip_dns1_step	=			'0.0.0.1'			                    ,
            #ip_dns2		=		'20.20.20.20'		                        ,
            #ip_dns2_step	=			'0.0.1.0'			                    ,
            ipaddress_pool		=		'4.5.0.10'	                    ,
            ipaddress_pool_step		=	'0.0.0.1'			                ,
            ipaddress_pool_prefix_length =		'16'			                ,
            ipaddress_pool_prefix_step	=	'1'			                    ,
            dhcp_offer_router_address	=	'4.5.0.1'	                 ,
            dhcp_offer_router_address_step 	= '0.0.0.0'			            ,
            ip_address		=		'4.5.0.9'			                        ,
            ip_step		=		'0.0.0.0'			                        ,
            ip_gateway		=		'4.5.0.1'			                        ,
            ip_gateway_step		=	'0.0.0.0'			                    ,
            ip_prefix_length	=		'16'			                        ,
            ip_prefix_step		=		'0'			                        ,
            local_mac              =         mac                 ,
            local_mac_outer_step   =       '0000.0001.0000'                   ,
            local_mtu		=		'800'			                            ,
            vlan_id			=		'0'			                        ,
            vlan_id_step		=		'0'			                        ,
            protocol_name		=	"DHCP4 Server"                   ,
            use_rapid_commit		=	'1'			                        ,
            pool_address_increment	=	'0.0.0.1'		                    ,
            pool_address_increment_step =		'0.0.0.1'			            ,
            ping_timeout		=		'10'			                        ,
            ping_check		=		'1'			                            ,
            echo_relay_info     =       '1'                                   ,
            enable_resolve_gateway	=	'0'								  	,
            #manual_gateway_mac	=	    '00bd.2340.0000'					  	,
            #manual_gateway_mac_step =	'0000.0000.0001'					  	,
    )
    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_config', dhcp_status)

    return(dhcp_status)
    



def dhcpServerConf(group_handle):    
    #mac = macGenerator()    
    dhcp_status = ixiangpf.emulation_dhcp_server_config(
        handle                                 = group_handle,
        ip_dns1                                = "0.0.0.0",
        ip_dns2                                = "0.0.0.0",
        ip_version                             = "4",
        ip_address		                       = '4.5.0.9',
        ip_step		                           = '0.0.0.0',
        ip_gateway		                       = '4.5.0.1',
        dhcp_offer_router_address	           = '4.5.0.1',
        dhcp_offer_router_address_step 	       = '0.0.0.0',
        ipaddress_count                        = '2000',
        ipaddress_pool                         = "4.5.0.10",
        ipaddress_pool_prefix_length           = "16",
        ipaddress_pool_prefix_inside_step      = "0",
        lease_time                             = "86400",
        mode                                   = "create",
        protocol_name                          = "DHCPv4 Server 1",
        use_rapid_commit                       = "0",
        echo_relay_info                        = "1",
        pool_address_increment                 = "0.0.0.1",
        pool_count                             = "1",
        subnet_addr_assign                     = "0",

    )
    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_config', dhcp_status)

    return(dhcp_status)
    


def dhcpServerBringUp(port_hdl,scale):
    _result_ = ixiangpf.topology_config(
        topology_name            =	"Server",
        port_handle              =	port_hdl,
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)
    
    topology_1_handle = _result_['topology_handle']
    #ixnHLT['HANDLE,//topology:<1>'] = topology_1_handle
 
    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = "Server1",
        device_group_multiplier      = scale,
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)
    
    deviceGroup_1_handle = _result_['device_group_handle']
    #ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>'] = deviceGroup_1_handle
   
    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00.11.01.00.00.01",
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)
    
    multivalue_1_handle = _result_['multivalue_handle']
 
    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 1""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_1_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
    
    ethernet_1_handle = _result_['ethernet_handle']
    #ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>'] = ethernet_1_handle
 
    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "4.5.0.1",
        counter_step           = "0.0.0.0",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.0.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)
    
    multivalue_2_handle = _result_['multivalue_handle']
    countdown(10)    
    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 1""",
        protocol_handle                   = ethernet_1_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv4_enable_gratarprarp           = "0",
        ipv4_gratarprarp                  = "gratarp",
        gateway                           = multivalue_2_handle,
        intf_ip_addr                      = "4.5.0.5",
        intf_ip_addr_step                 = "0.0.1.0",
        netmask                           = "255.255.0.0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    countdown(10)
    ipv4_1_handle = _result_['ipv4_handle']
    #ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'] = ipv4_1_handle
  
    dhcp_status = ixiangpf.emulation_dhcp_server_config(
        dhcp_offer_router_address              = "4.5.0.1",
        handle                                 = ipv4_1_handle,
        ip_dns1                                = "0.0.0.0",
        ip_dns2                                = "0.0.0.0",
        ip_version                             = "4",
        ipaddress_count                        = "1000",
        ipaddress_pool                         = "4.5.0.100",
        ipaddress_pool_inside_step             = "0.0.0.1",
        ipaddress_pool_prefix_length           = "16",
        ipaddress_pool_prefix_inside_step      = "0",
        lease_time                             = "86400",
        mode                                   = "create",
        protocol_name                          = """DHCPv4 Server 1""",
        use_rapid_commit                       = "0",
        echo_relay_info                        = "1",
        pool_address_increment                 = "0.0.0.1",
        pool_count                             = "1",
        subnet_addr_assign                     = "0",
        subnet                                 = "relay",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_config', _result_)

    countdown(10)
    dhcp_server = dhcp_status['dhcpv4server_handle']

    #import pdb;pdb.set_trace()

    '''

    _result_ = ixiangpf.emulation_dhcp_server_config(
        handle                                = "/globals",
        ip_version                            = "4",
        mode                                  = "create",
        ping_check                            = "0",
        ping_timeout                          = "1",
        offer_timeout                         = "20",
        init_force_renew_timeout              = "4",
        force_renew_factor                    = "2",
        force_renew_max_rc                    = "3",
        reconfigure_rate_scale_mode           = "port",
        reconfigure_rate_enabled              = "1",
        reconfigure_rate_max_outstanding      = "400",
        reconfigure_rate_interval             = "1000",
        reconfigure_rate                      = "200",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_config', _result_)
    
    import pdb;pdb.set_trace()
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        arp_on_linkup                       = "0",
        single_arp_per_gateway              = "1",
        ipv4_send_arp_rate                  = "200",
        ipv4_send_arp_interval              = "1000",
        ipv4_send_arp_max_outstanding       = "400",
        ipv4_send_arp_scale_mode            = "port",
        ipv4_attempt_enabled                = "0",
        ipv4_attempt_rate                   = "200",
        ipv4_attempt_interval               = "1000",
        ipv4_attempt_scale_mode             = "port",
        ipv4_diconnect_enabled              = "0",
        ipv4_disconnect_rate                = "200",
        ipv4_disconnect_interval            = "1000",
        ipv4_disconnect_scale_mode          = "port",
        ipv4_re_send_arp_on_link_up         = "true",
        ipv4_permanent_mac_for_gateway      = "false",
        ipv4_gratarp_transmit_count         = "1",
        ipv4_gratarp_transmit_interval      = "3000",
        ipv4_rarp_transmit_count            = "1",
        ipv4_rarp_transmit_interval         = "3000",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    import pdb;pdb.set_trace()
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        ethernet_attempt_enabled            = "0",
        ethernet_attempt_rate               = "200",
        ethernet_attempt_interval           = "1000",
        ethernet_attempt_scale_mode         = "port",
        ethernet_diconnect_enabled          = "0",
        ethernet_disconnect_rate            = "200",
        ethernet_disconnect_interval        = "1000",
        ethernet_disconnect_scale_mode      = "port",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
    '''
    control_status = ixiangpf.emulation_dhcp_server_control(
        dhcp_handle = 			dhcp_server 		                           ,
        action = "collect"								                           ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_control', control_status)

    time.sleep(60)
    #import pdb;pdb.set_trace()
    return(dhcp_server)


def dhcpServerControll(dhcp_server,action):  
    ##print "Starting dhcp server...."
    control_status = ixiangpf.emulation_dhcp_server_control(
        dhcp_handle = 			dhcp_server 		                           ,
        action = action								                           ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_control', control_status)

    time.sleep(10)


    #for client_port_hdl in client_port_hdl_list:

    #    topology_status = ixiangpf.topology_config(
    #        topology_name           =   "DHCPv4 Client"+client_port_hdl  ,
    #        port_handle             =   client_port_hdl                             ,
    #        device_group_multiplier =    '1'                                 ,
    #    )
    #    if topology_status['status'] != IxiaHlt.SUCCESS:
    #        ixnHLT_errorHandler('topology_config', topology_status)


    #    deviceGroup_first_handle = topology_status ['device_group_handle']
    #    top_1 = topology_status['topology_handle']

    #    client_topo_list.append(top_1)

def configure_dhcpclient(client_port_hdl,mac_start): 
    #import pdb;pdb.set_trace()
    topology_status = ixiangpf.topology_config(
        topology_name      = "client"+str(random.randint(1,100)),
        port_handle        = client_port_hdl,
    )
         
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)
    
    # n The attribute: note with the value:  is not supported by scriptgen.
    client_topo_handle = topology_status['topology_handle']
    #ixnHLT['HANDLE,//topology:<2>'] = topology_2_handle
 
    _result_ = ixiangpf.topology_config(
        topology_handle              = client_port_hdl,
        device_group_name            =  "client"+str(random.randint(1,100)),
        device_group_multiplier      = 1,
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)
    
    deviceGroup_2_handle = _result_['device_group_handle']
    #ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>'] = deviceGroup_2_handle
    
    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 5""",
        protocol_handle              = deviceGroup_2_handle,
        mtu                          = "1500",
        src_mac_addr                 = mac_start,
        src_mac_addr_step            = "00.00.00.00.00.02",
        vlan                         = "0",
        vlan_id                      = '%s' % ("0"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
    
 
    ethernet_2_handle = _result_['ethernet_handle']
    #ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>'] = ethernet_2_handle
    
    _result_ = ixiangpf.emulation_dhcp_group_config(
        dhcp_range_ip_type               = "ipv4",
        dhcp_range_renew_timer           = "20000",
        dhcp_range_server_address        = "4.5.0.9",
        dhcp_range_use_first_server      = "1",
        handle                           = ethernet_2_handle,
        use_rapid_commit                 = "1",
        protocol_name                    = "Dhcp_client"+client_port_hdl,
        dhcp4_broadcast                  = "1",
        dhcp4_gateway_address            = "0.0.0.0",
        dhcp4_gateway_mac                = "00.00.00.00.00.00",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_group_config', _result_)
    
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    dhcpv4client_handle = _result_['dhcpv4client_handle']
    #ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/dhcpv4client:<1>'] = dhcpv4client_1_handle
    
   

    return client_topo_handle,dhcpv4client_handle

    dhcpClientControll(dhcp_client,'bind')


 


def dhcpTest(port_list,server_port): 

    mac_start1 = macGenerator()
    mac_start2 = macGenerator() 
    mac_start3 = macGenerator() 
    mac_start4 = macGenerator() 
    mac_start5 = macGenerator() 
    mac_start6 = macGenerator()   

    port_list.remove(server_port)
    port_list.insert(0, server_port)


    port_handle = ixiaConnect(port_list)    

 
    countdown(20)
    ##import pdb;pdb.set_trace()            
    server_port_hdl = port_handle.split(' ')[0]
    client_port_hdl1 = port_handle.split(' ')[1]
    client_port_hdl2 = port_handle.split(' ')[2]
    client_port_hdl3 = port_handle.split(' ')[3]       
    client_port_hdl4 = port_handle.split(' ')[4]      
    client_port_hdl5 = port_handle.split(' ')[5] 


    #import pdb;pdb.set_trace()

    devicegroup_handle_srv,topo_handle_srv = createTopology(server_port_hdl,1)
    dhcp_server = configureDhcpServer(devicegroup_handle_srv)
    
    devicegroup_handle_client1,topo_handle_client1 = createTopology(client_port_hdl1,1)
    dhcp_client1 = configureDhcpClient(devicegroup_handle_client1)

    devicegroup_handle_client2,topo_handle_client1 = createTopology(client_port_hdl2,1)
    dhcp_client2 = configureDhcpClient(devicegroup_handle_client2)

    devicegroup_handle_client3,topo_handle_client3 = createTopology(client_port_hdl3,1)
    devicegroup_handle_client4,topo_handle_client4 = createTopology(client_port_hdl4,1)
    devicegroup_handle_client5,topo_handle_client5 = createTopology(client_port_hdl5,1)


 ####################### Create Topologies ###################################
def createTopology(port_handle,scale):
    topology_status = ixiangpf.topology_config(
        topology_name           =   "DHCPv4 Client"                    ,
        port_handle             =   port_handle                             ,
        device_group_multiplier =    scale                                 ,
    )
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)

    devicegroup_handle = topology_status ['device_group_handle']
    topo_handle = topology_status['topology_handle']
    return (devicegroup_handle,topo_handle)


 
def configureDhcpClient(devicegroup_handle):
    mac_start1 = macGenerator()
    dhcp_status = ixiangpf.emulation_dhcp_group_config(
        handle      =  devicegroup_handle                         ,
        protocol_name 		=		"Dhcp_client"                     ,
        mac_addr  =  mac_start1                                        ,
        mac_addr_step		=		'00.00.00.00.00.02'	                  ,
        use_rapid_commit = '0'                                              ,
        enable_stateless = '0'                                              ,
        num_sessions     =  '1'                                           ,
        dhcp4_broadcast   = '1'                                            ,
        dhcp_range_use_first_server = '1'                                   ,
        dhcp_range_renew_timer = '20'                                       ,
        dhcp_range_ip_type       =      'ipv4'                             ,
        vendor_id                =          'any'                          ,
    )
    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_group_config', dhcp_status)

    dhcp_client = dhcp_status['dhcpv4client_handle']

    dhcp_status = ixiangpf.emulation_dhcp_config(
        handle 			=	dhcp_client                             ,
        mode			=		'modify'	                                 ,
        release_rate	=			'65'	                                 ,
        msg_timeout		=		'5'	                                 ,
        request_rate	=			'7'	                                 ,
        retry_count		=		'2'	                                 ,
        interval_stop	=			'5'	                                 ,
        interval_start		=		'6'	                                 ,
        min_lifetime		=		'10'	                                 ,
        max_restarts		=		'20'	                                 ,
        max_lifetime		=		'30'	                                 ,
        enable_restart		=		'1'	                                 ,
        enable_lifetime		=	'0'	                                 ,
        client_port             =       '119'                              ,
        skip_release_on_stop    =       '1'                                ,
        renew_on_link_up        =       '1'                                ,
    )
    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_config', dhcp_status)

    control_status = ixiangpf.emulation_dhcp_control(
        handle 			=	dhcp_client                            ,
        action = 'bind'						                            ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_control', control_status)

    return(dhcp_client)


def configureDhcpServer(devicegroup_handle):
    mac_start1 = macGenerator()	
    dhcp_status = ixiangpf.emulation_dhcp_server_config(
        handle				=	devicegroup_handle              ,
		count				=	'5'			                            ,
		lease_time             =   '86400'                                ,
		ipaddress_count		=	'10'			                        ,
		ip_dns1		=		'10.10.10.10'		                        ,
		ip_dns1_step	=			'0.0.0.1'			                    ,
		ip_dns2		=		'20.20.20.20'		                        ,
		ip_dns2_step	=			'0.0.1.0'			                    ,
		ipaddress_pool		=		'4.5.0.100'	                    ,
		ipaddress_pool_step		=	'0.0.0.1'			                ,
		ipaddress_pool_prefix_length =		'16'			                ,
		ipaddress_pool_prefix_step	=	'1'			                    ,
		dhcp_offer_router_address	=	'4.5.0.9'	                ,
		dhcp_offer_router_address_step 	= '0.0.0.1'			            ,
		ip_address		=		'4.5.0.10'			                        ,
		ip_step		=		'0.0.0.1'			                        ,
		ip_gateway		=		'4.5.0.1'			                        ,
		ip_gateway_step		=	'0.0.0.0'			                    ,
		ip_prefix_length	=		'16'			                        ,
		ip_prefix_step		=		'1'			                        ,
		local_mac              =         mac_start1                 ,
       	local_mac_outer_step   =       '0000.0001.0000'                   ,
		local_mtu		=		'800'			                            ,
		vlan_id			=		'100'			                        ,
		vlan_id_step		=		'10'			                        ,
		protocol_name		=	"DHCP4 Server"                   ,
		use_rapid_commit		=	'1'			                        ,
		ping_timeout		=		'10'			                        ,
		ping_check		=		'1'			                            ,
        echo_relay_info     =       '1'                                   ,
		enable_resolve_gateway	=	'0'								  	,
        )

    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_config', dhcp_status)

    dhcp_server = dhcp_status['dhcpv4server_handle']
 

    control_status = ixiangpf.emulation_dhcp_server_control(
            dhcp_handle = 			dhcp_server 		                           ,
            action = 'collect'								                           ,
        )
    if control_status['status'] != IxiaHlt.SUCCESS:
	    ixnHLT_errorHandler('emulation_dhcp_server_control', control_status)


    return(dhcp_server)    



 


def dhcpTest100(port_list,server_port):
    scale = 1
    log.info(" ====== START dhcpTest100  ====== ")

    port_list.remove(server_port)
    port_list.insert(0, server_port)


    port_handle = ixiaConnect(port_list)    

    server_port_hdl = port_handle.split(' ')[0]
    client_port_hdl1 = port_handle.split(' ')[1]
    client_port_hdl2 = port_handle.split(' ')[2]
    client_port_hdl3 = port_handle.split(' ')[3]       
    client_port_hdl4 = port_handle.split(' ')[4]      
    client_port_hdl5 = port_handle.split(' ')[5] 


    _result_ = ixiangpf.connect(
        reset=1,
        device=chassis,
        port_list=port_list,
        ixnetwork_tcl_server='10.197.127.23',
        tcl_server=tcl_server,
        guard_rail=guard_rail,
        return_detailed_handles=0
    )

    _result_ = ixiangpf.topology_config(
        topology_name      = """Topology 1""",
        port_handle        = server_port_hdl,
    )

    topology_1_handle = _result_['topology_handle']


    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = server_port_hdl,
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
    )

    deviceGroup_1_handle = _result_['device_group_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00.12.11.00.00.01",
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )

    multivalue_1_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 1""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_1_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )

    ethernet_1_handle = _result_['ethernet_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "4.5.0.1",
        counter_step           = "0.0.0.0",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )

    multivalue_2_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 1""",
        protocol_handle                   = ethernet_1_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv4_enable_gratarprarp           = "0",
        ipv4_gratarprarp                  = "gratarp",
        gateway                           = multivalue_2_handle,
        intf_ip_addr                      = "4.5.0.5",
        intf_ip_addr_step                 = "0.0.1.0",
        netmask                           = "255.255.0.0",
    )


    ipv4_1_handle = _result_['ipv4_handle']


    _result_ = ixiangpf.emulation_dhcp_server_config(
        dhcp_offer_router_address              = "4.5.0.1",
        handle                                 = ipv4_1_handle,
        ip_dns1                                = "0.0.0.0",
        ip_dns2                                = "0.0.0.0",
        ip_version                             = "4",
        ipaddress_count                        = "1000",
        ipaddress_pool                         = "4.5.0.100",
        ipaddress_pool_inside_step             = "0.0.0.1",
        ipaddress_pool_prefix_length           = "16",
        ipaddress_pool_prefix_inside_step      = "0",
        lease_time                             = "86400",
        mode                                   = "create",
        protocol_name                          = """DHCPv4 Server 1""",
        use_rapid_commit                       = "0",
        echo_relay_info                        = "1",
        pool_address_increment                 = "0.0.0.1",
        pool_count                             = "1",
        subnet_addr_assign                     = "0",
        subnet                                 = "relay",
    )


    dhcpv4server_1_handle = _result_['dhcpv4server_handle']


    _result_ = ixiangpf.emulation_dhcp_server_config(
        handle                                = "/globals",
        ip_version                            = "4",
        mode                                  = "create",
        ping_check                            = "0",
        ping_timeout                          = "1",
        offer_timeout                         = "20",
        init_force_renew_timeout              = "4",
        force_renew_factor                    = "2",
        force_renew_max_rc                    = "3",
        reconfigure_rate_scale_mode           = "port",
        reconfigure_rate_enabled              = "1",
        reconfigure_rate_max_outstanding      = "400",
        reconfigure_rate_interval             = "1000",
        reconfigure_rate                      = "200",
    )

    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        arp_on_linkup                       = "0",
        single_arp_per_gateway              = "1",
        ipv4_send_arp_rate                  = "200",
        ipv4_send_arp_interval              = "1000",
        ipv4_send_arp_max_outstanding       = "400",
        ipv4_send_arp_scale_mode            = "port",
        ipv4_attempt_enabled                = "0",
        ipv4_attempt_rate                   = "200",
        ipv4_attempt_interval               = "1000",
        ipv4_attempt_scale_mode             = "port",
        ipv4_diconnect_enabled              = "0",
        ipv4_disconnect_rate                = "200",
        ipv4_disconnect_interval            = "1000",
        ipv4_disconnect_scale_mode          = "port",
        ipv4_re_send_arp_on_link_up         = "true",
        ipv4_permanent_mac_for_gateway      = "false",
        ipv4_gratarp_transmit_count         = "1",
        ipv4_gratarp_transmit_interval      = "3000",
        ipv4_rarp_transmit_count            = "1",
        ipv4_rarp_transmit_interval         = "3000",
    )


    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        ethernet_attempt_enabled            = "0",
        ethernet_attempt_rate               = "200",
        ethernet_attempt_interval           = "1000",
        ethernet_attempt_scale_mode         = "port",
        ethernet_diconnect_enabled          = "0",
        ethernet_disconnect_rate            = "200",
        ethernet_disconnect_interval        = "1000",
        ethernet_disconnect_scale_mode      = "port",
    )


    countdown(50)                  
    control_status = ixiangpf.emulation_dhcp_server_control(
            dhcp_handle = 			dhcpv4server_1_handle 		                           ,
            action = 'collect'								                           ,
        )

    countdown(50)   
    devicegroup_handle_client1,topo_handle_client1 = createTopology(client_port_hdl1,1)
    dhcp_client1 = configureDhcpClient(devicegroup_handle_client1)

    devicegroup_handle_client2,topo_handle_client1 = createTopology(client_port_hdl2,1)
    dhcp_client2 = configureDhcpClient(devicegroup_handle_client2)

    devicegroup_handle_client3,topo_handle_client3 = createTopology(client_port_hdl3,1)
    dhcp_client3 = configureDhcpClient(devicegroup_handle_client3)
    
    devicegroup_handle_client4,topo_handle_client4 = createTopology(client_port_hdl4,1)
    dhcp_client4 = configureDhcpClient(devicegroup_handle_client4)    

    devicegroup_handle_client5,topo_handle_client5 = createTopology(client_port_hdl5,1)
    dhcp_client5 = configureDhcpClient(devicegroup_handle_client5)



 
def ixiaDhcpClient(port_handle,mac_start1):

    _result_ = ixiangpf.topology_config(
        topology_name      = """Topology 2""",
        port_handle        = port_handle,
    )
 
    topology_1_handle = _result_['topology_handle']
   
    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
    )
    
    deviceGroup_1_handle = _result_['device_group_handle']

 
    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = mac_start1,
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
 
    
    multivalue_1_handle = _result_['multivalue_handle']
    
    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 2""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_1_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
 
    ethernet_1_handle = _result_['ethernet_handle']
    
    _result_ = ixiangpf.emulation_dhcp_group_config(
        dhcp_range_ip_type               = "ipv4",
        dhcp_range_renew_timer           = "0",
        dhcp_range_server_address        = "4.5.0.9",
        dhcp_range_use_first_server      = "1",
        handle                           = ethernet_1_handle,
        use_rapid_commit                 = "0",
        protocol_name                    = """DHCPv4 Client 1""",
        dhcp4_broadcast                  = "0",
        dhcp4_gateway_address            = "0.0.0.0",
        dhcp4_gateway_mac                = "00.00.00.00.00.00",
    )

 
    dhcpv4client_1_handle = _result_['dhcpv4client_handle']
    return(topology_1_handle,dhcpv4client_1_handle)


def generateTraffic(src_handle,dst_handle,StreamName):          

    countdown(1) 
    rate_pps = 20000
    frame_size = 500

    #def Ixia_Configure_Traffic(topology_1_handle, topology_2_handle, rate_pps, frame_size):
    print("Configuring L2-L3 traffic")
    _result_ = ixiangpf.traffic_config(
        mode='create',
        name=StreamName,
        endpointset_count='1',
        l4_protocol = 'tcp',
        tcp_src_port = '1001 1003',
        tcp_dst_port = '1005 1007',
        tcp_src_port_mode = 'list',
        tcp_dst_port_mode = 'list',
        emulation_src_handle=src_handle,
        emulation_dst_handle=dst_handle,
        bidirectional = '1',
        circuit_endpoint_type='ipv4',
        rate_pps=rate_pps,
        frame_size=frame_size,
        mac_dst_mode='fixed',
        mac_src_mode='fixed',
        track_by='trackingenabled0',
    )

    if _result_['status'] != IxiaHlt.SUCCESS:
        trafficItem_handle = 0
        #ErrorHandler('traffic_config', _result_)
    else:
        trafficItem_handle = _result_["stream_id"]
    
    return trafficItem_handle


def generateTrafficV6(src_handle,dst_handle,StreamName):          

    countdown(1) 
    rate_pps = 20000
    frame_size = 500

    #def Ixia_Configure_Traffic(topology_1_handle, topology_2_handle, rate_pps, frame_size):
    print("Configuring L2-L3 traffic")
    _result_ = ixiangpf.traffic_config(
        mode='create',
        name=StreamName,
        endpointset_count='1',
        l4_protocol = 'tcp',
        tcp_src_port = '1001 1003',
        tcp_dst_port = '1005 1007',
        tcp_src_port_mode = 'list',
        tcp_dst_port_mode = 'list',
        emulation_src_handle=src_handle,
        emulation_dst_handle=dst_handle,
        bidirectional = '1',
        circuit_endpoint_type='ipv6',
        rate_pps=rate_pps,
        frame_size=frame_size,
        mac_dst_mode='fixed',
        mac_src_mode='fixed',
        track_by='trackingenabled0',
    )

    if _result_['status'] != IxiaHlt.SUCCESS:
        trafficItem_handle = 0
        #ErrorHandler('traffic_config', _result_)
    else:
        trafficItem_handle = _result_["stream_id"]
    
    return trafficItem_handle


def TrafficControll():     
    result_ = ixiangpf.traffic_control(
        action='stop',
        traffic_generator='ixnetwork_540',
        type='l23',
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        #ErrorHandler('traffic_control', _result_)
        return 0    

def stopAppProto():     
    stop = ixiangpf.test_control(action='stop_all_protocols')
    if stop['status'] != IxiaHlt.SUCCESS:
        #ErrorHandler('test_control', stop)	
        return 0

    time.sleep(2)
       




def ixiaHostConfigV6(port_handle,ipv6_address_start,ipv6_gw,scale,vlan_id,topology_name):
    _result_ = ixiangpf.topology_config(
        topology_name      = topology_name,
        port_handle        = port_handle,
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    topology_2_handle = _result_['topology_handle']
    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_2_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = scale,
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)
    
    deviceGroup_2_handle = _result_['device_group_handle']

    mac_start2 = macGenerator() 
    
    if 'novlan' in vlan_id:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = '0',
            vlan_id_step                 = '0',
            vlan_id_count                = '0',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            pass
        
        ethernet_2_handle = _result_['ethernet_handle']
    else:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = str(vlan_id),
            vlan_id_step                 = '0',
            vlan_id_count                = '1',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            pass
        
        ethernet_2_handle = _result_['ethernet_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv6 1""",
        protocol_handle                   = ethernet_2_handle,
        ipv6_multiplier                   = "1",
        ipv6_resolve_gateway              = "1",
        ipv6_gateway                      = ipv6_gw,
        ipv6_intf_addr                    = ipv6_address_start,
        ipv6_gateway_step                 = "0:0:0:0:0:0:0:0",
        ipv6_prefix_length                = "112",
        ipv6_send_ra                      = "0",
        ipv6_discover_gateway_ip          = "0",
        ipv6_include_ra_prefix            = "0",


    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass
    

    ipv6_1_handle = _result_['ipv6_handle']
         
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        arp_on_linkup                       = "0",
        single_arp_per_gateway              = "1",
        ipv4_send_arp_rate                  = "200",
        ipv4_send_arp_interval              = "1000",
        ipv4_send_arp_max_outstanding       = "400",
        ipv4_send_arp_scale_mode            = "port",
        ipv4_attempt_enabled                = "0",
        ipv4_attempt_rate                   = "200",
        ipv4_attempt_interval               = "1000",
        ipv4_attempt_scale_mode             = "port",
        ipv4_diconnect_enabled              = "0",
        ipv4_disconnect_rate                = "200",
        ipv4_disconnect_interval            = "1000",
        ipv4_disconnect_scale_mode          = "port",
        ipv4_re_send_arp_on_link_up         = "true",
        ipv4_permanent_mac_for_gateway      = "false",
        ipv4_gratarp_transmit_count         = "1",
        ipv4_gratarp_transmit_interval      = "3000",
        ipv4_rarp_transmit_count            = "1",
        ipv4_rarp_transmit_interval         = "3000",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass
        
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        ethernet_attempt_enabled            = "0",
        ethernet_attempt_rate               = "200",
        ethernet_attempt_interval           = "1000",
        ethernet_attempt_scale_mode         = "port",
        ethernet_diconnect_enabled          = "0",
        ethernet_disconnect_rate            = "200",
        ethernet_disconnect_interval        = "1000",
        ethernet_disconnect_scale_mode      = "port",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass
    
    return(ipv6_1_handle)  


def ixiaHostConfigV4V6(port_handle,ipv4_address_start,ipv4_gw,ipv6_address_start,ipv6_gw,scale,vlan_id,topology_name):
    _result_ = ixiangpf.topology_config(
        topology_name      = topology_name,
        port_handle        = port_handle,
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass

    topology_2_handle = _result_['topology_handle']

    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_2_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = scale,
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass
    
    deviceGroup_2_handle = _result_['device_group_handle']

    mac_start2 = macGenerator() 


    if 'novlan' in vlan_id:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = '0',
            vlan_id_step                 = '0',
            vlan_id_count                = '0',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            pass
        
        ethernet_2_handle = _result_['ethernet_handle']
    else:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = str(vlan_id),
            vlan_id_step                 = '0',
            vlan_id_count                = '1',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            pass
        
        ethernet_2_handle = _result_['ethernet_handle']



 
    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 2""",
        protocol_handle                   = ethernet_2_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        gateway                           =  ipv4_gw,
        gateway_step                      = "0.0.0.0",
        intf_ip_addr                      = ipv4_address_start,
        intf_ip_addr_step                 = "0.0.0.1",
        netmask                           = "255.255.0.0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass

    ipv4_1_handle = _result_['ipv4_handle']


    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv6 1""",
        protocol_handle                   = ethernet_2_handle,
        ipv6_multiplier                   = "1",
        ipv6_resolve_gateway              = "1",
        ipv6_gateway                      = ipv6_gw,
        ipv6_intf_addr                    = ipv6_address_start,
        ipv6_gateway_step                 = "0:0:0:0:0:0:0:0",
        ipv6_prefix_length                = "112",
        ipv6_send_ra                      = "0",
        ipv6_discover_gateway_ip          = "0",
        ipv6_include_ra_prefix            = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        pass

    ipv6_1_handle = _result_['ipv6_handle']

    return ipv4_1_handle,ipv6_1_handle
    

def ixiaHostConfig(port_handle,ipv4_address_start,ipv4_gw,scale,vlan_id,topology_name):
    _result_ = ixiangpf.topology_config(
        topology_name      = topology_name,
        port_handle        = port_handle,
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    topology_2_handle = _result_['topology_handle']
    
    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_2_handle,
        device_group_name            = """Device Group 2""",
        device_group_multiplier      = scale,
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)
    
    deviceGroup_2_handle = _result_['device_group_handle']

    mac_start2 = macGenerator() 
    
    if 'novlan' in vlan_id:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = '0',
            vlan_id_step                 = '0',
            vlan_id_count                = '0',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            ixnHLT_errorHandler('interface_config', _result_)
        
        ethernet_2_handle = _result_['ethernet_handle']
    else:
        _result_ = ixiangpf.interface_config(
            protocol_name                = """Ethernet 2""",
            protocol_handle              = deviceGroup_2_handle,
            mtu                          = "1500",
            src_mac_addr                 = mac_start2,
            vlan                         = 1,
            vlan_id                      = str(vlan_id),
            vlan_id_step                 = '0',
            vlan_id_count                = '1',
        )
        if _result_['status'] != IxiaHlt.SUCCESS:
            ixnHLT_errorHandler('interface_config', _result_)
        
        ethernet_2_handle = _result_['ethernet_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 2""",
        protocol_handle                   = ethernet_2_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        gateway                           =  ipv4_gw,
        gateway_step                      = "0.0.0.0",
        intf_ip_addr                      = ipv4_address_start,
        intf_ip_addr_step                 = "0.0.0.1",
        netmask                           = "255.255.0.0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
    

    ipv4_2_handle = _result_['ipv4_handle']
         
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        arp_on_linkup                       = "0",
        single_arp_per_gateway              = "1",
        ipv4_send_arp_rate                  = "200",
        ipv4_send_arp_interval              = "1000",
        ipv4_send_arp_max_outstanding       = "400",
        ipv4_send_arp_scale_mode            = "port",
        ipv4_attempt_enabled                = "0",
        ipv4_attempt_rate                   = "200",
        ipv4_attempt_interval               = "1000",
        ipv4_attempt_scale_mode             = "port",
        ipv4_diconnect_enabled              = "0",
        ipv4_disconnect_rate                = "200",
        ipv4_disconnect_interval            = "1000",
        ipv4_disconnect_scale_mode          = "port",
        ipv4_re_send_arp_on_link_up         = "true",
        ipv4_permanent_mac_for_gateway      = "false",
        ipv4_gratarp_transmit_count         = "1",
        ipv4_gratarp_transmit_interval      = "3000",
        ipv4_rarp_transmit_count            = "1",
        ipv4_rarp_transmit_interval         = "3000",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
        
    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        ethernet_attempt_enabled            = "0",
        ethernet_attempt_rate               = "200",
        ethernet_attempt_interval           = "1000",
        ethernet_attempt_scale_mode         = "port",
        ethernet_diconnect_enabled          = "0",
        ethernet_disconnect_rate            = "200",
        ethernet_disconnect_interval        = "1000",
        ethernet_disconnect_scale_mode      = "port",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)
    
    return(ipv4_2_handle)  


 
                    

def ixiaTrafficConfig(ipv4_1_handle,ipv4_2_handle):
    #ixnHLT_logger('Resetting traffic...')
    _result_ = ixiahlt.traffic_control(
        action='reset',
        traffic_generator='ixnetwork_540',
        cpdp_convergence_enable='0',
        l1_rate_stats_enable ='1',
        misdirected_per_flow ='0',
        delay_variation_enable='0',
        packet_loss_duration_enable='0',
        latency_enable='1',
        latency_bins='enabled',
        latency_control='store_and_forward',
        instantaneous_stats_enable='0'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_control', _result_)
    #
    # Collect port_handles for traffic_stats
    #
    traffic_stats_ph = set()
    for (k, v) in ixnHLT.items():
        if k.startswith('PORT-HANDLE,'):
            traffic_stats_ph.add(v)
                    
    # 
    #  Configure traffic for all configuration elements
    # 
    #  -- Traffic item//traffic/trafficItem:<1>
    #ixnHLT_logger('Configuring traffic for traffic item: //traffic/trafficItem:<1>')
    
    ti_srcs, ti_dsts = {}, {}
    ti_mcast_rcvr_handle, ti_mcast_rcvr_port_index, ti_mcast_rcvr_host_index, ti_mcast_rcvr_mcast_index = {}, {}, {}, {}
    
    ti_srcs['EndpointSet-1'] = ixnHLT_endpointMatch(ixnHLT, ['//topology:<1>'], 'HANDLE')
    if len(ti_srcs) == 0:
        match_err = {'log': 'Cannot find any src endpoints for EndpointSet-1'}
        ixnHLT_errorHandler('ixnHLT_endpointMatch', match_err)
    
    ti_dsts['EndpointSet-1'] = ixnHLT_endpointMatch(ixnHLT, ['//topology:<2>'], 'HANDLE')
    if len(ti_dsts) == 0:
        match_err = {'log': 'Cannot find any dst endpoints for elem EndpointSet-1'}
        ixnHLT_errorHandler('ixnHLT_endpointMatch', match_err)
    
    
    _result_ = ixiahlt.traffic_config(
        mode='create',
        traffic_generator='ixnetwork_540',
        endpointset_count=1,
        emulation_src_handle=ipv4_1_handle,
        emulation_dst_handle=ipv4_2_handle,
        emulation_multicast_dst_handle=[[]],
        emulation_multicast_dst_handle_type=[[]],
        global_dest_mac_retry_count='1',
        global_dest_mac_retry_delay='5',
        enable_data_integrity='1',
        global_enable_dest_mac_retry='1',
        global_enable_min_frame_size='0',
        global_enable_staggered_transmit='0',
        global_enable_stream_ordering='0',
        global_stream_control='continuous',
        global_stream_control_iterations='1',
        global_large_error_threshhold='2',
        global_enable_mac_change_on_fly='0',
        global_max_traffic_generation_queries='500',
        global_mpls_label_learning_timeout='30',
        global_refresh_learned_info_before_apply='0',
        global_use_tx_rx_sync='1',
        global_wait_time='1',
        global_display_mpls_current_label_value='0',
        global_detect_misdirected_packets='0',
        global_frame_ordering='none',
        global_enable_lag_rebalance_on_port_up='1',
        global_enable_lag_flow_failover_mode='1',
        global_enable_lag_flow_balancing='1',
        global_enable_lag_auto_rate='1',
        frame_sequencing='disable',
        frame_sequencing_mode='rx_threshold',
        src_dest_mesh='one_to_one',
        route_mesh='one_to_one',
        bidirectional='1',
        allow_self_destined='0',
        use_cp_rate='1',
        use_cp_size='1',
        enable_dynamic_mpls_labels='0',
        hosts_per_net='1',
        name='Traffic_Item_1',
        source_filter='all',
        destination_filter='all',
        tag_filter=[[]],
        merge_destinations='0',
        lisp_reloc_ordinal_number='0',
        has_open_flow='0',
        multicast_forwarding_mode='replication',
        evpn_next_hop_ordinal_value='0',
        frer_duplicate_elimination='0',
        num_vlans_for_multicast_replication='1',
        enable_mac_sec_egress_only_autoconfig='1',
        raw_traffic_rx_ports_behavior='replicated',
        circuit_endpoint_type='ipv4',
        pending_operations_timeout='30'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_config', _result_)
    
    #  -- All current config elements
    config_elements = ixiatcl.convert_tcl_list(_result_['traffic_item'])
    
    #  -- Config Element //traffic/trafficItem:<1>/configElement:<1>
    #ixnHLT_logger('Configuring options for config elem: //traffic/trafficItem:<1>/configElement:<1>')
    _result_ = ixiahlt.traffic_config(
        mode='modify',
        traffic_generator='ixnetwork_540',
        stream_id=config_elements[0],
        preamble_size_mode='auto',
        preamble_custom_size='8',
        data_pattern='',
        data_pattern_mode='incr_byte',
        enforce_min_gap='0',
        rate_pps='1000',
        frame_rate_distribution_port='apply_to_all',
        frame_rate_distribution_stream='split_evenly',
        frame_size='512',
        length_mode='fixed',
        tx_mode='advanced',
        transmit_mode='continuous',
        pkts_per_burst='1',
        tx_delay='0',
        tx_delay_unit='bytes',
        number_of_packets_per_stream='1',
        loop_count='1',
        min_gap_bytes='12'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_config', _result_)
    
    #  -- Endpoint set EndpointSet-1
    #ixnHLT_logger('Configuring traffic for config elem: //traffic/trafficItem:<1>/configElement:<1>')
    #ixnHLT_logger('Configuring traffic for endpoint set: EndpointSet-1')
    #  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ethernet-1"
    _result_ = ixiahlt.traffic_config(
        mode='modify_or_insert',
        traffic_generator='ixnetwork_540',
        stream_id=config_elements[0],
        stack_index='1',
        l2_encap='ethernet_ii',
        mac_src_mode='fixed',
        mac_src_tracking='0',
        mac_src='00:00:00:00:00:00'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_config', _result_)
    
    #  -- Stack //traffic/trafficItem:<1>/configElement:<1>/stack:"ipv4-2"
    _result_ = ixiahlt.traffic_config(
        mode='modify_or_insert',
        traffic_generator='ixnetwork_540',
        stream_id=config_elements[0],
        stack_index='2',
        l3_protocol='ipv4',
        qos_type_ixn='tos',
        ip_precedence_mode='fixed',
        ip_precedence='0',
        ip_precedence_tracking='0',
        ip_delay_mode='fixed',
        ip_delay='0',
        ip_delay_tracking='0',
        ip_throughput_mode='fixed',
        ip_throughput='0',
        ip_throughput_tracking='0',
        ip_reliability_mode='fixed',
        ip_reliability='0',
        ip_reliability_tracking='0',
        ip_cost_mode='fixed',
        ip_cost='0',
        ip_cost_tracking='0',
        ip_cu_mode='fixed',
        ip_cu='0',
        ip_cu_tracking='0',
        ip_id_mode='fixed',
        ip_id='0',
        ip_id_tracking='0',
        ip_reserved_mode='fixed',
        ip_reserved='0',
        ip_reserved_tracking='0',
        ip_fragment_mode='fixed',
        ip_fragment='1',
        ip_fragment_tracking='0',
        ip_fragment_last_mode='fixed',
        ip_fragment_last='1',
        ip_fragment_last_tracking='0',
        ip_fragment_offset_mode='fixed',
        ip_fragment_offset='0',
        ip_fragment_offset_tracking='0',
        ip_ttl_mode='fixed',
        ip_ttl='64',
        ip_ttl_tracking='0',
        track_by='none',
        egress_tracking='none'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_config', _result_)
    
    #  -- Post Options
    #ixnHLT_logger('Configuring post options for config elem: //traffic/trafficItem:<1>/configElement:<1>')
    _result_ = ixiahlt.traffic_config(
        mode='modify',
        traffic_generator='ixnetwork_540',
        stream_id=config_elements[0],
        transmit_distribution='none'    
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_#ErrorHandler('traffic_config', _result_)
    
  
    # 
    # Configure traffic for Layer 4-7 AppLibrary Profile
    # 
    
def IxiaTrafficControl(action):
    #if 'run' in action:'run','stop'
    _result_ = ixiahlt.traffic_control(
        action=action,
        traffic_generator='ixnetwork_540',
        type='l23'
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_#ErrorHandler('traffic_control', _result_)
                  
    time.sleep(30)
    
     
    
    _result_ = ixiahlt.test_control(action='stop_all_protocols')
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('ixiahlt::traffic_control', _result_)
                    

def connectIxia(ixia_port_list):
    port_handle_list = ixiaConnect(ixia_port_list)  
    port_handle1 = port_handle_list.split()[0]
    port_handle2 = port_handle_list.split()[1]
    port_handle3 = port_handle_list.split()[2]
    port_handle4 = port_handle_list.split()[3]
    port_handle5 = port_handle_list.split()[4]
    port_handle6 = port_handle_list.split()[5]
    port_handle7 = port_handle_list.split()[6]
    port_handle8 = port_handle_list.split()[7]
    return (port_handle1,port_handle2,port_handle3,port_handle4,port_handle5,port_handle6,port_handle7,port_handle8)

def trafficConfEsgAll(port_handle1,port_handle2,scale,ipv4_address_start1,ipv4_address_start2,vlan_id1,vlan_id2,ipv4_gw1,ipv4_gw2):
    ipv4_gw = '4.5.0.1'
                
    handle1 = ixiaHostConfig(port_handle,ipv4_address_start,ipv4_gw,scale,\
                             vlan_id,vlan_id_step,vlan_id_count,topology_name)
    
    ixiaHostConfig(port_handle1,ipv4_address_start1,ipv4_gw,scale,vlan_id1)
    handle2 = ixiaHostConfig(port_handle2,ipv4_address_start2,ipv4_gw,scale,vlan_id2)
    _result_ = ixiahlt.test_control(action='start_all_protocols')
    countdown(5)
    return handle1,handle2
 

def TrafficGenAll(handle1,handle2,StreamName1,StreamName2): 
    generateTraffic(handle1,handle2,StreamName1)      
    #generateTraffic(handle2,handle1,StreamName2)           
    countdown(1)    





def trafficConfEsg(ixia_port_list,scale,ipv4_address_start1,ipv4_address_start2):
    ipv4_gw = '4.5.0.1'
    #ipv4_address_start1 = '4.5.0.10' 
    #ipv4_address_start2 = '4.5.0.100'                   

    port_handle_list = ixiaConnect(ixia_port_list)  
    port_handle1 = port_handle_list.split()[0]
    port_handle2 = port_handle_list.split()[1]

    handle1 = ixiaHostConfig(port_handle1,ipv4_address_start1,ipv4_gw,scale)
    handle2 = ixiaHostConfig(port_handle2,ipv4_address_start2,ipv4_gw,scale)
    _result_ = ixiahlt.test_control(action='start_all_protocols')
    countdown(5)
    #ixiaTrafficConfig(handle1,handle2)
 
    generateTraffic(handle1,handle2)      
    generateTraffic(handle2,handle1)           
    countdown(5)    
    
def ixiaStatCheck():    
    trafficControll('run')
    countdown(10)
    trafficStats = getTrafficStats()
    tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
    rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
    trafficControll('stop')    
    countdown(2)
    if abs(int(tx)-int(rx)) > 200:
        log.info("Traffic Test failed")  
        return 0
    else:
        log.info("trafficTestEsg pAss")        
        return 1       
    

def ixiaStatCheckRate(rate):    
    trafficControll('run')
    countdown(10)
    trafficStats = getTrafficStats()
    tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
    rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
    log.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    log.info(f"EXPECTED RX rate--------{rate}")
    log.info(f"TX rate--------{tx}")
    log.info(f"RX rate--------{rx}")
    log.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    trafficControll('stop')    
    countdown(2)

    if int(rate) < 1210:
        if int(rx) < 600: 
            return 1        
    if abs(int(rx)-int(rate)) > 1200:    
        log.info("Traffic RX rate Test failed")      
        return 0    
    else:
        log.info("trafficTestEsg pAss")        
        return 1       
    