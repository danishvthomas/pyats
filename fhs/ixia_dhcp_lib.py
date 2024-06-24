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
try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)


def IxiaConnect(client_port_list):
    ##import pdb;pdb.set_trace()    
    
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


    port_handle = IxiaConnect(port_list)    

 
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
    import pdb;pdb.set_trace()  

    dhcp_server = dhcpServerBringUp(server_port_hdl,1)

    #import pdb;pdb.set_trace()    
    
    import pdb;pdb.set_trace()  
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

    import pdb;pdb.set_trace()
    
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
    import pdb;pdb.set_trace()    
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
    import pdb;pdb.set_trace()    
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
    import pdb;pdb.set_trace()    
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
    import pdb;pdb.set_trace()    
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
    import pdb;pdb.set_trace()    
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

    import pdb;pdb.set_trace()

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
    import pdb;pdb.set_trace()
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
    import pdb;pdb.set_trace()
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



     
chassis = ['10.197.127.16']
tcl_server = '10.197.127.16'
port_list = [['12/6', '12/13', '12/1', '12/2', '12/7', '12/11', '12/4']]
vport_name_list = [['1/12/6', '1/12/13', '1/12/1', '1/12/2', '1/12/7', '1/12/11', '1/12/4']]
aggregation_mode = [['normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal']]
aggregation_resource_mode = [['normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal']]
guard_rail = 'none'
 


def dhcpTest100(port_list,server_port):
    scale = 1
    log.info(" ====== START dhcpTest100  ====== ")

    port_list.remove(server_port)
    port_list.insert(0, server_port)


    port_handle = IxiaConnect(port_list)    

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


