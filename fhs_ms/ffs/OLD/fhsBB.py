
import logging
from pyats.async_ import pcall
from pyats import aetest
from genie.testbed import load
 
import time
import os
from IxNetwork import IxNet

from pexpect import pxssh
import getpass
import pdb
from ipaddress import *
import sys
import random
import genie
import yaml
from genie.libs.conf.ospf import Ospf
 
import unittest
from unittest.mock import Mock
from fhs_lib import *

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# Genie Conf
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.interface import Interface
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.gracefulrestart import GracefulRestart
from genie.libs.conf.ospf.stubrouter import StubRouter
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.ospf.arearange import AreaRange
from genie.libs.conf.ospf.interfacestaticneighbor import InterfaceStaticNeighbor
from unicon.utils import Utils
logger = logging.getLogger(__name__)
 

from unicon.eal.dialogs import Statement, Dialog
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

 
 

 
#from paramiko import SSHClient
#from paramiko import AutoAddPolicy
import os
import socket
import warnings,time

#from cryptography.utils import CryptographyDeprecationWarning
 
#import Python packages
import time
import os
from IxNetwork import IxNet
 
firewall_mode = 'transparent'
dip = '200.1.1.2'


 
import ixiaPyats_lib


from ixia_dhcp_lib import *

 

 
#ixLib = ixiaPyats_lib.ixiaPyats_lib()



class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    @aetest.subsection
    def connect_to_tb_devices(self, testbed,build=""):
        self.parent.parameters['testbed'] = testbed = load(testbed)

        global ixLib,leaf_uut_list,uut_list,leaf11,leaf12,leaf21,leaf22,leaf31,spine,sw1,sw2,sw3,conf_dict,l3_device_list,l3_conf_dict,\
            l2_conf_dict,l2_device_list,leaf_conf_dict,tgn1


        skip_setup =  False
        image_upgrade = True


        chassisIP='10.197.127.16'
        serverIP='10.197.127.23'

        #CreateDhcpServ(serverIP,chassisIP)
        #dhcpIxiatest()



        #(Pdb) kk = tgn1.ixia_port_list
        #(Pdb) kk
        #['1/11/7', '1/11/8', '1/11/4', '1/11/1', '1/11/2', '1/11/8', '1/11/11']

        """
        assign_ixia_ports
        export_packet_capture_file
        generate_export_quicktest_report
        get_ixia_virtual_port
        get_ixia_virtual_port_attribute
        get_ixia_virtual_port_capture
        ixia_port_list
        ixnetwork_tcl_port
        set_ixia_virtual_ports
        short_interface_name
        virtual_ports
        >>> for i in kk:
        ...     if  'dhc' in i:
        ...         print(i)
        ...
        add_dhcpv4_emulator_client
        add_dhcpv6_emulator_client
        clear_dhcp_emulator_clients
        configure_dhcpv4_reply
        configure_dhcpv4_request
        configure_dhcpv6_reply
        configure_dhcpv6_request
        get_dhcp_binding
        get_dhcpv4_binding_address
        get_dhcpv6_binding_address
        verify_dhcp_client_binding
        """
        #import pdb; pdb.set_trace()

        #tgn1.ixia_port_list

        #ixia_port_list: ['1/11/7', '1/11/8','1/11/4', '1/11/1','1/11/2', '1/11/8','1/11/11']

        leaf11 = testbed.devices['fx301']
        leaf12 = testbed.devices['fx302'] 
        leaf21 = testbed.devices['gx01']
        leaf22 = testbed.devices['gx02']     
        leaf31 = testbed.devices['fx303']               
        spine = testbed.devices['fx01']
        sw1 = testbed.devices['Tetly1']     
        sw2 = testbed.devices['fx02']               
        sw3 = testbed.devices['t2p1']    

        leaf_uut_list=[leaf11,leaf12,leaf21,leaf22,leaf31]
        uut_list=[leaf11,leaf12,leaf21,leaf22,leaf31,spine,sw1,sw2,sw3]
        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/fhs/fhs_topo.yaml'))

        l3_device_list = [leaf11,leaf12,leaf21,leaf22,leaf31,spine] 
        l3_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        leaf_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        l2_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        l2_device_list = [leaf11,leaf12,leaf21,leaf22,leaf31,sw1,sw2,sw3] 


