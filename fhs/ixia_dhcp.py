#!/usr/bin/env python

# python
import logging
import unittest
from unittest.mock import Mock
from randmac import RandMac
import macaddress
            
import time
import os
from IxNetwork import IxNet


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

from fhs_lib import *
import sys
import os
 

import sys, os
import time, re

# Append paths to python APIs

# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python') 
# sys.path.append('/path/to/ixnetwork/api/python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

ixiatcl = IxiaTcl()
ixiahlt = IxiaHlt(ixiatcl)
ixiangpf = IxiaNgpf(ixiahlt)

try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

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

 
 


def dhcpTest(port_list,server_port): 

    mac_start1 = macGenerator()
    mac_start2 = macGenerator() 
    mac_start3 = macGenerator() 
    mac_start4 = macGenerator() 
    mac_start5 = macGenerator() 
    mac_start6 = macGenerator()   

    port_list.remove(server_port)
    port_list.insert(0, server_port)


    port_handle = IxiaConnect(port_list)    

 
    countdown(20)
    ##import pdb;pdb.set_trace()            
    server_port_hdl = port_handle.split(' ')[0]
    client_port_hdl1 = port_handle.split(' ')[1]
    client_port_hdl2 = port_handle.split(' ')[2]
    client_port_hdl3 = port_handle.split(' ')[3]       
    client_port_hdl4 = port_handle.split(' ')[4]      
    client_port_hdl5 = port_handle.split(' ')[5] 


    import pdb;pdb.set_trace()

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



 