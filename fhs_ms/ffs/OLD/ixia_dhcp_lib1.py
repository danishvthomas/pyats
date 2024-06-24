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


try:
	ixnHLT_errorHandler('', {})
except (NameError,):
	def ixnHLT_errorHandler(cmd, retval):
		global ixiatcl
		err = ixiatcl.tcl_error_info()
		log = retval['log']
		additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
		raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

        
def ixDHCP(srv_port,client_port1,client_port2,client_port3,client_port4):

    import pdb;pdb.set_trace()

    ixia_port_list =  srv_port+" "+client_port1+" "+client_port2+" "+client_port3+" "+client_port4
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
    srv_port_hdl = port_handle.split(' ')[0]
    port_1 = port_handle.split(' ')[1]
    port_2 = port_handle.split(' ')[2]
    port_3 = port_handle.split(' ')[3]
    client_port_hdl = port_handle.split(' ')[4]
 
    topology_status = ixiangpf.topology_config(
        topology_name            =	"DHCPv4 Server",
        port_handle              =	srv_port_hdl,
        device_group_multiplier  =	 	'1',
    )
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)


    deviceGroup_second_handle = topology_status['device_group_handle']
    top_handle = topology_status['topology_handle']
    top_2 = topology_status['topology_handle']
 

    mac = macGenerator()    

    dhcp_status = ixiangpf.emulation_dhcp_server_config(
            handle				=	deviceGroup_second_handle              ,
            count				=	'5'			                            ,
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

    dhcp_server = dhcp_status['dhcpv4server_handle']


    #print "Starting dhcp server...."
    control_status = ixiangpf.emulation_dhcp_server_control(
        dhcp_handle = 			dhcp_server 		                           ,
        action = 'collect'								                           ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_server_control', control_status)



    topology_status = ixiangpf.topology_config(
        topology_name           =   "DHCPv4 Client"+client_port_hdl  ,
        port_handle             =   client_port_hdl                             ,
        device_group_multiplier =    '10'                                 ,
    )
    if topology_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', topology_status)


    deviceGroup_first_handle = topology_status ['device_group_handle']
    top_1 = topology_status['topology_handle']


    mac1 = macGenerator()   

    while mac1 == mac:
        mac1 = macGenerator()    


    dhcp_client_dict = {
        'topo_device_handle'        : topo_hndl1,
        'num_of_sessions'           : "10",
        'vlan'                      : "0",
        'vlan_id_step'              : "0",
        'circuit_type'              : "ipv4",
    }

    dhcp_status = ixiangpf.emulation_dhcp_group_config(
            handle                         = deviceGroup_first_handle,
            protocol_name 		            = "Dhcp_client"+client_port_hdl,
            mac_addr                       = mac1,
            mac_addr_step		            = '00.00.00.00.00.02',
            #use_rapid_commit               = '0',
            enable_stateless               = '0',
            num_sessions                   = "10",
            vlan_id		                = "0",
            vlan_id_step		            = '0',
            #vlan_user_priority		        = '2',
            #dhcp4_broadcast                = args_dict['bcast_flag'],
            dhcp_range_use_first_server    = '1',
            dhcp_range_renew_timer         = '20',
            dhcp_range_ip_type             = 'ipv4',
            vendor_id                      = 'any',
    )

    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_group_config', dhcp_status)
 



    dhcp_client = dhcp_status['dhcpv4client_handle']


    control_status = ixiangpf.emulation_dhcp_control(
        handle 			=	dhcp_client                            ,
        action = 'bind'						                            ,
    )
    if control_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_control', control_status)

    time.sleep(30)


    '''
    #dhcp_status = ixiangpf.emulation_dhcp_group_config(
        handle      =  deviceGroup_first_handle                         ,
        protocol_name 		=		"Dhcp_client"                     ,
        mac_addr  =  mac1                                      ,
        mac_addr_step		=		'00.00.00.00.00.02'	                  ,
        use_rapid_commit = '0'                                              ,
        enable_stateless = '0'                                              ,
        num_sessions     =  '30'                                           ,
        vlan_id		=				'0'			                      ,
        vlan_id_step		=			'0'			                      ,
        vlan_user_priority		=		'2'			                  ,
        dhcp4_broadcast   = '1'                                            ,
        dhcp_range_use_first_server = '1'                                   ,
        dhcp_range_renew_timer = '20'                                       ,
        dhcp_range_ip_type       =      'ipv4'                             ,
        vendor_id                =          'any'                          ,
    )
    if dhcp_status['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_dhcp_group_config', dhcp_status)

    ''' 
    '''

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

    '''        
    #print "Starting dhcp client...."




    # status = ixiangpf.emulation_dhcp_control(
    #    handle          = dhcp_client,
    #    action          = 'bind',
    #)

    #import pdb ; pdb.set_trace()








def ixiaDHCPConnect(ixLib,srv_port,client_port1,client_port2,client_port3,client_port4):     
    ixia_port_list =  srv_port+" "+client_port1+" "+client_port2+" "+client_port3+" "+client_port4
    ixia_chassis_ip = '10.197.127.16'
    ixia_tcl_server = '10.197.127.23'
    ixia_tcl_port = '8009'
 
    ixiaArgDict = {
                    'chassis_ip'    : ixia_chassis_ip,
                    'port_list'     : ixia_port_list,
                    'tcl_server'    : ixia_tcl_server,
                    'tcl_port'      : ixia_tcl_port
    }

    log.info("Ixia Args Dict is:")
    log.info(ixiaArgDict)

    result = ixLib.connect_to_ixia(ixiaArgDict)
    if result == 0:
        log.debug("Connecting to ixia failed")
        #errored("Connecting to ixia failed", goto=['next_tc'])
 
    ch_key = result['port_handle']
    for ch_p in ixia_chassis_ip.split('.'):
        ch_key = ch_key[ch_p]

    log.info("Port Handles are:")
    log.info(ch_key)
    port_hdl_dict = {}
    port_hdl_list = []
    #for port in ixia_port_list .split():
    phl_srv = result['port_handle']['10']['197']['127']['16'] [srv_port]
    phl_client1 = result['port_handle']['10']['197']['127']['16'] [client_port1]
    phl_client2 = result['port_handle']['10']['197']['127']['16'] [client_port2]
    phl_client3 = result['port_handle']['10']['197']['127']['16'] [client_port3]
    phl_client4 = result['port_handle']['10']['197']['127']['16'] [client_port4]
    

    port_hdl_list = [phl_srv,phl_client1,phl_client2]

    port_hdl_dict['phl_srv'] = phl_srv
    port_hdl_dict['phl_client1'] = phl_client1    
    port_hdl_dict['phl_client2'] = phl_client2
    port_hdl_dict['phl_client3'] = phl_client3    
    port_hdl_dict['phl_client4'] = phl_client4


    return(port_hdl_dict)

def ixiaDHCPServer(ixLib,srv_port_hdl):   

    TOPO_1_dict = { 'topology_name'      : 'DHCPServ',
                    'device_grp_name'    : 'DHCPServ',
                    'port_handle'        : srv_port_hdl}


    result1 = ixLib.create_topo_device_grp(TOPO_1_dict) 
    topo_hndl1 = result1['topo_hndl']

    args_dict = {
                    'topology_handle'      : topo_hndl1,
                    'router_addr'      : '4.5.0.10',
                    'router_addr_gw'       : '4.5.0.1',
                    'vlan'    : "0",
                    'pool_count'      : "1",
                    'lease_pool_step'       : "0.0.0.1",
                    'lease_pool_start' : '4.5.0.100',
                    'lease_pool_addr_count'   : '100',
                    'lease_pool_prfx_len'  : '16',
                }

    result2 = ixLib.emulate_dhcp_server(args_dict)

    return result2
 

def ixiaDHCPClient(ixLib,client_hdl):   
    """ Configure DHCP Client in IXIA """   
    #import pdb;pdb.set_trace() 
   
    #topology_name = 'DHCPclient'+str(random.randint(100,199))
    topology_name='DHCPclient'+client_hdl

    TOPO_1_dict = { 'topology_name'      : topology_name,
                    'device_grp_name'    : topology_name,
                    'port_handle'        : client_hdl}

    #import pdb;pdb.set_trace()
    result1 = ixLib.create_topo_device_grp(TOPO_1_dict) 
    topo_hndl1 = result1['topo_hndl']
  

    dhcp_client_dict = {
        'topo_device_handle'        : topo_hndl1,
        'num_of_sessions'           : "10",
        'vlan'                      : "0",
        'vlan_id_step'              : "0",
        'circuit_type'              : "ipv4",
    }
    
    DHCP_client_emul = ixLib.emulate_dhcp_client(dhcp_client_dict)
 
    return(DHCP_client_emul)
    log.info(DHCP_client_emul)