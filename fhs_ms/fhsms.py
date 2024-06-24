
import logging
from pyats.async_ import pcall
from pyats import aetest
from genie.testbed import load
 
import time
import os
from IxNetwork import IxNet
from ats import aetest, log
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

 
ixiangpf = IxiaNgpf(ixiahlt)
 
#ixLib = ixiaPyats_lib.ixiaPyats_lib()

scale = 1

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    @aetest.subsection
    def connect_to_tb_devices(self, testbed,build=""):
        self.parent.parameters['testbed'] = testbed = load(testbed)

        global scale,ixiangpf,ixLib,leaf_uut_list,uut_list,leaf11,leaf12,leaf21,leaf22,leaf31,spine,sw1,sw2,sw3,conf_dict,l3_device_list,l3_conf_dict,\
            l2_conf_dict,l2_device_list,leaf_conf_dict,tgn1,client_mac_list,dhcp_client1,client_mac_list1,client_topo_handle1,dhcp_client2,client_mac_list2,client_topo_handle2,\
            client_port_hdl1,client_port_hdl2,mac_start1,mac_start2,mac_start3,mac_start4,snoop_list_local_1,snoop_list_local_2,snoop_list_local_3,sw1_svi_mac,sw2_svi_mac,sw3_svi_mac,\
            snoop_mac_list,dhcp_client3,leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris,dci11fx,sw11tetley,sw31neptune

        
        client_mac_list = []


        skip_setup =  False
        image_upgrade = True


        chassisIP='10.197.127.16'
        serverIP='10.197.127.23'

        #CreateDhcpServ(serverIP,chassisIP)
        #dhcpIxiatest()

 

        leaf11fx3 = testbed.devices['leaf11fx3']
        leaf12fx3 = testbed.devices['leaf12fx3']
        leaf13fx3 = testbed.devices['leaf13fx3']
        leaf21fx3 = testbed.devices['leaf21fx3']
        leaf31paris = testbed.devices['leaf31paris']
        spine11fx = testbed.devices['spine11fx']
        bgw11gx = testbed.devices['bgw11gx']
        bgw12gx = testbed.devices['bgw12gx']
        bgw21fx3 = testbed.devices['bgw21fx3']
        bgw31fx3 = testbed.devices['bgw31fx3']
        spine31paris = testbed.devices['spine31paris']
        dci11fx = testbed.devices['dci11fx']
        sw11tetley = testbed.devices['sw11tetley']
        sw31neptune = testbed.devices['sw31neptune']

        leaf_uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris1]
        uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris,dci11fx,sw11tetley,sw31neptune]
        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/fhs/fhsms_topo.yaml'))

        '''

        l3_device_list = [leaf11,leaf12,leaf21,leaf22,leaf31,spine] 
        l3_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        leaf_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        l2_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        l2_device_list = [leaf11,leaf12,leaf21,leaf22,leaf31,sw1,sw2] 

        mac_start1 = macGenerator()
        mac_start2 = macGenerator() 
        mac_start3 = macGenerator() 
        mac_start4 = macGenerator() 
        sw1_svi_mac = macGenerator()
        sw2_svi_mac = macGenerator() 
        sw3_svi_mac = macGenerator()                       
 

        snoop_list_local_1 = [mac_start1,sw1_svi_mac]
        snoop_list_local_2 = [mac_start2,sw2_svi_mac]
        snoop_list_local_3 = [mac_start3,sw3_svi_mac]
        snoop_mac_list = snoop_list_local_1+snoop_list_local_2+snoop_list_local_3

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

    ''' 
    @aetest.subsection
    def vpcGlobalConf(self, testbed):             
        pcall(addVpcConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)

 
    @aetest.subsection
    def l2Conf(self, testbed):  
        #import pdb;pdb.set_trace()
        #configureL2Interface(leaf12,conf_dict)
 
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
        #pcall(hostMoveSetup, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
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
    @aetest.setup
    def setup(self, testbed):
        #pcall(unshutAllintf, uut=tuple(uut_list))
        pass

    @aetest.test   
    def test1(self, testbed): 
        #fhsCliEnable(uut,conf_dict):
        pcall(fhsCliEnable, uut=tuple(leaf_uut_list),conf_dict=(leaf_conf_dict))  

        for uut in leaf_uut_list:
           if not fhsCliCheck(uut):
                import pdb;pdb.set_trace()
                self.failed()
 

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
        #pcall(saveConf, uut=tuple(uut_list))
       
        for uut in leaf_uut_list:
            op = uut.execute("sh run | inc 'ip source bindin'")
            for line in op.splitlines():
                if 'binding' in line:
                    uut.configure(f"no {line}")
                    
        for uut in leaf_uut_list:
            uut.configure("clear ip dhcp snooping binding")

        for uut in leaf_uut_list:
            staticDict = dhcpStaticBinding(uut,conf_dict)
            countdown(6)
            if not checkdhcpBinding(uut,staticDict,leaf_uut_list):
                import pdb;pdb.set_trace()
                self.failed()
 
         
    @aetest.cleanup
    def cleanup(self):
        pass
 


