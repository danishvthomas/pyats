
#!/usr/bin/env python

# python
import logging
import unittest
from unittest.mock import Mock
from randmac import RandMac
import macaddress
import json    
import time
import os
from IxNetwork import IxNet
from ats.log.utils import banner
from netaddr import *
from pyats.async_ import pcall
from ixia_dhcp_lib import *
import sys

# Genie package
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface

# xBU-shared genie pacakge
from genie.libs.conf.interface import TunnelTeInterface
from genie.libs.conf.base import MAC, IPv4Interface, IPv6Interface, IPv4Address, IPv6Address
from genie.libs.conf.interface import Layer, L2_type, IPv4Addr, IPv6Addr,NveInterface
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
 

import re


def configureSecurityContract(uut,conf_dict): 

    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 

    SG1v6 = conf_dict["esg"]["ipv6"]["SG1"] 
    SG2v6 = conf_dict["esg"]["ipv6"]["SG2"] 
    SG3v6 = conf_dict["esg"]["ipv6"]["SG3"] 
    SG4v6 = conf_dict["esg"]["ipv6"]["SG4"]

    policy_name = conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    #direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
 
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
    if not 'enforce' in uut.execute("show running-config security-group"):
        if not esgSecEnforceAdd(uut,vrf,"1919","deny"):
            return 0 

    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """ 
    for i in range(1,scale+1):
        if i > int(scale/2):
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  unidir\n' 

        else:    
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name} bidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name} bidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name} bidir\n'           
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  bidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  bidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  bidir\n' 

        SG1 = str(int(SG1)+1) 
        SG2 = str(int(SG2)+1) 
        SG3 = str(int(SG3)+1)             
        SG1v6 = str(int(SG1v6)+1) 
        SG2v6 = str(int(SG2v6)+1) 
        SG3v6 = str(int(SG3v6)+1)    
    try:
        uut.configure(cfg)
    except:
        return 0  


def configureSecurityContractDeny(uut,conf_dict): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    policy_name = "deny_all"
    SG1v6 = conf_dict["esg"]["ipv6"]["SG1"] 
    SG2v6 = conf_dict["esg"]["ipv6"]["SG2"] 
    SG3v6 = conf_dict["esg"]["ipv6"]["SG3"] 
    SG4v6 = conf_dict["esg"]["ipv6"]["SG4"]
    #conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    #direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
 
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):

    if not 'enforce' in uut.execute("show running-config security-group"):
        if not esgSecEnforceAdd(uut,vrf,"1919","permit"):
            return 0 

    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """
    
    for i in range(1,scale+1):
        if i > int(scale/2):
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  unidir\n' 
        else:    
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name} bidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name} bidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name} bidir\n'           
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  bidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  bidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  bidir\n' 

        SG1 = str(int(SG1)+1) 
        SG2 = str(int(SG2)+1) 
        SG3 = str(int(SG3)+1)             
        SG1v6 = str(int(SG1v6)+1) 
        SG2v6 = str(int(SG2v6)+1) 
        SG3v6 = str(int(SG3v6)+1)    

    try:
        uut.configure(cfg)
    except:
        return 0  




