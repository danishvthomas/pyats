
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
            l2_conf_dict,l2_device_list,tgn1,client_mac_list,dhcp_client1,client_mac_list1,client_topo_handle1,dhcp_client2,client_mac_list2,client_topo_handle2,\
            client_port_hdl1,client_port_hdl2,mac_start1,mac_start2,mac_start3,mac_start4,mac_start5,mac_start6,snoop_list_local_1,snoop_list_local_2,snoop_list_local_3,sw1_svi_mac,sw2_svi_mac,sw3_svi_mac,\
            snoop_mac_list,dhcp_client3,leaf11fx3,leaf12fx3,leaf13fx3,leaf21fx3,leaf31paris,spine11fx,bgw11gx,bgw12gx,bgw21fx3,bgw31fx3,spine31paris,dci11fx,sw11tetley,sw31neptune,vpc_device_list,\
            vpc_conf_dict,site_1_uut_list,site_2_uut_list,site_3_uut_list,vxlan_uut_list,vxlan_conf_dict,dci_device_list,dci_conf_dict,\
            bgw_device_list,bgw_conf_dict,fhs_uut_list,fhc_conf_dict

        
        client_mac_list = []


        skip_setup =  False
        image_upgrade = True


        chassisIP='10.197.127.16'
        serverIP='10.197.127.23'

        #CreateDhcpServ(serverIP,chassisIP)
        #dhcpIxiatest()

        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/fhs/fhs_topo.yaml')) 

        leaf11fx3 = testbed.devices['leaf11fx3']
        leaf12fx3 = testbed.devices['leaf12fx3']
        leaf13fx3 = testbed.devices['leaf13fx3']
        spine11fx = testbed.devices['spine11fx']
        bgw11gx = testbed.devices['bgw11gx']
        bgw12gx = testbed.devices['bgw12gx']
        sw11tetley = testbed.devices['sw11tetley']
        sw31neptune = testbed.devices['sw31neptune']

 
        vxlan_uut_list = [leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx]
        vxlan_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)


        leaf_uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx]

        
        uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,spine11fx,bgw11gx,bgw12gx,sw11tetley,sw31neptune]


        vpc_device_list = [leaf11fx3,leaf12fx3,bgw11gx,bgw12gx] 
        vpc_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict)

        l2_device_list= (leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx,sw11tetley,sw31neptune)
        l2_conf_dict = [conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict] 

        l3_device_list = [leaf11fx3,leaf12fx3,leaf13fx3,spine11fx,bgw11gx,bgw12gx] 
        l3_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        
        fhs_uut_list=[leaf11fx3,leaf12fx3,leaf13fx3,bgw11gx,bgw12gx]
        fhc_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)

        mac_start1 = macGenerator()
        mac_start2 = macGenerator() 
        mac_start3 = macGenerator() 
        mac_start4 = macGenerator() 
        mac_start5 = macGenerator() 
        mac_start6 = macGenerator()                 
        sw1_svi_mac = macGenerator()
        sw2_svi_mac = macGenerator() 
        sw3_svi_mac = macGenerator()                       
 
 
        snoop_list_local_1 = [mac_start1,sw1_svi_mac]
        snoop_list_local_2 = [mac_start2,sw2_svi_mac]
        snoop_list_local_3 = [mac_start3,sw3_svi_mac]
        snoop_mac_list = snoop_list_local_1+snoop_list_local_2+snoop_list_local_3



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


    '''
 
    @aetest.subsection
    def cleanup(self, testbed):                 
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
        pcall(ibgpConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict) 
        pcall(saveConf, uut=tuple(vxlan_uut_list))

    @aetest.subsection
    def vxlanConf(self, testbed):   
        pcall(configVxlanLeaf, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
   

    @aetest.subsection
    def checkl2l3vxlan(self, testbed): 
        pcall(vxlanRouteAdd, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(saveConf, uut=tuple(uut_list))

 

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
 
 
'''
class CSCwf10812(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        cfg3= \
        """
        int Po 11
        switchport trunk allowed vlan 1005-1006
        """
       
        for uut in [leaf11fx3,leaf12fx3,sw11tetley]: 
            uut.configure(cfg3)



    @aetest.test   
    def test1(self, testbed): 
        countdown(60)
        for i in range(50):
            a = random.randint(10,200)
            b = a + 1

            c = random.randint(10,200)
            d = a + 1



            cfg1 = \
            f"""
            no interface Vlan1005
            no ip route 0.0.0.0 0.0.0.0 4.5.0.1
            interface Vlan1005
            no shutdown
            ip address 4.5.{c}.{a}/16
            ip route 0.0.0.0 0.0.0.0 4.5.0.1
            """

            sw31neptune.configure(cfg1)

            cfg2 = \
            f"""
            no interface Vlan1006
            no ip route 0.0.0.0 0.0.0.0 4.5.0.1
            interface Vlan1006
            no shutdown
            ip address 4.6.{d}.{b}/16
            ip route 0.0.0.0 0.0.0.0 4.6.0.1
            """

            clear = \
            """
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear mac add dy   
            clear ip arp vrf all force-delete
            clear logging logfile
            """

            sw11tetley.configure(cfg2)

            for uut in [leaf11fx3,leaf12fx3,bgw11gx,bgw12gx,sw11tetley,sw31neptune]:
                uut.execute(clear) 

        
            sw11tetley.execute(f"ping 4.5.{c}.{a}")
            #sw31neptune.execute("ping 4.6.199.10")
            #countdown(50)
            for uut in [leaf11fx3,leaf12fx3]:
                if "PATH_DELETE:  urib" in uut.execute("show logg log"):
                    self.failed()     
                    break  

            for uut in [leaf11fx3,leaf12fx3,bgw11gx,bgw12gx,sw11tetley,sw31neptune]:
                uut.execute(clear) 


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








 
 