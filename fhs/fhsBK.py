
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
                self.failed()
                break
 
         
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
                self.failed()
                break
 
         
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

        IxiaDhcpBringup(srv_port,client_port1,client_port2,client_port3,client_port4,leaf_uut_list)

        
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

    @aetest.test   
    def test1(self, testbed): 
        srv_port = '11/7'
        client_port1 = '11/2'
        client_port2 = '11/1'
        client_port3 = '11/8'
        client_port4 = '11/4'     

        IxiaDhcpBringup(srv_port,client_port1,client_port2,client_port3,client_port4,leaf_uut_list)

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

   

