
import logging
from pyats.async_ import pcall
from pyats import aetest
from genie.testbed import load
from random import * 
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
from ixia_dhcp_lib import * 
import unittest
from unittest.mock import Mock
from vxlan3_lib import *

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
 
 
import ixiaPyats_lib

#from ixia_dhcp_lib import * 
#ixiangpf = IxiaNgpf(ixiahlt)
 
#ixLib = ixiaPyats_lib.ixiaPyats_lib()

from esg_lib import *
 

class CommonSetup(aetest.CommonSetup):
    'common setup section always runs first within the script'

    @aetest.subsection
    def connect_to_tb_devices(self, testbed,build=""):
        self.parent.parameters['testbed'] = testbed = load(testbed)

        global ixiangpf,leaf_uut_list,uut_list,fx3005,fx3006,fx3003,tetley001,conf_dict,l3_device_list,l3_conf_dict,\
            l2_conf_dict,l2_device_list,scale2,ip_prefix_ext,bi_dir_list,uni_dir_list,paris002,sw_uut_list,\
            fx3004,fx001,gx001,gx002,fx3004,fx002,tetley001,paris001,vpc_device_list,ip_start1,ip_start2,esg_scale,\
            vpc_conf_dict,site_1_uut_list,vxlan_uut_list,vxlan_conf_dict,esg_start1,esg_start2,vrf_list,paris001_ixia1,paris001_ixia2,\
            paris002_ixia1,paris002_ixia2,tetley001_ixia1,tetley001_ixia2,fx3004_ixia,fx3005_ixia,vlan_1005,vlan_1006,ip_start1,ip_start2,ip_gw1,\
            esg_uut_list_po,esg_conf_dict,spine_conf_dict, esg_uut_gx,esg_uut_fx3,tag_list,traffic_rate_policy,traffic_rate_per_group,traffic_rate2,\
            esg_uut_list,fx3003_ixia,SG1,SG2,ixia_port_list,vrf1,vrf2,spine_uut_list,SG3,SG4,ip_gw_ext,ip_start_ext,\
            rate_no_traffic,ip_start3,ip_gw3,ixia_port_list2,ty,ip_gw_ext,ip_start_ext,ixia_port_list3,\
            traffic_rate_full,ixia_port_list2,traffic_rate_policy_deny
            
        traffic_rate_policy = 90000
        traffic_rate_full = 120000
        traffic_rate_policy_deny = 45000

        rate_no_traffic = int(traffic_rate_full*0.01)

        vrf_list = ["vxlan-900101","vxlan-900101","vxlan-900101","vxlan-900101"]
        esg_scale = 10

        scale2 = 5

        traffic_rate_per_group = int(traffic_rate_full/esg_scale)
        traffic_rate2 =traffic_rate_per_group*scale2

        vlan_1005 = '1005'
        vlan_1006 = '1006'

        ip_start1 = "4.5.0.10"
        ip_start3 = "4.5.1.100"
        ip_start2 = "4.6.1.100"
        ip_start_ext = "145.1.1.10"
        ip_prefix_ext = "145.1.0.0/16"
        ip_gw_ext = "145.1.1.1"  
        ip_gw1 =  "4.5.0.1"
        ip_gw3 =  "4.6.0.1"
        esg_start1 = 5100
        esg_start2 = 10100
  
        SG1 =  '11111'
        SG2 =  '22222'
        SG3 =  '33333'
        SG4 =  '44444'

        tag_list = [SG1,SG2]
 

        vrf1 = 'vxlan-900102'
        vrf2 = 'vxlan-900101'
     

        esg_start1 = 5100
        esg_start2 = 10100
 
        paris001_ixia1 = '11/1'
        paris001_ixia2 = '11/6'
        paris002_ixia1 = '11/3'
        paris002_ixia2 = '11/5'
        tetley001_ixia1 = '11/2'
        tetley001_ixia2 = '11/8'
        fx3004_ixia = '11/7'   
        fx3003_ixia = '11/4'   


        bi_dir_list = ('bidir','bidir','bidir','bidir','bidir','bidir')
        uni_dir_list = ('unidir','unidir','unidir','unidir','unidir','unidir')
        ixia_port_list = [tetley001_ixia1,tetley001_ixia2,paris001_ixia1,paris001_ixia2,paris002_ixia1,paris002_ixia2,fx3004_ixia,fx3003_ixia]
        #ixia_port_list = [paris001_ixia1,tetley001_ixia1,tetley001_ixia2,paris002_ixia1,fx3005_ixia,paris001_ixia2]
        ixia_port_list2 = [tetley001_ixia1,tetley001_ixia2,paris001_ixia1,paris002_ixia1,paris002_ixia2,fx3004_ixia]
                      

        skip_setup =  False
        image_upgrade = True

        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/esg/vxlan_topo2.yaml')) 

        fx3005 = testbed.devices['fx3005']
        fx3006 = testbed.devices['fx3006']
        fx3003 = testbed.devices['fx3003']
        fx3004 = testbed.devices['fx3004']
        fx001 = testbed.devices['fx001']   
        gx001 = testbed.devices['gx001']
        gx002 = testbed.devices['gx002']
        fx002 = testbed.devices['fx002']
        tetley001 = testbed.devices['tetley001']
        paris001 = testbed.devices['paris001']
        paris002 = testbed.devices['paris002']

        sw_uut_list = [paris002,paris001,tetley001]

        spine_uut_list = [fx001,fx002]
        spine_conf_dict = [conf_dict,conf_dict]

        site_1_uut_list = [fx3005,fx3006,fx3003,gx001,gx002,fx001]
 
        vxlan_uut_list = [fx3005,fx3006,fx3003,fx3004,gx001,gx002]
        vxlan_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)

        leaf_uut_list=[fx3005,fx3006,fx3003,fx3004,gx001,gx002]
        uut_list=[fx3005,fx3006,fx3003,fx3004,fx001,fx002,gx001,gx002,tetley001,paris001,paris002]

        vpc_device_list = [fx3005,fx3006,gx001,gx002] 
        vpc_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict)

        l2_device_list= (paris002,gx001,gx002,fx3005,fx3006,fx3003,fx3004,tetley001,paris001)
        l2_conf_dict = [conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict] 

        l3_device_list = [fx3005,fx3006,fx3003,fx3004,fx002,fx001,gx001,gx002] 
        l3_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)

        esg_uut_list = [gx001,gx002,fx3005,fx3006,fx3003,fx3004]
        esg_conf_dict = (conf_dict,conf_dict,conf_dict,conf_dict,conf_dict,conf_dict)
        esg_uut_list_po  = [gx001,gx002,fx3005,fx3006,fx3003]
        esg_uut_gx = [gx001,gx002]                            
        esg_uut_fx3 = [fx3005,fx3006]

 
 
    @aetest.subsection
    def connect(self, testscript, testbed):
        for uut in uut_list: 
        #for uut in [gx002,gx001]:    
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
        #pcall(vni2kvrf500, uut=tuple(vxlan_uut_list))   
 

 

    @aetest.subsection
    def cleanup(self, testbed):                 
        pcall(preSetupVxlan, uut=tuple(l3_device_list))
        pcall(SwCleanupConfigs, uut=tuple(sw_uut_list)) 

        countdown(30)    
 
    @aetest.subsection
    def vpcGlobalConf(self, testbed):             
        pcall(addVpcConfig, uut=tuple(vpc_device_list),conf_dict=vpc_conf_dict)

    @aetest.subsection
    def l2Conf(self, testbed):  
        pcall(configureL2Interface, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
 

    @aetest.subsection
    def LoopIntfBringup(self, testbed):    
        pcall(configureLoopInterface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        configureLoopInterface(fx002,conf_dict)
 
    @aetest.subsection
    def l3IntfBringup(self, testbed): 
        pcall(configureL3Interface, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
  
    @aetest.subsection
    def igpConf(self, testbed):  
        pcall(addOspfConfig, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)

 

    @aetest.subsection
    def PimConf(self, testbed):  
        pimConfig(l3_device_list,conf_dict)
        pcall(pimConfigSpine, uut=tuple(spine_uut_list),conf_dict=tuple(spine_conf_dict))
 
 
    @aetest.subsection
    def bgpConf(self, testscript, testbed):
        pcall(ibgpConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict) 
        pcall(saveConf, uut=tuple(vxlan_uut_list))
  

    @aetest.subsection
    def vxlanConf(self, testbed):   
        pcall(configVxlanLeaf, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(vxlanRouteAdd, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(addBgpPip, uut=tuple(vxlan_uut_list)) 
        pcall(vxlanVrfRouteleak, uut=tuple(vxlan_uut_list)) 

    @aetest.subsection
    def trmconf(self, testbed): 
        pcall(configureTrm1, uut=tuple(vxlan_uut_list))
        pcall(bgpmvpnConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        pcall(saveConf, uut=tuple(vxlan_uut_list))  
        pcall(clearMac, uut=tuple(uut_list)) 
        pcall(disableHapReset, uut=tuple(vxlan_uut_list))  

 

    @aetest.subsection
    def externalRoute(self, testbed): 
        pcall(vxlanRouteAdd, uut=tuple(vxlan_uut_list),conf_dict=(vxlan_conf_dict))  
        pcall(addBgpPip, uut=tuple(vxlan_uut_list))  
  
        cfg= \
        """
        feature ospfv3
        ip access-list type5555
        permit ip any any

        route-map ospfToBgp permit
        match ip address type5555 
        match route-type internal 

        route-map bgpToOspf permit
        match ip address type5555 
        
        router ospfv3 100
        address-family ipv6 unicast
        vrf vxlan-900102
        address-family ipv6 unicast

        router ospf 45
        vrf vxlan-900102
        redistribute bgp 65001 route-map ospfToBgp 

        int e1/13
        channel-group 11 force mode active
                        
        interface Port-channel 11
        no switchport
        vrf member vxlan-900102
        ip address 45.1.1.1/24
        ipv6 address 45::1/112
        ipv6 router ospfv3 100 area 0.0.0.0                
        ip router ospf 45 area 0
        no shut
       
        router bgp 65001  
        vrf vxlan-900102
        address-family ipv4 unicast
        redistribute ospf 45 route-map bgpToOspf
        redistribute direct route-map bgpToOspf
        address-family ipv6 unicast
        network 2002:1:1:1:1:0:145:0/112        
        """

        fx3003.configure(cfg)

        cfg= \
        f"""
        feature ospf
        feature ospfv3
        
        router ospf 45
        router ospfv3 100

        interface port-channel11
        description Po 11
        no switchport
        ip address 45.1.1.2/24
        ipv6 address 45::2/112
        ip router ospf 45 area 0.0.0.0
        ipv6 router ospfv3 100 area 0.0.0.0

        interface Vlan1005
        no shutdown
        ip address {ip_gw_ext}/16
        ipv6 address 2002:1:1:1:1:0:145:1/112
        ip router ospf 45 area 0.0.0.0
        ipv6 router ospfv3 100 area 0.0.0.0                
        ip route 0.0.0.0 0.0.0.0 45.1.1.1                   
        ipv6 route 0::0/0 45::1
        
        
        """
        paris002.configure(cfg)

        pcall(configureTrm1, uut=tuple(vxlan_uut_list))
        pcall(bgpmvpnConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        pcall(saveConf, uut=tuple(vxlan_uut_list)) 
 
    @aetest.subsection
    def v6Enable(self, testbed): 
        #import pdb;pdb.set_trace()
        #pcall(enableV6forVxlan2, uut=tuple(vxlan_uut_list)) 
        pcall(enableV6forVxlan2, uut=tuple(vxlan_uut_list))      
 
 
 
    @aetest.subsection
    def ixiaSetup(self, testbed):              

        pcall(bpduFilter, uut=(fx3003,fx3004),port=('Eth1/3','Eth1/3')) 

        cfg= \
        """
        clear ipv6 neighbor vrf all force-delete
        clear ip arp vrf all force-delete 
        clear mac add dynamic        
        """

        for uut in esg_uut_list:
            uut.configure(cfg) 

 

        log.info("SETUP HOSTS & TRAFFIC IN IXIA")
        esgAllTrafficTestScale(ixia_port_list,esg_scale) 



 

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
    ########################################

 

class TC001_enableFeature(aetest.Testcase):
    @aetest.setup
    def setup(self):

        log.info("Add security group routing template")

        pcall(addSecGrpTemplate, uut=tuple(esg_uut_list))

        log.info("Test traffic without security group")
        if not removeSecurityGroup(esg_uut_list):
            self.failed()         

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate_full): 
            self.failed(goto=['common_cleanup'])

    @aetest.test   
    def test1(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            uut.configure("system no hap-reset")

            pcall(configureSgacl, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)
            pcall(configureSgaclV6, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                self.failed()       

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()


    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
 
 

 
class TC002_mcast_default_deny(aetest.Testcase):
   ###    his is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test4(self): 
        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                self.failed()       

        log.info("TEST TRAFFIC rate_no_traffic") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(rate_no_traffic): 
                self.failed(goto=['common_cleanup'])              
 
  
 
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass

 
class TC003_mcast_default_deny_plus_permit_policy(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        #esgAllTrafficTest(ixia_port_list,esg_scale)
        pass

    @aetest.test   
    def test5(self): 
        for uut in esg_uut_list:
            uut.configure("logging ip access-list include sgt")

        log.info("CONFIGURE permit Contract unidir") 
        
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)
     
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate_policy)): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(int(traffic_rate_policy)): 
                self.failed(goto=['common_cleanup'])              
            self.failed()  
        #import pdb;pdb.set_trace() 

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache detail")        
        pass
 
 

 
class TC017_Proc_restart_urib(aetest.Testcase):

    def setup(self):    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for protocol in ['policyelem','policy_mgr']:
        for protocol in ['urib']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            import pdb;pdb.set_trace()
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache detail")        
        pass
 

class TC017_Proc_restart_vpc(aetest.Testcase):

    def setup(self):    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for protocol in ['policyelem','policy_mgr']:
        for protocol in ['vpc']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            import pdb;pdb.set_trace()
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache detail")        
        pass
 
  




 

class tc032111TriggerAccessPortFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
   
              

    @aetest.test   
    def test7(self): 

        #pcall(po11Flap, uut=tuple(sw),timegap=(100,100,100))
        po11Flap(tetley001,100)
        countdown(150)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy):          
            self.failed()     
              

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass      



class tc03222221TriggerAccessPortFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
    
              

    @aetest.test   
    def test7(self): 

        #pcall(po11Flap, uut=tuple(sw_uut_list),timegap=(200,200,200))
        po11Flap(tetley001,200)
        countdown(150)


        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy):          
            self.failed()     
              

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass      



class tc03333331TriggerAccessPortFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
  
              

    @aetest.test   
    def test7(self): 


        po11Flap(tetley001,2)
        #pcall(po11Flap, uut=tuple(sw_uut_list),timegap=(2,2,2))
        countdown(150)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy):          
            self.failed()     
              

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        pass      


 
 
class tc10001_mcast_remove_add_class(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def trigger1(self):         
        for uut in esg_uut_list:
            if not removeAddClass(uut,"permit_all","permit_all","permit"):
                self.failed()

        countdown(50)
        
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")


    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass

class tc10002_mcast_remove_add_policy_contract(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
        for uut in esg_uut_gx:
            if not removeAddPolicyContract(uut,"permit_all","permit_all","permit"):
                self.failed()

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc10003_mcast_remove_add_class_from_policy(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
        for uut in esg_uut_gx:
            if not removeAddClassFromPolicy(uut,"permit_all","permit_all","permit"):
                self.failed()

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass



class tc10004_mcast_remove_add_match_from_class(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
        for uut in esg_uut_gx:
            if not removeAddMatchInClass(uut,"permit_all","permit_all","permit"):
                self.failed()

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc10005_mcast_remove_bgp_add(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
            
        pcall(removeAddBgp,uut=(fx3005,fx3006))

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc10006_mcast_clear_bgp(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
            
        for uut in [fx3005,gx001]:
            uut.configure("clear bgp all *")

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


 
class tc023TriggerClearIpRoute(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear ip route *") 
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc10007_mcast_clear_bgp_neighbor(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
            
        pcall(removeAddBgpNeighbor,uut=(fx3005,fx3006))

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc1008_mcast_rp_loss_recovery(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
           
        pcall(loopInterfaceFlap,uut=(fx001,fx002))
        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass



class tc1009_removAddSgacl(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
           
        pcall(removeAddSgacl,uut=(fx3006,gx002))

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class tc1010_removeAddSelector(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
           
        pcall(removeAddSelector,uut=(fx3005,fx3006))

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass



class tc1011_withOutArpSuppress(aetest.Testcase):
   ###    This is description for my tecase two

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)   
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                    

    @aetest.test       
    def trigger1(self):         
           
        fx3005_conf = removeArpSuppress(fx3005)
        fx3006_conf = removeArpSuppress(fx3006)
        gx001_conf = removeArpSuppress(gx001)
        gx002_conf = removeArpSuppress(gx002)

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     

        fx3005.configure(fx3005_conf)
        fx3006.configure(fx3006_conf)
        gx001.configure(gx001_conf)
        gx002.configure(gx002_conf)

        countdown(50)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()  

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


# class tc032111TriggerAccessPortFlap(aetest.Testcase):
#     @aetest.setup
#     def setup(self):
#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy): 
#             #pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              

#     @aetest.test   
#     def test7(self): 

#         pcall(po11Flap, uut=tuple(esg_uut_list_po))
#         countdown(110)

#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy): 
#             #import pdb;pdb.set_trace()
#             #pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              

#     @aetest.test   
#     def testLocalFwd(self):   
#         for uut in esg_uut_fx3:
#             if not icmpPingTest(uut):
#                 #import pdb;pdb.set_trace()
#                 self.failed()

#     @aetest.test   
#     def testArpTable(self):   
#         for uut in esg_uut_fx3:
#             if not checkArpTable(uut,ip_start2,vrf1):
#                 self.failed()

#         for uut in esg_uut_gx:
#             if not checkArpTable(uut,ip_start1,vrf1):
#                 self.failed()

#     @aetest.cleanup
#     def cleanup(self):
#         pass      



 
class TC005_mcast_removeEsgContractAndDeny(aetest.Testcase):
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                self.failed()       
                  
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                self.failed()              

                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_full): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_full): 
                self.failed(goto=['common_cleanup'])              
            self.failed()   

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
 


class TC006_mcast_default_permit_plus_deny_policy(aetest.Testcase):
    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        pcall(configureSecurityContractDeny2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)      

        log.info("TEST TRAFFIC 1/2 TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate_policy_deny)): 
            #import pdb;pdb.set_trace()
            self.failed()       
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
 
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
     
class TC008_mcast_default_permit_remove(aetest.Testcase):

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test8(self):     
    
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                self.failed()       
                  
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","permit"):
                self.failed()              
        

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_full): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_full): 
                self.failed(goto=['common_cleanup'])              
            self.failed()    

            
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if  not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
                
    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
 
 

class TC009_mcastToIngresConvert(aetest.Testcase):
   
    @aetest.setup
    def setup(self):
        pass


    @aetest.test   
    def test4(self): 
        cfg = \
        """
        interface nve1
        member vni 201002-201006
            suppress-arp
            no mcast-group 239.1.1.1
            ingress-replication protocol bgp
            shut
            no shut    
            """
        for uut in esg_uut_list:
            try:
                uut.configure(cfg)
            except:
                log.error('CONFIGS FAILED FOR %r',uut)
                self.failed()   

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
 


class TC010_ingresRepl_default_deny(aetest.Testcase):
   ###    his is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test4(self): 
        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                self.failed()       

        log.info("TEST TRAFFIC  rate_no_traffic") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(rate_no_traffic): 
                self.failed(goto=['common_cleanup'])              
            self.failed()       

        
            
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
  
 

class TC012_ingresRepl_default_deny_plus_permit_policy_bidir(aetest.Testcase):
   ###    This is description for my tecase two

    def setup(self):
        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                self.failed()       

    @aetest.test   
    def test6(self): 

        log.info("CONFIGURE permit Contract bidi") 
        #for uut in esg_uut_list:
        pcall(configureSecurityContract2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)                       
        countdown(30)                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy): 
                self.failed(goto=['common_cleanup'])              
            self.failed()  
                    

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass


class TC013_ingresRepl_removeEsgContractAndDeny(aetest.Testcase):
   ###    This is description for my tecase two
    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                self.failed()       
                  
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                self.failed()              
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_full): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_full): 
                self.failed(goto=['common_cleanup'])              
            self.failed()                        
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
 


class TC014_ingresRepl_default_permit_plus_deny_policy_unidir(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                self.failed()    

    @aetest.test   
    def test6(self):         
   
            
        log.info("CONFIGURE deny Contract") 

        pcall(configureSecurityContractDeny2, uut=tuple(esg_uut_list),conf_dict=esg_conf_dict)               

        log.info("TEST TRAFFIC 1/3 TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate_policy_deny)): 
            #import pdb;pdb.set_trace()
            self.failed()  
     
 
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
 
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
     
 
 
 

class TC018_Proc_restart_urib_ipfib_hmm(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            #import pdb;pdb.set_trace()
            #pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            #countdown(30)
            #if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            self.failed(goto=['common_cleanup'])              
            #self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for uut in esg_uut_list:
        for protocol in ['urib','ipfib','hmm']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny):
            import pdb;pdb.set_trace() 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass    

 


class TC019_Proc_restart_nve_cfs_vpc(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for uut in esg_uut_list:
        for protocol in ['nve','cfs','vpc']:
            if not 'vpc' in protocol:
                processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny):
            for uut in esg_uut_list:
                uut.execute("show ip arp vrf all") 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['traffic_rate_policy_deny'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        



class TC020_Proc_restart_arp_adjmgr_aclqos(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for uut in esg_uut_list:
        for protocol in ['arp','adjmgr','aclqos']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass            


class TC021_Proc_restart_netstack_ethpm_l2rib(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for uut in esg_uut_list:
        for protocol in ['netstack','ethpm','l2rib']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass            

 
class TC022_Proc_restart_eltm_ospf_l2fm(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        #for uut in esg_uut_list:
        for protocol in ['eltm','ospf','l2fm']:
            processRestartTest(esg_uut_list[randint(0,5)],protocol)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      
 
 

'''

 
class tc024TriggerClearIpRouteVrf(aetest.Testcase):

    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear ip route vrf all *",timeout=300)
        countdown(80)


        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass    


class tc025TriggerClearBgpAll(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear bgp all *") 
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        

class tc025TriggerClearBgpAll(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear bgp all *") 
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass    
  
        
class tc1026TriggerClearIpArp(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear ip arp vrf all",timeout=300)
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        


        
# class tc2026TriggerClearIpArpForceDel(aetest.Testcase):
#     @aetest.setup
#     def setup(self):
#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#             pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              

#     @aetest.test   
#     def test7(self):  

#         for uut in esg_uut_list:
#             uut.configure("clear ip arp vrf all force-delete",timeout=300)
#         countdown(80)

#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#             pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              

#     @aetest.test   
#     def testHWProgramming(self):         
#         for uut in esg_uut_gx:
#             if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
#                 self.failed()

#         for uut in esg_uut_fx3:
#             if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
#                 self.failed()

#     @aetest.test   
#     def checkLogs(self):  
#         for uut in esg_uut_list:
#             uut.execute("show logging ip access-list cache")

#     @aetest.test   
#     def testLocalFwd(self):   
#         for uut in esg_uut_fx3:
#             if not icmpPingTest(uut):
#                 #import pdb;pdb.set_trace()
#                 self.failed()

#     @aetest.test   
#     def testArpTable(self):   
#         for uut in esg_uut_fx3:
#             if not checkArpTable(uut,ip_start2,vrf1):
#                 self.failed()

#         for uut in esg_uut_gx:
#             if not checkArpTable(uut,ip_start1,vrf1):
#                 self.failed()

#     @aetest.cleanup
#     def cleanup(self):
#         pass        




class tc027TriggerClearFwd(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  


        for uut in esg_uut_list:
            uut.configure(" clear forwarding route * module all") 
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        



class tc028TriggerFwdVrf(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  


        for uut in esg_uut_list:
            uut.configure("clear forwarding route vrf vxlan-900101 * module all") 

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        



class tc029TriggerClearMac(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  



        for uut in esg_uut_list:
            uut.configure("clear mac address-table dynamic") 

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        




class tc030TriggerClearMac(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  



        for uut in esg_uut_list:
            uut.configure("clear mac address-table dynamic") 

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        





class tc031TriggerClearOspf(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear ip ospf UNDERLAY neighbor *") 

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        



class tc032TriggerClearOspf(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure("clear ip ospf UNDERLAY neighbor *") 

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      



class tc032TriggerUpLinkFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  
        pcall(coreInterfaceFlap, uut=tuple(esg_uut_list))

        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

class tc033TriggerConfigReplace1(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 
        
        cli_list = []
        for i in range(len(esg_uut_list)):
            cli_list.append("no feature security-group")
        
        pcall(configReplaceEsg1, uut=tuple(esg_uut_list),cli=tuple(cli_list))
            
                 
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")                
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

                

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      



class tc034TriggerConfigReplace2(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 


        cli_list = []
        for i in range(len(esg_uut_list)):
            cli_list.append("no feature bgp")
        
        pcall(configReplaceEsg1, uut=tuple(esg_uut_list),cli=tuple(cli_list))
                     
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              


    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      




class tc036TriggerLoopIntfFlapSpine(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 

        for uut in spine_uut_list:
            if not triggerLoopIfFlapOspf(uut):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()  

  
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

class tc037TriggerLoopIntfFlapLeaf(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 

        for uut in esg_uut_list:
            if not triggerLoopIfFlapOspf(uut):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()              
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

 
class tc039TriggerMctMemberFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 

        for uut in vpc_device_list:
            if not vPCMemberFlap(uut,["1"]):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()              
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

 

class tc040TriggerSecondIpLoopRemoveAdd(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 
        
        for uut in vpc_device_list:
            if not secodaryIpRemoveAdd(uut):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()              
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      



class tc041TriggerSviFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 
        
        for uut in esg_uut_list:
            if not sviFlap(uut):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()              
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      


 
class tc043TriggerAnyCastRPFailover(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test1(self): 
        if not nodeIsolate(spine_uut_list[0]):
            #import pdb;pdb.set_trace()
            self.failed()   

        countdown(40)
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

        if not nodeNoIsolate(spine_uut_list[0]):
            #import pdb;pdb.set_trace()
            self.failed()   

        countdown(40)
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test2(self): 
        if not nodeIsolate(spine_uut_list[1]):
            #import pdb;pdb.set_trace()
            self.failed()   

        countdown(40)
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

        if not nodeNoIsolate(spine_uut_list[1]):
            #import pdb;pdb.set_trace()
            self.failed()   

        countdown(40)
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

 
 
class tc044TriggerRemoveAddSecEnforc(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              


    @aetest.test   
    def test2(self): 
                  
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                self.failed()      

        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                self.failed()   

        countdown(40)
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
  
    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      



class tc035TriggerConfigReplace3(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 

        cli_list = []
        for i in range(len(esg_uut_list)):
            cli_list.append("no feature nv overlay")
        
        pcall(configReplaceEsg1, uut=tuple(esg_uut_list),cli=tuple(cli_list))
                       
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      

 
# class tc038TriggerVpcMemberFlap(aetest.Testcase):
#     @aetest.setup
#     def setup(self):
#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#             pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              

#     @aetest.test   
#     def test7(self): 

#         for uut in vpc_device_list:
#             if not vPCMemberFlap(uut,["11"]):
#                 ##import pdb;pdb.set_trace()
#                 pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#                 self.failed()              
#         countdown(80)

#         log.info("TEST TRAFFIC ") 
#         if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#             pcall(vxlanEsgAllReset,uut=(esg_uut_list))
#             countdown(30)
#             if not ixiaStatCheckRate(traffic_rate_policy_deny): 
#                 self.failed(goto=['common_cleanup'])              
#             self.failed()     
              
 

#     @aetest.test   
#     def testHWProgramming(self):                 
#         for uut in esg_uut_gx:
#             if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
#                 self.failed()

#         for uut in esg_uut_fx3:
#             if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
#                 self.failed()

#     @aetest.test   
#     def checkLogs(self):  
#         for uut in esg_uut_list:
#             uut.execute("show logging ip access-list cache")
                
#     @aetest.test   
#     def testLocalFwd(self):   
#         for uut in esg_uut_fx3:
#             if not icmpPingTest(uut):
#                 #import pdb;pdb.set_trace()
#                 self.failed()

#     @aetest.test   
#     def testArpTable(self):   
#         for uut in esg_uut_fx3:
#             if not checkArpTable(uut,ip_start2,vrf1):
#                 self.failed()

#         for uut in esg_uut_gx:
#             if not checkArpTable(uut,ip_start1,vrf1):
#                 self.failed()

#     @aetest.cleanup
#     def cleanup(self):
#         pass      


  

class tc042TriggerVlanFlap(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self): 
        
        for uut in esg_uut_list:
            if not vlanFlap(uut):
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()              
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              
 

    @aetest.test   
    def testHWProgramming(self):                 
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")
                
    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass      
 

        
class tc2026221TriggerClearIpv6Route(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure(" clear ipv6 route vrf vxlan-900101",timeout=300)
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        






class tc20261TriggerClearIpv6NeiForceDel(aetest.Testcase):
    @aetest.setup
    def setup(self):
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def test7(self):  

        for uut in esg_uut_list:
            uut.configure(" clear ipv6 neighbor vrf vxlan-900101",timeout=300)
        countdown(80)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_policy_deny): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_policy_deny): 
                self.failed(goto=['common_cleanup'])              
            self.failed()     
              

    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass        



class TC016_ingresRepl_default_permit_remove(aetest.Testcase):

    @aetest.setup
    def setup(self):
        pass

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                ##import pdb;pdb.set_trace()
                pcall(vxlanEsgAllReset,uut=(esg_uut_list))
                self.failed()     

        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                self.failed()       
                  
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","permit"):
                self.failed()     

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate_full): 
            pcall(vxlanEsgAllReset,uut=(esg_uut_list))
            countdown(30)
            if not ixiaStatCheckRate(traffic_rate_full): 
                self.failed(goto=['common_cleanup'])              
            self.failed()      

            
    @aetest.test   
    def testHWProgramming(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1,SG2,SG3,SG4]):
                self.failed()

    @aetest.test   
    def checkLogs(self):  
        for uut in esg_uut_list:
            uut.execute("show logging ip access-list cache")

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.test   
    def testLocalFwd(self):   
        for uut in esg_uut_fx3:
            if not icmpPingTest(uut):
                #import pdb;pdb.set_trace()
                self.failed()

    @aetest.test   
    def testArpTable(self):   
        for uut in esg_uut_fx3:
            if not checkArpTable(uut,ip_start1,vrf1):
                self.failed()

        for uut in esg_uut_gx:
            if not checkArpTable(uut,ip_start2,vrf1):
                self.failed()

    @aetest.cleanup
    def cleanup(self):
        pass
''' 
 
class common_cleanup(aetest.CommonCleanup):

    @aetest.subsection
    def stop_tgn_streams(self):
        #IxiaReset()
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








 
  