class fhsDinBinding(aetest.Testcase):
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
        #pcall(saveConf, uut=tuple(uut_list))
       
        pcall(dhcpCleanup, uut=tuple(leaf_uut_list))
                    
        for uut in leaf_uut_list:
            uut.configure("clear ip dhcp snooping binding")

        for uut in leaf_uut_list:
            staticDict = dhcpStaticBinding(uut,conf_dict)
            countdown(6)
            if not checkdhcpBinding(uut,staticDict,leaf_uut_list):
                import pdb;pdb.set_trace()
                self.failed()

 
         
    @aetest.cleanup
    def cleanup(self):
        pass
 
        
     

class TC001_ixia_Setup(aetest.Testcase): 
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):

        pcall(dhcpCleanup, uut=tuple(leaf_uut_list))
        #for uut in leaf_uut_list:
        cfg = \
            """
            interface e1/49/1
            ip dhcp snooping trust
            no  ip verify source dhcp-snooping-vlan
            ip arp inspection trust 
            """
        leaf31.configure(cfg)    

        cfg = \
            """
            interface {po}
            switchport trunk allowed vlan {vlan}
            """

        for uut in [sw1]:
            uut.configure(cfg.format(po="Po11",vlan='1005'))

        for uut in [sw1]:
            uut.configure(cfg.format(po="Po12",vlan='none'))

        countdown(10)            

        global dhcp_client1,client_mac_list1,client_topo_handle1,dhcp_client2,client_mac_list2,client_topo_handle2,client_port_hdl1,client_port_hdl2,\
               dhcp_client3,dhcp_client4,client_topo_handle3,client_port_hdl3,client_port_hdl4,client_topo_handle4
        srv_port = '11/4'
        client_port1 = '11/8'
        client_port2 = '11/2'
        #client_port3 = '11/7'
        client_port3 = '11/11'     
      
        #client_port3
        client_port_list = [srv_port,client_port1,client_port2,client_port3]
        
        ##import pdb;pdb.set_trace()

        port_handle = IxiaConnect(client_port_list)

        
        
        ixia_port_list =  " "

        for port in client_port_list:
            ixia_port_list = ixia_port_list+" "+port
            
        #srv_port+" "+client_port1+" "+client_port2+" "+client_port3+" "+client_port4
        ixia_chassis_ip = '10.197.127.16'
        ixia_tcl_server = '10.197.127.23'
        ixia_tcl_port = '8009'
    
        #connect_status = ixiangpf.connect(
        #    reset                  = 1,
        #    device                 = ixia_chassis_ip,
        #    port_list              = ixia_port_list,
        #    ixnetwork_tcl_server   = ixia_tcl_server,
        #    tcl_server             = ixia_chassis_ip,
        #)
        #if connect_status['status'] != IxiaHlt.SUCCESS:
        #    ixnHLT_errorHandler('connect', connect_status)

        connect_status =  IxiaConnect(client_port_list)

        port_handle = connect_status['ixia_port_list']

        
        #IxiaConnect(client_port_list):

        ##import pdb;pdb.set_trace()


        srv_port_hdl = port_handle.split(' ')[0]
        client_port_hdl1 = port_handle.split(' ')[1]
        client_port_hdl2 = port_handle.split(' ')[2]
        client_port_hdl3 = port_handle.split(' ')[3]       
        #client_port_hdl4 = port_handle.split(' ')[4]     
        dhcp_server = dhcpServerSetup(srv_port_hdl)

        c1_top_stat,dhcp_client1,client_topo_handle1 = dhcpClientSetup(client_port_hdl1,mac_start1)
        c2_top_stat,dhcp_client2,client_topo_handle2 = dhcpClientSetup(client_port_hdl2,mac_start2)
        c2_top_stat,dhcp_client3,client_topo_handle3 = dhcpClientSetup(client_port_hdl3,mac_start3)
        #c2_top_stat,dhcp_client4,client_topo_handle4 = dhcpClientSetup(client_port_hdl4,mac_start4)

        for sw,mac in zip([sw1,sw2],[sw1_svi_mac,sw2_svi_mac]):
            accessSWSviConf(sw,mac)



        countdown(40)

        dhcpClientTrafficl(client_topo_handle3,client_topo_handle1)
        dhcpClientTrafficl(client_topo_handle1,client_topo_handle3)

        countdown(10)  

    @aetest.test   
    def test1_sviDhcp(self, testbed): 
        countdown(80)
        #for port_handle,dhcp_client in zip([client_port_hdl1,client_port_hdl2],[dhcp_client1,dhcp_client2]):
        for uut in [sw1,sw2]:
            if not find_svi_ip(uut,'1005'):
                import pdb;pdb.set_trace()
                self.failed()


    @aetest.test   
    def test1_binding(self, testbed): 
        #for port_handle,dhcp_client in zip([client_port_hdl1,client_port_hdl2],[dhcp_client1,dhcp_client2]):
        for port_handle in [client_port_hdl3,client_port_hdl2,client_port_hdl1]:        
            if not checkClientBindingStatsIxia(port_handle):
                import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
       
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            import pdb;pdb.set_trace()
            self.failed()
                                                

        ##import pdb;pdb.set_trace()


    @aetest.cleanup
    def cleanup(self):
        pass
 