''' 
       
    @aetest.subsection
    def connect(self, testscript, testbed):
        for uut in uut_list:   
            #log.info('connect to %s' % uut.alias)
            try:
                uut.connect()
   
            except:
                #log.info('connect failed once ; clearing console'))
                if 'port' in uut.connections['a']:
                    ts = str(uut.connections['a']['ip'])
                    port=str(uut.connections['a']['port'])[-2:]
                    u = Utils()
                    u.clear_line(ts, port, 'lab', 'lab')
                    #clearConsole(ts,[port])
                try:
                    uut.connect()
                except:
                    self.failed(goto=['common_cleanup'])
            if not hasattr(uut, 'execute'):
                self.failed(goto=['common_cleanup'])
            if uut.execute != uut.connectionmgr.default.execute:
                self.failed(goto=['common_cleanup'])

 
 
    @aetest.subsection
    def cleanup(self, testbed):                 
        pcall(preSetupVxlan, uut=tuple(uut_list))

 
    @aetest.subsection
    def vpcGlobalConf(self, testbed):             
        pcall(addVpcConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)

 
    @aetest.subsection
    def l2Conf(self, testbed):  
        pcall(configureL2Interface, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)

 

    @aetest.subsection
    def LoopIntfBringup(self, testbed):    
        pcall(configureLoopInterface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
    @aetest.subsection
    def l3IntfBringup(self, testbed): 
        pcall(configureL3Interface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
    @aetest.subsection
    def igpConf(self, testbed):  
        pcall(addOspfConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
    @aetest.subsection
    def PimConf(self, testbed):  
        pcall(pimConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict) 

    @aetest.subsection
    def bgpConf(self, testbed):   
        pcall(leafConfig, leaf=tuple(leaf_uut_list))  
        spineBgpConf(spine)
        #countdown(120)

    @aetest.subsection
    def vxlanConf(self, testbed):   
        pcall(configVxlanLeaf, uut=tuple(leaf_uut_list),conf_dict=(leaf_conf_dict))  


    @aetest.subsection
    def checkl2l3vxlan(self, testbed): 
        pcall(saveConf, uut=tuple(uut_list))


    @aetest.subsection
    def hostMoveSetupuut(self, testbed): 
        pcall(configureL2Interface, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
        pcall(hostMoveSetup, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
        pcall(saveConf, uut=tuple(uut_list))

        pcall(clearMac, uut=tuple(uut_list))
       
    #######################################################################
    ###                  testCASE BLOCK                                 ###
    #######################################################################
    # Test 1 :  Check Tables , Configs
    # test 2 : Traffic
    # Test 3 : Test SNMP polling 
    # Test 4 : Test failover
    # Test 5 : Test Reload
    # Test 6 : Test Link Flap
    # Test 7 : Test Remove add config
    # Test 8 : Test config replace
    # Verify stats/ Counters in each case
    
 





class enable_fhs_cli(aetest.Testcase):
    """
    1	FHS Cli Verification	"	
    1) Bring up the topology with - 
        Spiene & Leaf topology with 3 leaves
        DHCP Server is connected to leaf3 and hosts are connected to all the leaf switches
        Leaf 1 & 2 are vPC nodes with pMCT
        OSPF for underlay
        Multicast replication        
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
    """
    @aetest.setup
    def setup(self, testbed):
        #pcall(unshutAllintf, uut=tuple(uut_list))
        pass

    @aetest.test   
    def test1(self, testbed): 
        #fhsCliEnable(uut,conf_dict):
        pcall(fhsCliEnable, uut=tuple(leaf_uut_list),conf_dict=(leaf_conf_dict))  
 

    @aetest.cleanup
    def cleanup(self):
        pass

 
 

class fhsStaticBinding(aetest.Testcase):
    """
    ip source binding 4.1.1.8 0000.4118.4118 vlan 1001 interface Ethernet1/8
    """
    @aetest.setup
    def setup(self, testbed):
        pass
        
    @aetest.test   
    def test1(self, testbed): 
        #fhsCliEnable(uut,conf_dict):
        #pcall(dhcpStaticBinding, uut=tuple(leaf_uut_list),conf_dict=(leaf_conf_dict)) 
        for uut in [leaf11,leaf21,leaf31]:
            #dhcpStaticBinding(uut,conf_dict)
            pass
        pcall(saveConf, uut=tuple(uut_list))
       
         

    @aetest.cleanup
    def cleanup(self):
        pass

 

class addDHCpServer(aetest.Testcase):
    """
    ip source binding 4.1.1.8 0000.4118.4118 vlan 1001 interface Ethernet1/8
    """
    @aetest.setup
    def setup(self, testbed):
        pass
        
    @aetest.test   
    def test1(self, testbed): 
        #fhsCliEnable(uut,conf_dict):
        #pcall(dhcpStaticBinding, uut=tuple(leaf_uut_list),conf_dict=(leaf_conf_dict)) 

        cfg = \
            """
            interface e1/47
            ip dhcp snooping trust
            """
        leaf11.configure(cfg)    
 
        pcall(saveConf, uut=tuple(uut_list))
       
         

    @aetest.cleanup
    def cleanup(self):
        pass


class TC008_bgp_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def bgpRestart(self, testscript, testbed):
        pass

    @aetest.cleanup
    def cleanup(self):
        pass
'''

