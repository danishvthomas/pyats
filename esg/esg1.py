
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
            l2_conf_dict,l2_device_list,scale2,ip_prefix_ext,port_handle2,handle1,handle2,paris002,sw_uut_list,\
            fx3004,fx001,gx001,gx002,fx3004,fx002,tetley001,paris001,vpc_device_list,ip_start1,ip_start2,esg_scale,\
            vpc_conf_dict,site_1_uut_list,vxlan_uut_list,vxlan_conf_dict,esg_start1,esg_start2,vrf_list,paris001_ixia1,paris001_ixia2,\
            paris002_ixia1,paris002_ixia2,tetley001_ixia1,tetley001_ixia2,fx3004_ixia,fx3005_ixia,vlan_1005,vlan_1006,ip_start1,ip_start2,ip_gw1,\
            server_port,spine_conf_dict, esg_uut_gx,esg_uut_fx3,tag_list1,tag_list2,tag_list,traffic_rate1,traffic_rate_per_group,traffic_rate2,\
            esg_uut_list,fx3005_ixia,SG1,SG2,ixia_port_list,vrf1,vrf2,spine_uut_list,port_hdl1,port_hdl2,ip_gw_ext,ip_start_ext,\
            rate_no_traffic,ip_start3,ip_gw3,ixia_port_list2,ty,ip_gw_ext,ip_start_ext,ixia_port_list3
            
        traffic_rate1 =20000

        rate_no_traffic = int(traffic_rate1*0.01)

        vrf_list = ["vxlan-900101","vxlan-900101","vxlan-900101","vxlan-900101"]
        esg_scale = 20

        scale2 = 5


        traffic_rate_per_group = int(traffic_rate1/esg_scale)
        traffic_rate2 =traffic_rate_per_group*scale2

        vlan_1005 = '1005'
        vlan_1006 = '1006'

        ip_start1 = "4.5.0.10"
        ip_start2 = "4.5.1.100"

        ip_start3 = "4.6.1.100"
        ip_start_ext = "145.1.1.10"
        ip_prefix_ext = "145.1.0.0/16"
        ip_gw_ext = "145.1.1.1"  
        ip_gw1 =  "4.5.0.1"
        ip_gw3 =  "4.6.0.1"
        esg_start1 = 5100
        esg_start2 = 10100
  
        SG1 =  '4444'
        SG2 =  '7777'

        tag_list = [SG1,SG2]
 

        vrf1 = 'vxlan-900101'
        vrf2 = 'vxlan-900102'
     

        esg_start1 = 5100
        esg_start2 = 10100
        '''

        traffic_rate1 : '80000'
        gx_paris001_ixia1 :  '11/1'
        gx_paris001_ixia2 :  '11/6'
        fx33_paris002_ixia1 :  '11/3'
        fx33_paris002_ixia2 :  '11/5'
        fx356_tetley001_ixia1 :  '11/2'
        fx356_tetley001_ixia2 :  '11/8'
        fx3005_ixia :  '11/7'
        fx3004_ixia :  '11/4'   
        '''
        paris001_ixia1 = '11/1'
        paris001_ixia2 = '11/6'
        paris002_ixia1 = '11/3'
        paris002_ixia2 = '11/5'
        tetley001_ixia1 = '11/2'
        tetley001_ixia2 = '11/8'
        fx3005_ixia = '11/7'
        fx3004_ixia = '11/4'   


        ixia_port_list = [paris001_ixia1,tetley001_ixia1,tetley001_ixia2,paris002_ixia1]
        ixia_port_list2 = [paris001_ixia1,fx3005_ixia]
        ixia_port_list3 = [paris001_ixia1,paris002_ixia1]                          

        #paris001_ixia2,paris002_ixia1,paris002_ixia2,tetley001_ixia1,tetley001_ixia2,fx3004_ixia,fx3005_ixia,]


        skip_setup =  False
        image_upgrade = True


        conf_dict=yaml.safe_load(open('/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/esg/vxlan_topo3.yaml')) 

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


    @aetest.subsection
    def cleanup(self, testbed):                 
        pcall(preSetupVxlan, uut=tuple(l3_device_list))
        pcall(SwCleanupConfigs, uut=tuple(sw_uut_list))
 
    @aetest.subsection
    def vpcGlobalConf(self, testbed):             
        pcall(addVpcConfig, uut=tuple(vpc_device_list),conf_dict=vpc_conf_dict)
    
    @aetest.subsection
    def l2Conf(self, testbed):  
        import pdb;pdb.set_trace()
        pcall(configureL2Interface, uut=tuple(l2_device_list),conf_dict=l2_conf_dict)
 
    ''' 
    ######
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
        
        cfg= \
        """
        interface Port-channel 11
        no switchport
        vrf member vxlan-900101
        ip address 45.1.1.1/24
        no shut

        router ospf 45
        vrf vxlan-900101
        interface Port-channel 11
        ip router ospf 45 area 0
        ip access-list type5555
        permit ip any any

        route-map ospfToBgp permit
        match ip address type5555 
        match route-type internal 

        route-map bgpToOspf permit
        match ip address type5555 
        
                
        router ospf 45
        vrf vxlan-900101
        redistribute bgp 65001 route-map ospfToBgp 
       
        router bgp 65001  
        vrf vxlan-900101
        address-family ipv4 unicast
        redistribute ospf 45 route-map bgpToOspf
        redistribute direct route-map bgpToOspf
        """

        fx3003.configure(cfg)

        cfg= \
        f"""
        interface Port-channel 11
        no switchport
        ip address 45.1.1.2/24
        no shut
        feature ospf
        router ospf 45
        interface Port-channel 11
        ip router ospf 45 area 0
        interface vlan 1005
        ip address {ip_gw_ext}/16
        no shut
        ip router ospf 45 area 0   
         ip route 0.0.0.0 0.0.0.0 45.1.1.1                   
        """
        paris002.configure(cfg)

        pcall(configureTrm1, uut=tuple(vxlan_uut_list))
        pcall(bgpmvpnConfigure, uut=tuple(l3_device_list),conf_dict=l3_conf_dict)
        pcall(saveConf, uut=tuple(vxlan_uut_list))  
 
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



class TC010_test1_routed_proc_restart1(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        esgAllTrafficTest(ixia_port_list)
     
    '''

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list3)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start_ext,ip_gw1,ip_gw_ext,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed(goto=['common_cleanup'])   

 

        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()      

            if not configureSgaclExt(uut,ip_prefix_ext,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
 
 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       


        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()
 

        for uut in esg_uut_list:
            for protocol in ['arp','adjmgr','aclqos','netstack','ethpm','l2rib','eltm','ospf']:
                ProcessRestart(uut,protocol)

        countdown(100)

        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()
 
   
  
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()    

      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        
    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass   
 

 
class TC011_test1_bridged_proc_restart2(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()


        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed(goto=['common_cleanup'])   


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear ip route *") 

        countdown(100)

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   



        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
 





 
class TC012_test1_bridged_proc_restart2(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')

 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            for protocol in ['policyelem','policy_mgr','urib','ipfib','hmm','nve','cfs','vpc']:
                ProcessRestart(uut,protocol)


        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   



        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
 

 
class TC013_test1_bridged_clear_ip_route_vrf(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear ip route vrf all *") 

        countdown(100)

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   



        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
 


 
class TC014_test1_bridged_clear_ip_route(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear ip route vrf all *") 

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
      

class TC015_test1_bridged_clear_bgp_all(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear bgp all *") 

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass



class TC016_test1_bridged_clear_ip_arp(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear forwarding route vrf vxlan-900101 * module all") 
            uut.configure("clear ip arp vrf all") 
            uut.configure("clear ip arp vrf all force-delete") 
            

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
  
class TC017_test1_bridged_clear_fwd(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure(" clear forwarding route * module all") 


        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass


class TC018_test1_bridged_clear_fwd(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear forwarding route vrf vxlan-900101 * module all") 


        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
  
class TC018_test1_bridged_clear_mac(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')


 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()

        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       
  
      
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
                
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            uut.configure("clear mac address-table dynamic") 


        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   


        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
      
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()
        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
  
 
 
class TC005_test1_routed_type5_mcast(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass
    

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list3)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start_ext,ip_gw1,ip_gw_ext,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed() 


    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgaclExt(uut,ip_prefix_ext,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
    
        pass    



 

class TC006_test1_routed_type5_ingress_replicn(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass
     

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list3)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start_ext,ip_gw1,ip_gw_ext,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed(goto=['common_cleanup'])   


    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgaclExt(uut,ip_prefix_ext,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            import pdb;pdb.set_trace()
            self.failed()      


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()         


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()      


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            import pdb;pdb.set_trace()
            self.failed()    

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            import pdb;pdb.set_trace()
            self.failed()    

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass   
 

 

class TC001_test1_bridged_mcast(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1005,ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')



    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            #import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
 
 
class TC002_test1_routed_mcast(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        pass

     #if not esgConfigureAndTest(ixia_port_list[0],ixia_port_list[1],vlan_1005,\
        #                       vlan_1005,ip_start1,ip_start2,SG1,SG2,vrf1,vrf2,ip_gw1,ip_gw1,1,20000,esg_uut_list):
        #   self.failed()

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1006,ip_start1,ip_start3,ip_gw1,ip_gw3,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')



    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start3,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            #import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        pass
 
 
 
class TC003_test1_bridged_ingres_replicn(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        cfg = \
        """
        interface nve1
        member vni 201002-201010
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
                log.error(sys.exc_info())      
          

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,"novlan",ip_start1,ip_start2,ip_gw1,ip_gw1,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')



    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start2,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            #import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        cfg = \
        """
        interface nve1
        member vni 201002-201010
            suppress-arp            
            no ingress-replication protocol bgp
            mcast-group 239.1.1.1
        """
        for uut in esg_uut_list:
            try:
                uut.configure(cfg)
            except:
                log.error('CONFIGS FAILED FOR %r',uut)
                log.error(sys.exc_info())      
          
 
 
class TC004_test1_routed_ingres_replicn(aetest.Testcase):
   ###    This is description for my tecase two
  
    @aetest.setup
    def setup(self):
        cfg = \
        """
        interface nve1
        member vni 201002-201010
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
                log.error(sys.exc_info())      

    @aetest.test   
    def test1(self): 
        log.info("Remove feature security-group")
        global port_hdl1,port_hdl2
        if not removeSecurityGroup(esg_uut_list):
            self.failed()
        log.info("CONNECT TO IXIA")
        port_list = ixiaConnect(ixia_port_list)
        countdown(4)        
        port_hdl1 = port_list.split(' ')[0]
        port_hdl2 = port_list.split(' ')[1]

        log.info("SETUP TRAFFIC IN IXIA")
        if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan_1005,vlan_1006,ip_start1,ip_start3,ip_gw1,ip_gw3,1):
            self.failed()

        log.info("CHECK TRAFFIC RATE IN IXIA")
        if not ixiaStatCheckRate(traffic_rate1): 
            self.failed(goto=['common_cleanup')



    @aetest.test   
    def test2(self): 
        log.info("ENABLE FEATURE SECURITY GROUP")
        if not configureSecurityGroup(esg_uut_list):
            self.failed()
        #+-----------------------------------------------------------------------------------------------------------+
        #ESG-SGACL-PD-Func: 004	"Enable feature security-groups and verify no traffic drops on existing \
        # flows and verify all VRFs are in unenforced mode and verify routes 
        #programed with default tag."    
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("CONFIGURE SGACL")
        for uut in esg_uut_list:
            if not configureSgacl(uut,ip_start1,SG1,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()                 
            if not configureSgacl(uut,ip_start3,SG2,vrf1): 
                import pdb;pdb.set_trace()
                self.failed()             

        log.info("CONFIGURE PERMIT POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
                import pdb;pdb.set_trace()
                self.failed()                 

        log.info("CONFIGURE DENY POLICY") 
        for uut in esg_uut_list:
            if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("CONFIGURE ENFORCE DENY") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 007	"Configure one VRF in enforced mode and verify all data traffic\
        #  is dropped for that vrf and verify default DENY rule for the VRF,
        #and verify Control traffic (ARP/Protocol tenant traffic) is not dropped."        
        #+-----------------------------------------------------------------------------------------------------------+ 
        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test3(self): 
        log.info("CONFIGURE permit Contract unidir") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+ 
        #ESG-SGACL-PD-Func: 009	Create an ESG and add IPV4 hosts/subnets selector into it ,send ARP and\
        #make sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+                             
        #ESG-SGACL-PD-Func: 010	Create an ESG in remote switch and add IPV4 hosts/subnets into it ,send ARP and make \
        #sure endpoint IPs are learnt with proper tags.
        #+-----------------------------------------------------------------------------------------------------------+          
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            import pdb;pdb.set_trace()
            self.failed()

    @aetest.test   
    def test4(self): 

        log.info("CONFIGURE permit Contract bidi") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       
                    
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test5(self): 
        log.info("removeEsgContract") 
        for uut in esg_uut_list:
            if not removeEsgContract(uut,vrf1):
                import pdb;pdb.set_trace()
                self.failed()       
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 011	"Configure the vrf in enforced mode in remote node also.
        #Create SGACL(contract) in local and remote node add source and destination and add service policy type into it.
        #Send unicast bridged traffic between src and dst for the vrf.Do we need service-policy type required traffic to flow ?"
        #+-----------------------------------------------------------------------------------------------------------+                      
        for uut in esg_uut_list:
            if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
                import pdb;pdb.set_trace()
                self.failed()              
        #+-----------------------------------------------------------------------------------------------------------+  
        #ESG-SGACL-PD-Func: 012	"Verify Unicast bridged IPv4 traffic on EVPN- Vxlanv4 with ESG/SGACL \
        #enforcement with underlay multicast mode,
        #Show verification commands (l2-rib, bgp,rpm, fib)"
        #+-----------------------------------------------------------------------------------------------------------+  
        log.info("TEST TRAFFIC ") 
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()       


    @aetest.test   
    def test6(self):         
        log.info("CONFIGURE ENFORCE permit") 
        for uut in esg_uut_list:
            if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
                import pdb;pdb.set_trace()
                self.failed()       
            
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(int(traffic_rate1/2)): 
            #import pdb;pdb.set_trace()
            self.failed()       
     

    @aetest.test   
    def test7(self):     
        log.info("CONFIGURE deny Contract") 
        for uut in esg_uut_list:
            if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
                import pdb;pdb.set_trace()
                self.failed()       

        log.info("TEST TRAFFIC NO TRAFFIC") 
        if not ixiaStatCheckRate(rate_no_traffic): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test8(self):     
        for uut in esg_uut_list:
            if not removeSgacl(uut): 
                import pdb;pdb.set_trace()
                self.failed()       

        if not removeSecurityGroup(esg_uut_list):
            #import pdb;pdb.set_trace()
            self.failed()   
        
        if not ixiaStatCheckRate(traffic_rate1): 
            #import pdb;pdb.set_trace()
            self.failed()   

    @aetest.test   
    def test9(self):         
        for uut in esg_uut_gx:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG1]):
                self.failed()

        for uut in esg_uut_fx3:
            if not esgCheckFibL2ribAdj(uut,tag_list,[SG2]):
                self.failed()

        

    @aetest.test   
    def test2_core(self): 
        for uut in esg_uut_list:
            if not checkCore(uut):
                self.failed()


    @aetest.cleanup
    def cleanup(self):
        IxiaReset()
        cfg = \
        """
        interface nve1
        member vni 201002-201010
            suppress-arp            
            no ingress-replication protocol bgp
            mcast-group 239.1.1.1
        """
        for uut in esg_uut_list:
            try:
                uut.configure(cfg)
            except:
                log.error('CONFIGS FAILED FOR %r',uut)
                log.error(sys.exc_info())      



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








 
 