class dai_Ipsg(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def daiIpsgart(self, testscript, testbed):
        
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            import pdb;pdb.set_trace()
            self.failed()
        


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
        ProcessRestart(leaf11,'bgp')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()




    @aetest.cleanup
    def cleanup(self):
        pass



class TC008_dhcp_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def bgpRestart(self, testscript, testbed):
        ProcessRestart(leaf11,'dhcp_snoop')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()




    @aetest.cleanup
    def cleanup(self):
        pass




class TC008_l2fm_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def Restart(self, testscript, testbed):
        ProcessRestart(leaf31,'l2fm')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()



    @aetest.cleanup
    def cleanup(self):
        pass



class TC008_l2rib_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def Restart(self, testscript, testbed):
        ProcessRestart(leaf31,'l2rib')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()



    @aetest.cleanup
    def cleanup(self):
        pass

 


class TC008_adjmgr_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def Restart(self, testscript, testbed):
        ProcessRestart(leaf21,'adjmgr')
        ProcessRestart(leaf22,'adjmgr')
        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()



    @aetest.cleanup
    def cleanup(self):
        pass


class TC008_arp_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def Restart(self, testscript, testbed):
        ProcessRestart(leaf21,'arp')
        ProcessRestart(leaf22,'arp')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()



    @aetest.cleanup
    def cleanup(self):
        pass

 


class TC008_hmm_restart(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def Restart(self, testscript, testbed):
        ProcessRestart(leaf31,'hmm')

        countdown(40)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass


class TC009_dhcp_remove_add(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def dhscprestart(self, testscript, testbed):
        #conf1 = leaf11.configure("show run dhcp")
        #countdown(10)
        
        conf2 = leaf11.configure("no feature dhcp")

        countdown(10)
        fhsCliEnable(leaf11,conf_dict)

        countdown(30)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass



class TC010_conf_replace(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def dhscprestart(self, testscript, testbed):
        #conf1 = leaf11.configure("show run dhcp")
        #countdown(10)
        for uut in [leaf11,leaf21]:
            uut.execute('copy run bootflash:fhs100 ')
        for uut in [leaf11,leaf21]:            
            uut.configure("no feature dhcp")

        countdown(10)

        for uut in [leaf11,leaf21]:
            uut.execute('configure replace bootflash:fhs100 ')

        #fhsCliEnable(leaf11,conf_dict)

        countdown(30)

        for mac in client_mac_list:
            for leaf in leaf_uut_list:
                checksnoopBinding(leaf,mac)

    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                #import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            #import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            #import pdb;pdb.set_trace()
            self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass




class clear_Bind(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def clearBind(self, testscript, testbed):
        
        if not clearIpDhcpBinding(leaf11,sw1):
            self.failed()
        

    @aetest.cleanup
    def cleanup(self):
        pass
 

class TC008_mac_move_vpcleaf1_to_vpcLeaf2(aetest.Testcase): 
   ###    This is description for my tecase two

    @aetest.setup
    def move1(self, testscript, testbed):

        #00:00:00:51:19:c4  4.5.0.10         85926     dhcp-snoop  1005  port-channel11  

        ip2 = find_svi_ip(sw1,'1005')

        op1 = leaf11.execute("sh ip dh sn binding")
        for line in op1.splitlines():
            if not ip2 in line:
                if 'port-channel11' in line:
                    ip1 = line.split()[1]

        cfg = \
        """
        interface {po}
         switchport trunk allowed vlan {vlan}
        """

        for uut in [sw1]:
            uut.configure(cfg.format(po="Po11",vlan='none'))    
   
        for uut in [sw1]:
            uut.configure(cfg.format(po="Po12",vlan='1005')) 

        countdown(10)   

        #dhcpClientControll(dhcp_client3,'bind')

        leaf21.execute(f"ping {ip1}")
        leaf22.execute(f"ping {ip1}")


        countdown(10)   


        for uut in [leaf21,leaf22]:
            op1 = uut.execute("sh ip dh sn binding")
            for line in op1.splitlines():
                if ip1 in line:
                    if 'nve' in line:
                        self.failed()

        #control_status = ixiangpf.emulation_dhcp_control(
        #    handle 			=	dhcp_client3,
        #    ping_destination = '4.5.0.1',
        #    action = 'send_ping',
        #)
        #if control_status['status'] != IxiaHlt.SUCCESS:
        #    ixnHLT_errorHandler('emulation_dhcp_control', control_status)
            

 


    @aetest.test   
    def test1_binding(self, testbed): 

        ##import pdb;pdb.set_trace()

        for port_handle in [client_port_hdl3,client_port_hdl4,client_port_hdl2,client_port_hdl3]:        
            if not checkClientBindingStatsIxia(port_handle):
                import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def test2_stats(self, testbed): 
        #for mac in snoop_mac_list:
        for leaf in leaf_uut_list:
            if not checksnoopBinding(leaf,snoop_mac_list):
                import pdb;pdb.set_trace()
                self.failed()              

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in leaf_uut_list:
            if not checkCore(uut):
                import pdb;pdb.set_trace()
                self.failed()
    @aetest.test   
    def test3_traffic(self, testbed): 
        trafficControll('run')
        countdown(30)
    
        trafficStats = getTrafficStats()
        tx = trafficStats['aggregate']['tx']['total_pkt_rate']['sum']
        rx = trafficStats['aggregate']['rx']['total_pkt_rate']['sum']
        if abs(int(tx)-int(rx)) > 200:
            import pdb;pdb.set_trace()
            self.failed()
                                    
    @aetest.test   
    def test4_daiIpsg(self, testbed): 
        if not  ipsgDaiCheck(sw1,sw1_svi_mac):
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.cleanup
    def cleanup(self):
        cfg = \
        """
        interface {po}
         switchport trunk allowed vlan {vlan}
        """

        for uut in [sw1]:
            uut.configure(cfg.format(po="Po11",vlan='1005'))    
   
        for uut in [sw1]:
            uut.configure(cfg.format(po="Po12",vlan='none')) 

 
 
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








 
 