def configureSecurityContract2(uut,conf_dict): 

    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 

    SG1v6 = conf_dict["esg"]["ipv6"]["SG1"] 
    SG2v6 = conf_dict["esg"]["ipv6"]["SG2"] 
    SG3v6 = conf_dict["esg"]["ipv6"]["SG3"] 
    SG4v6 = conf_dict["esg"]["ipv6"]["SG4"]

    policy_name = conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    #direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
 
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
    if not 'enforce' in uut.execute("show running-config security-group"):
        if not esgSecEnforceAdd(uut,vrf,"1919","deny"):
            return 0 

    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """ 
    for i in range(1,scale+1):
        if i > int(scale/2):
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  unidir\n' 

        else:    
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name} bidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name} bidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name} bidir\n'           
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  bidir\n'            
            cfg += f'security contract source {SG1v6} destination {SG3v6} policy {policy_name}  bidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  bidir\n' 

        SG1 = str(int(SG1)+1) 
        SG2 = str(int(SG2)+1) 
        SG3 = str(int(SG3)+1)             
        SG1v6 = str(int(SG1v6)+1) 
        SG2v6 = str(int(SG2v6)+1) 
        SG3v6 = str(int(SG3v6)+1)    
    try:
        uut.configure(cfg)
    except:
        return 0  


def configureSecurityContractDeny2(uut,conf_dict): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    policy_name = "deny_all"
    SG1v6 = conf_dict["esg"]["ipv6"]["SG1"] 
    SG2v6 = conf_dict["esg"]["ipv6"]["SG2"] 
    SG3v6 = conf_dict["esg"]["ipv6"]["SG3"] 
    SG4v6 = conf_dict["esg"]["ipv6"]["SG4"]
    #conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    #direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
 
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):

    if not 'enforce' in uut.execute("show running-config security-group"):
        if not esgSecEnforceAdd(uut,vrf,"1919","permit"):
            return 0 

    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """
    
    for i in range(1,scale+1):
        if i > int(scale/2):
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  unidir\n'            
            cfg += f'security contract source {SG2v6} destination {SG4v6} policy {policy_name}  unidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  unidir\n' 
        else:    
            cfg += f'security contract source {SG1} destination {SG2} policy {policy_name} bidir\n'            
            cfg += f'security contract source {SG1} destination {SG3} policy {policy_name} bidir\n' 
            cfg += f'security contract source {SG1} destination {SG4} policy {policy_name} bidir\n'           
            cfg += f'security contract source {SG1v6} destination {SG2v6} policy {policy_name}  bidir\n'            
            cfg += f'security contract source {SG2v6} destination {SG4v6} policy {policy_name}  bidir\n' 
            cfg += f'security contract source {SG1v6} destination {SG4v6} policy {policy_name}  bidir\n' 

        SG1 = str(int(SG1)+1) 
        SG2 = str(int(SG2)+1) 
        SG3 = str(int(SG3)+1)             
        SG1v6 = str(int(SG1v6)+1) 
        SG2v6 = str(int(SG2v6)+1) 
        SG3v6 = str(int(SG3v6)+1)    

    try:
        uut.configure(cfg)
    except:
        return 0  



