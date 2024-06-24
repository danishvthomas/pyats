
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

        global scale,ixiangpf,ixLib,leaf_uut_list,uut_list,leaf11fx3,leaf12,leaf12fx3,leaf12fx3,leaf13fx3,spine,sw11tetley,sw2,sw3,conf_dict,l3_device_list,l3_conf_dict,\
            l2_conf_dict,l2_device_list,tgn1,client_mac_list,dhcp_client1,client_mac_list1,client_topo_handle1,dhcp_client2,client_mac_list2,client_topo_handle2,\
            client_port_hdl1,client_port_hdl2,mac_start1,mac_start2,mac_start3,mac_start4,mac_start5,mac_start6,snoop_list_local_1,snoop_list_local_2,snoop_list_local_3,sw1_svi_mac,sw2_svi_mac,sw3_svi_mac,\
            snoop_mac_list,dhcp_client3,leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris,dci11fx,sw11tetley,sw31neptune,vpc_device_list,\
            vpc_conf_dict,site_1_uut_list,site_2_uut_list,site_3_uut_list,vxlan_uut_list,vxlan_conf_dict,dci_device_list,dci_conf_dict,\
            bgw_device_list,bgw_conf_dict,fhs_uut_list,fhc_conf_dict,sw1_port,sw2_port,leaf11_port1,leaf12_port1,leaf13_port1,leaf21_port1,sw1_port_hdl,sw2_port_hdl,\
            leaf11_port_hdl,leaf12_port_hdl,leaf13_port_hdl,leaf21_port_hdl,dhcp_client1,client_mac_list1,client_topo_handle1,dhcp_client2,client_mac_list2,client_topo_handle2,client_port_hdl1,client_port_hdl2,\
            dhcp_client3,dhcp_client4,client_topo_handle3,client_port_hdl3,client_port_hdl4,client_topo_handle4,sw1_port,sw2_port,leaf11_port1,leaf12_port1,leaf13_port1,leaf21_port1,\
            sw1_port_hdl,sw2_port_hdl,leaf11_port_hdl,leaf12_port_hdl,leaf13_port_hdl,leaf21_port_hdl,port_list,sw1_port_hdl,sw2_port_hdl,leaf11_port_hdl,leaf12_port_hdl,leaf21_port_hdl,server_port,bgw31_port1,\
            port_list_msite1
        
        
        sw1_port = '12/13'
        sw2_port = '12/1'     
        leaf11_port1 = '12/6'
        leaf12_port1 = '12/2'
        leaf13_port1 = '12/7'
        leaf21_port1 = '12/11'
        bgw31_port1 = '12/4'

        port_list = [sw1_port,sw2_port,leaf11_port1,leaf12_port1,leaf13_port1,leaf21_port1,bgw31_port1]
        port_list_msite1 = [sw1_port,sw2_port,leaf11_port1,bgw31_port1,leaf13_port1,leaf21_port1]

        #port_list = [sw1_port,sw2_port,leaf11_port1,leaf12_port1,leaf13_port1,leaf21_port1]
        
        client_mac_list = []


        skip_setup =  False
        image_upgrade = True

        #CreateDhcpServ(serverIP,chassisIP)
        #dhcpIxiatest()

        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/fhs/fhsms_topo2.yaml')) 

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

        site_1_uut_list = [leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx,spine11fx]
        site_2_uut_list = [leaf21fx3,bgw21fx3]
        site_3_uut_list = [bgw31fx3,spine31paris,leaf31paris]

        vxlan_uut_list = [leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx,leaf21fx3,bgw21fx3,bgw31fx3,leaf31paris]
        vxlan_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)


        leaf_uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris]
        uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris,dci11fx,sw11tetley,sw31neptune]


        vpc_device_list = [leaf11fx3,leaf12fx3] 
        vpc_conf_dict = (conf_dict,conf_dict)

        l2_device_list= (leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,sw11tetley,sw31neptune)
        l2_conf_dict = [conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict] 

        l3_device_list = [leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris] 
        l3_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)

        dci_device_list = [bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,dci11fx]
        dci_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)

        bgw_device_list = [bgw11gx,bgw12gx,bgw21fx3,bgw31fx3]
        bgw_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict)

        fhs_uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3]
        fhc_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict)
              
        sw1_svi_mac = macGenerator()
        sw2_svi_mac = macGenerator() 
        sw3_svi_mac = macGenerator()                       
 
 
        #snoop_list_local_1 = [mac_start1]
        #snoop_list_local_2 = [mac_start2]
        #snoop_list_local_3 = [mac_start3]
        #snoop_mac_list = snoop_list_local_1+snoop_list_local_2+snoop_list_local_3

    @aetest.subsection
    def connect(self, testscript, testbed):
        for uut in uut_list: 
        #for uut in [leaf11fx3]:  
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
        #for uut in bgw_device_list:
        #    preSetupVxlan(uut)

        pcall(preSetupVxlan, uut=tuple(uut_list))


    @aetest.subsection
    def vpcGlobalConf(self, testbed):             
        pcall(addVpcConfig, uut=tuple(vpc_device_list),conf_dict=vpc_conf_dict)
    
 
    
    @aetest.subsection
    def l2Conf(self, testbed):  
        pcall(configureL2Interface, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
 
    @aetest.subsection
    def LoopIntfBringup(self, testbed):    
        pcall(configureLoopInterface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        configureLoopInterface(dci11fx,conf_dict)
 
    @aetest.subsection
    def l3IntfBringup(self, testbed): 
        pcall(configureL3Interface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)

    @aetest.subsection
    def igpConf(self, testbed):  
        pcall(addOspfConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)

    @aetest.subsection
    def PimConf(self, testbed):  

        ssm_range = conf_dict['pim']['site1']['ssm_range']
        pim_rp_address1 = conf_dict['pim']['site1']['pim_rp_address']
        pim_rp_address2 = conf_dict['pim']['site2']['pim_rp_address']
        pim_rp_address3 = conf_dict['pim']['site3']['pim_rp_address']

        ssm_range_1 = []
        rp_add1 = []
        ssm_range_2 = []
        rp_add2 = []
        ssm_range_3 = []
        rp_add3 = []

        for elem in site_1_uut_list:
            ssm_range_1.append(ssm_range)
            rp_add1.append(pim_rp_address1)

        for elem in site_2_uut_list:
            ssm_range_2.append(ssm_range)
            rp_add2.append(pim_rp_address2)
        
        for elem in site_3_uut_list:
            ssm_range_3.append(ssm_range)
            rp_add3.append(pim_rp_address3)
        
        pcall(pimConfigMs, uut=tuple(site_1_uut_list),ssm_range=tuple(ssm_range_1),pim_rp_address=tuple(rp_add1)) 
        pcall(pimConfigMs, uut=tuple(site_2_uut_list),ssm_range=tuple(ssm_range_2),pim_rp_address=tuple(rp_add2)) 
        pcall(pimConfigMs, uut=tuple(site_3_uut_list),ssm_range=tuple(ssm_range_3),pim_rp_address=tuple(rp_add3)) 

       
    @aetest.subsection
    def bgpConf1111333(self, testscript, testbed):

        pcall(ibgpConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict) 
        pcall(saveConf, uut=tuple(vxlan_uut_list))

          
    @aetest.subsection
    def bgpConf(self, testbed): 

        pcall(dciebgpConfigure, uut=tuple(dci_device_list),conf_dict=dci_conf_dict)
        pcall(dcievpnbgpConfigure, uut=tuple(dci_device_list),conf_dict=dci_conf_dict)

  
    @aetest.subsection
    def vxlanConf(self, testbed):   

        pcall(configVxlanLeaf, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(vxlanRouteAdd, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(bgwmultisiteconfig, uut=tuple(bgw_device_list),conf_dict=(bgw_conf_dict))  
   
    @aetest.subsection
    def trmconf(self, testbed): 

        pcall(configureTrm1, uut=tuple(vxlan_uut_list))
        pcall(bgpmvpnConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        pcall(saveConf, uut=tuple(vxlan_uut_list))  
        pcall(clearMac, uut=tuple(uut_list)) 
 
    @aetest.subsection
    def fhsEnable(self, testbed):         
        pcall(fhsCliEnable, uut=tuple(fhs_uut_list),conf_dict=(fhc_conf_dict))  

        for uut in fhs_uut_list:
           if not fhsCliCheck(uut):
                self.failed()
    '''

 
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
 
    
class TC001_Server_leaf11_orphan(aetest.Testcase): 
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))

        enableDhcpTrust(leaf11fx3,"Eth1/9")

    @aetest.test   
    def dhcpTest100(self):
        server_port = leaf11_port1
        if not ixiaDhcpConfTest(port_list,server_port):  
            self.failed()

 
   
    #dhcpTest(port_list,server_port): 
    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf11fx3,"Eth1/9")


class TC002_Server_leaf13(aetest.Testcase): 
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf13fx3,'Eth1/47')


    @aetest.test   
    def testDhcpIxia(self):
        server_port = leaf13_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf13fx3,'Eth1/47')
 


class TC003_Server_leaf11_12_vpc(aetest.Testcase): 
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))

        for uut in [leaf11fx3,leaf12fx3]:
            enableDhcpTrust(uut,"Po11")


    @aetest.test   
    def testDhcpIxia(self):
        server_port = sw1_port
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        for uut in [leaf11fx3,leaf12fx3]:
            disableDhcpTrust(uut,"Po11")

 


class TC004_Server_leaf12_orphan(aetest.Testcase): 
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))

        enableDhcpTrust(leaf12fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxia(self):
        server_port = leaf12_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf12fx3,"Eth1/47")


class TC005_Server_leaf21_orphan(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxia(self):
        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")

class TC006_Server_leaf21_bgp_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiaBgpRestart(self):
         
        ProcessRestart(leaf21fx3,'bgp')
        ProcessRestart(leaf11fx3,'bgp')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC007_Server_leaf21_dhcp_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiadhcpRestart(self):
         
        ProcessRestart(leaf21fx3,'dhcp_snoop')
        ProcessRestart(leaf11fx3,'dhcp_snoop')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")



class TC008_Server_leaf21_l2fm_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxial2fmRestart(self):
         
        ProcessRestart(leaf21fx3,'l2fm')
        ProcessRestart(leaf11fx3,'l2fm')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")



class TC009_Server_leaf21_l2rib_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxial2ribRestart(self):
         
        ProcessRestart(leaf21fx3,'l2rib')
        ProcessRestart(leaf11fx3,'l2rib')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC010_Server_leaf21_adjmgr_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiaadjmgrRestart(self):
         
        ProcessRestart(leaf21fx3,'adjmgr')
        ProcessRestart(leaf11fx3,'adjmgr')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")



class TC011_Server_leaf21_hmm_restart(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiahmmRestart(self):
         
        ProcessRestart(leaf21fx3,'hmm')
        ProcessRestart(leaf11fx3,'hmm')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")




class TC012_Server_leaf21_dhcp_remove_add(aetest.Testcase):
   ###    This is description for my tecase two
   
    @aetest.setup
    def setup(self):

        conf2 = leaf21fx3.configure("no feature dhcp")
        countdown(10)
        fhsCliEnable(leaf21fx3,conf_dict)

        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiahmmRestart(self):
         
        ProcessRestart(leaf21fx3,'hmm')
        ProcessRestart(leaf11fx3,'hmm')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC013_conf_replace(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):      
        for uut in [leaf21fx3,leaf11fx3]:
            uut.execute('dele bootflash:fhs100 no-prompt')
            uut.execute('copy run bootflash:fhs100 ')

        for uut in [leaf21fx3,leaf11fx3]:        
            uut.configure("no feature dhcp")

        countdown(5)

        for uut in [leaf21fx3,leaf11fx3]:  
            uut.execute('configure replace bootflash:fhs100 ')

        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxiahmmRestart(self):
         
        ProcessRestart(leaf21fx3,'hmm')
        ProcessRestart(leaf11fx3,'hmm')

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")

 
class TC014_multisite_testcase_1(aetest.Testcase): 
   ###    This is description for my tecase two

    #Different Port Types 1 - Acces Port == leaf11 1/9 access port
    #Different Port Types2 - Trunk Port == leaf11/12 po 11 - trunk port
    #Multisite : Clients in site1 leaf and BGW - Server connected to Leaf 2 == server in leaf21/clients in leaf11/12/bgw31
    #Multisite : Clients in site 1 leaf and BGW - Server connected to site 2 BGW == server in leaf21/clients in leaf11/12/bgw31(site 3 bgw instead of site1)
    
    
    @aetest.setup
    def setup(self):      
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf13fx3,"Eth1/47")

    @aetest.test   
    def testDhcpIxia(self):
        log.info("DHCP SNOOPING not supported on BGW, So there wont be an entry")         
        server_port = leaf13_port1
        if not ixiaDhcpConfTest(port_list_msite1,server_port):
            self.failed()
 
    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf13fx3,"Eth1/47")



class TC015_clear_ip_dhcp_snooping_statistics(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")

    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3]:
            uut.execute("clear ip dhcp snooping statistics")
         
        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")

 
class TC016_clear_ip_arp(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3]:
            uut.execute("clear ip arp vrf all force-delete")
         
        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC017_clear_mac_addd_dyna(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear mac add dynamic")

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")



class TC018_clear_igp(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear ip os neighbor *")

        countdown(10)    

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC019_clear_igp(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear ip os neighbor *")

        countdown(10)    

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")



class TC020_clear_bgp_l2vpn(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear bgp l2 evpn  *")

        countdown(20)    

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC021_clear_bgp_all(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear bgp all  *")

        countdown(20)    

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")


class TC022_clear_ip_mroute(aetest.Testcase): 
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):            
        pcall(dhcpCleanup, uut=tuple(fhs_uut_list))
        enableDhcpTrust(leaf21fx3,"Eth1/47")


    @aetest.test   
    def trigger(self):

        for uut in [leaf21fx3,leaf11fx3,leaf12fx3]:
            uut.execute("clear ip mroute *")

        countdown(20)    

        server_port = leaf21_port1
        if not ixiaDhcpConfTest(port_list,server_port):
            self.failed()
 

    @aetest.test   
    def testNxodhcpBinding(self, testbed): 
        for leaf in fhs_uut_list:
            checksnoopBinding(leaf,4)
            

    @aetest.test   
    def test3_core(self, testbed): 
        for uut in fhs_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        disableDhcpTrust(leaf21fx3,"Eth1/47")

 
        
        
 
    #if not  ipsgDaiCheck(sw11tetley,sw1_svi_mac):
    #        self.failed()

''' 

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








 
 