class ixiatest(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        pass
        
    @aetest.test   
    def test1(self, testbed): 


 


        srv_port = '11/7'
        client_port1 = '11/2'
        client_port2 = '11/1'
        client_port3 = '11/8'
        client_port4 = '11/4'     



        IxiaDhcpBringup(srv_port,client_port1,client_port2,client_port3,client_port4)

        #import pdb;pdb.set_trace()
        '''
        port_list =    [client_port1,client_port2,client_port3,client_port4]

        port_hdl_dict= ixiaDHCPConnect(ixLib,srv_port,client_port1,client_port2,client_port3,client_port4)  
        result = ixiaDHCPServer(ixLib,port_hdl_dict['phl_srv'] )
        
        dhcpv4server_handle = result['dhcpv4server_handle']  
        ixLib.startDHCPServer(dhcpv4server_handle)

        #status = ixLib.emulation_dhcp_server_control(
        #    dhcp_handle     = dhcpv4server_handle,
        #    action          = 'collect',
        #)

        #for port in port_list:
            #client_hdl = port_hdl_dict[port]
        #    result = ixiaDHCPClient(ixLib,client_hdl)  

        for client_hdl in  [port_hdl_dict['phl_client1'],port_hdl_dict['phl_client2'],port_hdl_dict['phl_client3'],port_hdl_dict['phl_client4']]:
            result = ixiaDHCPClient(ixLib,client_hdl)  
            #dhcpv4client_handle = result['dhcpv4client_handle']  

            #status = ixLib.emulation_dhcp_control(
            #    handle          = dhcpv4client_handle,
            #    action          = action,
            #)
            dhcpv4client_handle =  result['dhcpv4client_handle']
            ixLib.start_topology_protocols(dhcpv4client_handle)
            kk = ixLib.bindDHCPClient(dhcpv4client_handle, "bind")
            
        import pdb;pdb.set_trace()

        #_result = ixLib.test_control(action='stop_all_protocols')
        #_result = ixLib.test_control(action='start_all_protocols')

        '''
    @aetest.cleanup
    def cleanup(self):
        pass


class common_cleanup(aetest.CommonCleanup):

    @aetest.subsection
    def stop_tgn_streams(self):
        pass
    #if __name__ == '__main__':  # pragma: no cover
    #    aetest.main()
 
if __name__ == '__main__': # pragma: no cover
    import argparse 
    import json
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--build', dest = 'build', required=True)
    #args = parser.parse_known_args()[0]
    #print("Args %s" % args)
    #aetest.main(build = args.build)


 

#iperf -c 172.16.1.2 -bidir  -M 500 -t 10000 -P 100 -N

   