def configureEsgContract(uut,conf_dict,direction): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    policy_name = conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    #direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
 
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
        
    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """
    
    for i in range(scale):
        cfg += f'security contract source {SG1} destination {SG2} policy {policy_name}  {direction}\n'            
        cfg += f'security contract source {SG1} destination {SG3} policy {policy_name}  {direction}\n' 
        cfg += f'security contract source {SG1} destination {SG4} policy {policy_name}  {direction}\n'           
        SG1 = str(int(SG1)+1) 
        SG2 = str(int(SG2)+1) 
        SG3 = str(int(SG3)+1) 
    try:
        uut.configure(cfg)
    except:
        return 0     
                
def esgRestart(esg_uut_list): 
    if not configureSecurityGroup(esg_uut_list):
        return 0
    log.info("CONFIGURE SGACL")
    for uut in esg_uut_list:
        uut.configure("system no hap-reset")
        if not configureSgacl(uut,ip_start1,SG1,vrf1): 
            return 0               
        if not configureSgacl(uut,ip_start2,SG2,vrf1): 
            return 0                             
        if not configureSgacl(uut,ip_start3,SG3,vrf1): 
            return 0              
        if not configureSgaclExt(uut,ip_prefix_ext,SG4,vrf1): 
            return 0    

    log.info("CONFIGURE PERMIT POLICY") 
    for uut in esg_uut_list:
        if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
            return 0                    

    log.info("CONFIGURE DENY POLICY") 
    for uut in esg_uut_list:
        if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
            return 0          



def policyRemoveAdd(uut):
    pass
    """
    gx001# sh contracts | json-pretty
    {
        "TABLE_vrf": {
            "ROW_vrf": {
                "vrf": "vxlan-900101",
                "TABLE_contract": {
                    "ROW_contract": [
                        {
                            "sgt": "11111",
                            "dgt": "22222",
                            "policy": "permit_all",
                            "dir": "bidir",
                            "TABLE_class": {
                                "ROW_class": {
                                    "class": "permit_all",
                                    "permitdeny": "permit",
                                    "oper-state": "enabled",
                                    "stats": "0"
                                }
                            }
                        },
                        {
                            "sgt": "11111",
                            "dgt": "33333",
                            "policy": "permit_all",
                            "dir": "bidir",
                            "TABLE_class": {
                                "ROW_class": {
                                    "class": "permit_all",
                                    "permitdeny": "permit",
                                    "oper-state": "enabled",
                                    "stats": "0"
                                }
                            }
                        },
                        {
                            "sgt": "11111",
                            "dgt": "44444",
                            "policy": "permit_all",
                            "dir": "bidir",
                            "TABLE_class": {
                                "ROW_class": {
                                    "class": "permit_all",
                                    "permitdeny": "permit",
                                    "oper-state": "enabled",
                                    "stats": "0"
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
    """
    
def configureSgacl(uut,conf_dict): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    Policy = conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    Class = conf_dict["esg"]["contract_permit_bidir"]["Class"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
    ip_start1 = conf_dict["esg"]["contract_permit_bidir"]["ip_start1"] 
    ip_start2 = conf_dict["esg"]["contract_permit_bidir"]["ip_start2"] 
    ip_start3 = conf_dict["esg"]["contract_permit_bidir"]["ip_start3"] 
    ip_start_ext = conf_dict["esg"]["contract_permit_bidir"]["ip_start_ext"] 
    ip_prefix_ext = conf_dict["esg"]["contract_permit_bidir"]["ip_prefix_ext"] 
    #for vlan,vni in zip(range(vlan,vlan+count),range(vni,vni+count)):
    for i in range(scale):
        for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
            cfg += f'security-group  {SG}  name SG{SG} \n'
            cfg += f'match connected-endpoints vrf {vrf} ipv4 {IP}/32   \n'         
            #cfg += f'match host vrf {vrf} ipv4 {IP}/32   \n'              
        SG1 = str(int(SG1)+1)
        ip_start1 = str(IPAddress(ip_start1)+1)
        SG2 = str(int(SG2)+1)
        ip_start2 = str(IPAddress(ip_start2)+1)
        SG3 = str(int(SG3)+1)
        ip_start3 = str(IPAddress(ip_start3)+1)
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        return 0   
    
    if not configureSgaclExt(uut,ip_prefix_ext,SG4,vrf): 
        return 0
    return 1  



def configureSgaclV6(uut,conf_dict): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["ipv6"]["vrf"] 
    SG1 = conf_dict["esg"]["ipv6"]["SG1"] 
    SG2 = conf_dict["esg"]["ipv6"]["SG2"] 
    SG3 = conf_dict["esg"]["ipv6"]["SG3"] 
    SG4 = conf_dict["esg"]["ipv6"]["SG4"] 
    vrf = conf_dict["esg"]["ipv6"]["vrf"] 
    Policy = conf_dict["esg"]["ipv6"]["Policy"] 
    Class = conf_dict["esg"]["ipv6"]["Class"] 
    scale = conf_dict["esg"]["ipv6"]["scale"] 
    direction = conf_dict["esg"]["ipv6"]["direction"] 
    ip_start1 = conf_dict["esg"]["ipv6"]["ip_start1"] 
    ip_start2 = conf_dict["esg"]["ipv6"]["ip_start2"] 
    ip_start3 = conf_dict["esg"]["ipv6"]["ip_start3"] 
    ip_start_ext = conf_dict["esg"]["ipv6"]["ip_start_ext"] 
    ip_prefix_ext = conf_dict["esg"]["ipv6"]["ip_prefix_ext"] 
    #for vlan,vni in zip(range(vlan,vlan+count),range(vni,vni+count)):
    for i in range(scale):
        for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
            cfg += f'security-group  {SG}  name SG{SG} \n'
            #cfg += f'match host vrf {vrf} ipv6 {IP}/128   \n'  
            cfg += f'match connected-endpoints vrf {vrf} ipv6 {IP}/128   \n'                      
        SG1 = str(int(SG1)+1)
        ip_start1 = str(IPAddress(ip_start1)+1)
        SG2 = str(int(SG2)+1)
        ip_start2 = str(IPAddress(ip_start2)+1)
        SG3 = str(int(SG3)+1)
        ip_start3 = str(IPAddress(ip_start3)+1)
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        return 0   
    
    if not configureSgaclExtV6(uut,ip_prefix_ext,SG4,vrf): 
        return 0
    return 1  

def configureSgaclBK(uut,ip1,SG,vrf): 
    #uut,ip_start1,SG1,vrf1
    cfg = \
    """

    """
    cfg += f'security-group  {SG}  name SG{SG} \n'
    cfg += f'match host vrf {vrf} ipv4 {ip1}/32   \n'

    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())   
        return 0 
    return 1 


def configureSgaclExt(uut,ip1,SG,vrf): 
    cfg = \
    """

    """
    cfg += f'security-group  {SG}  name SG{SG} \n'
    #cfg += f'match external vrf {vrf} ipv4 {ip1}\n'
    cfg += f'match external-subnets vrf {vrf} ipv4 {ip1}\n'
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())   
        return 0 
    return 1 

def configureSgaclExtV6(uut,ip1,SG,vrf): 
    cfg = \
    """

    """
    cfg += f'security-group  {SG}  name SG{SG} \n'
    #cfg += f'match external vrf {vrf} ipv6 {ip1}\n'
    cfg += f'match external-subnets vrf {vrf} ipv6 {ip1}\n'
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())   
        return 0 
    return 1 


def removeSgacl(uut): 
    op1 = uut.execute("show running-config security-group")   
    cfg = \
    """

    """
    tag_list = []
    for line in op1.splitlines():
        if not 'feature' in line:
            if 'security-group' in line:
                if not 'Command' in line:
                    cfg += f'no {line}  \n'   
        
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info()) 
        return 0     
    return 1

 
def configReplaceEsg1(uut,cli):
    try:
        uut.configure('delete bootflash:cr1 no-promp',timeout = 180)
        countdown(2)
        uut.configure('copy running-config bootflash:cr1',timeout = 180)
        countdown(2)
        uut.configure(cli)
        countdown(2)
        uut.configure('configure replace bootflash:cr1 verbose',timeout = 180)
    except:
        log.info(f"CR FAILED for UUT {uut}")
        return 0 
    return 1

 


def vxlanEsgAllReset(uut):
    log.info(banner("starting VxlanStReset"))
    cfg = \
    """
    clear ipv6 neighbor vrf all  
    clear ip arp vrf all  
    clear mac add dynamic       
    """
    try:
        uut.configure(cfg)
        countdown(20)
    except:
        log.info(f"vxlanEsgAllReset FAILED for UUT {uut}")
        return 0 
    return 1 


def vxlanEsgAllResetBk(uut):
    log.info(banner("starting VxlanStReset"))
    try:
        cfgEsg = uut.execute("show run security-group  | b featu")
        uut.configure("no feature security-group")
        countdown(2)
        uut.configure(cfgEsg)
    except:
        log.info(f"vxlanEsgAllReset FAILED for UUT {uut}")
        return 0 
    countdown(20)
    return 1 

def configSecurityGroup(uut):
    log.info("Enable feature security-group") 
    uut.configure("no feature security-group") 
    uut.configure("feature security-group") 
    if not "Applied System Routing Mode: Security-Groups Support" in uut.configure("sh system routing mode | json-pretty "):
        return 0
    #if not "security-group" in uut.configure("sh run | inc feature"):
    #    return 0
    if not "Feature Security Group enabled: TRUE" in uut.configure(" show system internal adjmgr internal info | inc Sec"):
        return 0
    if not "Feature Security Group enabled: TRUE" in uut.configure(" show ip arp internal info | inc Sec"):
        return 0
    return 1

def configureSecurityGroup(uut_list):
    for uut in uut_list:
        log.info("Enable feature security-group") 
        uut.configure("no feature security-group") 
        uut.configure("feature security-group") 
    for uut in uut_list:
        if not "Applied System Routing Mode: Security-Groups Support" in uut.configure("sh system routing mode | json-pretty "):
            return 0
    #for uut in uut_list:
    #    if not "security-group" in uut.configure("sh run | inc feature"):
    #        return 0
    for uut in uut_list:
        if not "Feature Security Group enabled: TRUE" in uut.configure(" show system internal adjmgr internal info | inc Sec"):
            return 0
    for uut in uut_list:
        if not "Feature Security Group enabled: TRUE" in uut.configure(" show ip arp internal info | inc Sec"):
            return 0
    return 1

def removeSecurityGroup(uut_list):
    for uut in uut_list:
        if  "Feature Security Group enabled: TRUE" in uut.configure(" show system internal adjmgr internal info | inc Sec"):
            log.info("Remove feature security-group") 
            uut.configure("no feature security-group") 
    
    #for uut in uut_list:
    #    if "security-group" in uut.configure("sh run | inc feature"):
    #        return 0
    for uut in uut_list:
        if "Feature Security Group enabled: TRUE" in uut.configure(" show system internal adjmgr internal info | inc Sec"):
            return 0
    for uut in uut_list:
        if  "Feature Security Group enabled: TRUE" in uut.configure(" show ip arp internal info | inc Sec"):
            return 0
    return 1

 
 
def configureEsgPolicy(uut,className,policyName,action):
    cfg = \
    f"""
    class-map type security match-any {className}
    match ip
    
    policy-map type security {policyName}
    class {className}
    {action}
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1


def removeAddClass(uut,className,policyName,action):
    cfg = \
    f"""
    policy-map type security {policyName}
    no class {className}
    no class-map type security match-any {className}
    sleep 4        
    class-map type security match-any {className}
    match ip    
    policy-map type security {policyName}
    class {className}
    {action}
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1


def removeAddPolicyContract(uut,className,policyName,action):
    cfg = \
    f"""
    vrf context vxlan-900101
    no vni 900101
    no security contract source 11111 destination 22222 policy permit_all 
    no security contract source 11111 destination 33333 policy permit_all 
    no security contract source 11111 destination 44444 policy permit_all 
    sleep 4
    no policy-map type security {policyName}
    sleep 4            
    policy-map type security {policyName}
    class {className}
    {action}
    vrf context vxlan-900101
    vni 900101
    security contract source 11111 destination 22222 policy permit_all 
    security contract source 11111 destination 33333 policy permit_all 
    security contract source 11111 destination 44444 policy permit_all 
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1

def removeAddMatchInClass(uut,className,policyName,action):
    cfg = \
    f"""    
    class-map type security match-any {className}
    no match ip    
    sleep 5
    match ip  
    policy-map type security {policyName}
    class {className}
    {action}
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1

def removeAddClassFromPolicy(uut,className,policyName,action):
    cfg = \
    f"""
    policy-map type security {policyName}
    no class {className}
    sleep 4
    class {className}
    {action}
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0  
    return 1



def removeEsgPolicy(uut,className,policyName):
    cfg = \
    f"""    
    no policy-map type security {policyName}

    no class-map type security match-any {className}
    """
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1
  


def removeEsgContract(uut,vrf):
    cfg = \
    f"""
    vrf context {vrf}
    """

    op1 = uut.execute("show run security-group | inc 'security contract'")

    for line in op1.splitlines():
        if 'contract' in line:
           cfg += f'no {line} \n'

    try:
        uut.configure(cfg)
    except:
        return 0       
    return 1  




def configureEsgContractUnidir(uut,conf_dict): 
    cfg = \
    """

    """
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    SG1 = conf_dict["esg"]["contract_permit_bidir"]["SG1"] 
    SG2 = conf_dict["esg"]["contract_permit_bidir"]["SG2"] 
    SG3 = conf_dict["esg"]["contract_permit_bidir"]["SG3"] 
    SG4 = conf_dict["esg"]["contract_permit_bidir"]["SG4"] 
    vrf = conf_dict["esg"]["contract_permit_bidir"]["vrf"] 
    policy_name = conf_dict["esg"]["contract_permit_bidir"]["Policy"] 
    Class = conf_dict["esg"]["contract_permit_bidir"]["Class"] 
    scale = conf_dict["esg"]["contract_permit_bidir"]["scale"] 
    direction = conf_dict["esg"]["contract_permit_bidir"]["direction"] 
    ip_start1 = conf_dict["esg"]["contract_permit_bidir"]["ip_start1"] 
    ip_start2 = conf_dict["esg"]["contract_permit_bidir"]["ip_start2"] 
    ip_start3 = conf_dict["esg"]["contract_permit_bidir"]["ip_start3"] 
    ip_start_ext = conf_dict["esg"]["contract_permit_bidir"]["ip_start_ext"] 
    ip_prefix_ext = conf_dict["esg"]["contract_permit_bidir"]["ip_prefix_ext"] 
    #for vlan,vni in zip(range(vlan,vlan+count),range(vni,vni+count)):
    #for SG,IP in zip([SG1,SG2,SG3],[ip_start1,ip_start2,ip_start3]):
    direction = 'unidir'    

    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """
    checkList = []
    
    for source,destination in zip([SG1,SG1,SG1],[SG2,SG3,SG4]): 
        contracts = uut.execute("show run security-group")
        if 'bidir' in direction:
            check = f'security contract source {source} destination {destination} policy {policy_name}'       
        elif 'unidir' in direction:
            check = f'security contract source {source} destination {destination} policy {policy_name} unidir'
        if not check in contracts: 
            for i in range(scale):
                cfg += f'security contract source {source} destination {destination} policy {policy_name}  {direction}\n'
                source = str(int(source)+1)
                destination = str(int(destination)+1) 
            try:
                uut.configure(cfg)
            except:
                return 0       
    return 1

def configureEsgContractAll(uut,vrf,SG1,SG2,SG3,SG4,policyName,scale,direction):
    if not configureEsgContract(uut,vrf,SG1,SG2,policyName,scale,direction):
        return 0      
    if not configureEsgContract(uut,vrf,SG1,SG3,policyName,scale,direction):
        return 0      
    if not configureEsgContract(uut,vrf,SG1,SG4,policyName,scale,direction):
        return 0    
    return 1

def configureEsgContractBK(uut,vrf,source,destination,policyName,scale,direction):
    cfg = \
    f"""
    logging ip access-list include sgt
    vrf context {vrf}
    """
    checkList = []
    contracts = uut.execute("show run security-group")
    if 'bidir' in direction:
        check = f'security contract source {source} destination {destination} policy {policyName}'       
    elif 'unidir' in direction:
        check = f'security contract source {source} destination {destination} policy {policyName} unidir'
    if not check in contracts: 
        for i in range(scale):
            cfg += f'security contract source {source} destination {destination} policy {policyName}  {direction}\n'
            source = str(int(source)+1)
            destination = str(int(destination)+1) 
            # pass -- security contract source 4444 destination 7777 policy AAA bidir 
            # fail -- security contract source 4444 destination 7777 policy permit_all permit unidir
        try:
            uut.configure(cfg)
        except:
            return 0       
    return 1



def removeAddSgacl(uut):
    cfg1 = \
    """
    """
    cfg2 = \
    """
    """
    cfg = uut.execute("show run security-group  | sec security-group")
    for line in cfg.splitlines():
        if not 'Command' in line:
            if not 'feature' in line:
                if 'security-group' in line:
                    cfg1 += f"no {line} \n"
                cfg2 += f"{line} \n"

    uut.configure(cfg1)
    countdown(2)
    uut.configure(cfg2)    
    countdown(2)


def removeAddSelector(uut):
    cfg1 = \
    """
    """
    cfg2 = \
    """
    """
    cfg = uut.execute("show run security-group  | sec security-group")
    for line in cfg.splitlines():
        if not 'feature' in line:
            cfg1 += f"{line} \n"
            if 'match host vrf ' in line:
                cfg1 += f"no {line} \n"
            cfg2 += f"{line} \n"

    uut.configure(cfg1)
    countdown(2)
    uut.configure(cfg2)    
    countdown(2)


def esgCheckFibL2ribAdj(uut,tag_list,local_tag_list):
    out1 = uut.execute("show fabric forwarding internal ip local-host-db vrf all")
    out2 = uut.execute("show ip adjacency detail vrf all  ")
    out3= uut.execute("show ip route detail vrf vxlan-900101")
    out4 = uut.execute("show l2route evpn mac-ip all")
    result = []
    for tag in local_tag_list:
        if not tag in out1:
            log.info('tag not fount in {out1}')
            #import pdb;pdb.set_trace()
        if not tag in out2:
            log.info('tag not fount in {out2}')
            #import pdb;pdb.set_trace()
    for tag in tag_list:
        if not tag in out3:
            log.info('tag not fount in {out3}')
            #import pdb;pdb.set_trace()
        if not tag in out4:
            log.info('tag not fount in {out4}')
            #import pdb;pdb.set_trace()
    if 'fail' in result:
        return 0
    else:
        return 1   


def esgSecEnforceAdd(uut,vrf,tag,action):
    cfg = \
    f"""
    vrf context {vrf}
    security enforce tag {tag} default {action} 
    """   
    try:
        if not f'security enforce tag {tag} default {action}' in uut.execute(f'show run vrf {vrf}'):
            uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info())
        return 0     
    return 1
def esgSecEnforceRemove(uut,vrf,tag,action):
    cfg = \
    f"""
    vrf context {vrf}
    no security enforce tag {tag}  default {action} 
    """   
    try:
        uut.configure(cfg)
    except:
        log.error('CONFIGS FAILED FOR %r',uut)
        log.error(sys.exc_info()) 
        return 0      
    return 1
def esgConfigureAndTest(port1,port2,vlan1,vlan2,ip1,ip2,SG1,SG2,\
                        vrf1,vrf2,gw1,gw2,scale,rate,uut_list):
    

    log.info("Remove feature security-group")
    if not removeSecurityGroup(uut_list):
        return 0

    log.info("CONNECT TO IXIA")

    rate_no_traffic = int(rate*0.01)

    port_list = ixiaConnect([port1,port2])


    countdown(4)
         
    port_hdl1 = port_list.split(' ')[0]
    port_hdl2 = port_list.split(' ')[1]


    log.info("SETUP TRAFFIC IN IXIA")
    if not ixiaTrafficSetupEsg(port_hdl1,port_hdl2,vlan1,vlan2,ip1,ip2,gw1,gw2,scale):
        return 0


    log.info("CHECK TRAFFIC RATE IN IXIA")
    if not ixiaStatCheckRate(rate): 
        return 0 

    log.info("ENABLE FEATURE SECURITY GROUP")
    if not configureSecurityGroup(uut_list):
        return 0


    log.info("CONFIGURE SGACL")
    for uut in uut_list:
        if not configureSgacl(uut,ip1,SG1,vrf1): 
            return 0        
        if not configureSgacl(uut,ip2,SG2,vrf2): 
            return 0    


    log.info("CONFIGURE PERMIT POLICY") 
    for uut in uut_list:
        if not  configureEsgPolicy(uut,"permit_all","permit_all","permit"): 
            return 0        


    log.info("CONFIGURE DENY POLICY") 
    for uut in uut_list:
        if not  configureEsgPolicy(uut,"deny_all","deny_all","deny"): 
            return 0  


    log.info("CONFIGURE ENFORCE DENY") 
    for uut in uut_list:
        if not esgSecEnforceAdd(uut,vrf1,"1919","deny"):
            return 0  


    log.info("TEST TRAFFIC NO TRAFFIC") 
    if not ixiaStatCheckRate(rate_no_traffic): 
        return 0

    log.info("CONFIGURE permit Contract unidir") 
    for uut in uut_list:
        if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"unidir"):
            return 0  
                
    log.info("TEST TRAFFIC ") 
    if ixiaStatCheckRate(int(rate/2)): 
        import pdb;pdb.set_trace()
        return 0

    log.info("CONFIGURE permit Contract bidi") 
    for uut in uut_list:
        if not configureEsgContract(uut,vrf1,SG1,SG2,"permit_all",1,"bidir"):
            return 0  
                
    log.info("TEST TRAFFIC ") 
    if not ixiaStatCheckRate(rate): 
        return 0
    
    log.info("removeEsgContract") 
    for uut in uut_list:
        if not removeEsgContract(uut):
            return 0  
    
    for uut in uut_list:
        if not esgSecEnforceRemove(uut,vrf1,"1919","deny"):
            return 0     

    log.info("TEST TRAFFIC ") 
    if not ixiaStatCheckRate(rate): 
        return 0
    
    log.info("CONFIGURE ENFORCE permit") 
    for uut in uut_list:
        if not esgSecEnforceAdd(uut,vrf1,"1919","permit"):
            return 0  
        
    log.info("TEST TRAFFIC NO TRAFFIC") 
    if not ixiaStatCheckRate(rate): 
        return 0

    log.info("CONFIGURE deny Contract") 
    for uut in uut_list:
        if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"unidir"):
            return 0  

    log.info("TEST TRAFFIC NO TRAFFIC") 
    if not ixiaStatCheckRate(int(rate/2)): 
        return 0        

    log.info("CONFIGURE deny Contract") 
    for uut in uut_list:
        if not configureEsgContract(uut,vrf1,SG1,SG2,"deny_all",1,"bidir"):
            return 0  

    log.info("TEST TRAFFIC NO TRAFFIC") 
    if not ixiaStatCheckRate(rate_no_traffic): 
        return 0

    for uut in uut_list:
        if not removeSgacl(uut): 
            return 0  

    if not removeSecurityGroup(uut_list):
        return 0  
    
    if not ixiaStatCheckRate(rate): 
        return 0

    IxiaReset()
    return 1
    
 
 
   
    
    
