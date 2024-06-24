 
feature telnet
feature nxapi
feature bash-shell
feature ngmvpn
nv overlay evpn
feature ospf
feature bgp
feature pim
feature pim6
feature fabric forwarding
feature interface-vlan
feature vn-segment-vlan-based
feature lacp
feature lldp
feature bfd
feature nv overlay
feature container-tracker



ip access-list ANY
  10 permit ip any any
mac access-list FHS
  statistics per-entry
  10 deny any any
ip access-list type5
  10 permit ip any any
ip access-list type55
  10 permit ip any any
ip access-list type5555
  10 permit ip any any
class-map type qos match-any ALL
  match access-group name ANY
class-map type qos match-all sgacl-ipv4-class
policy-map type qos ANY
  class ALL
copp profile strict

ntp server 10.64.58.51 use-vrf management
ntp server 72.163.32.44 use-vrf management

fabric forwarding anycast-gateway-mac 0000.2222.3333
fabric forwarding dup-host-ip-addr-detection 2 60
ip pim rp-address 100.1.1.100 group-list 224.0.0.0/4
ip pim ssm range 232.0.0.0/8
ip pim pre-build-spt
ip igmp snooping vxlan
vlan 1,101-102,1001-1020,3001
vlan 101
  vn-segment 900101
vlan 102
  vn-segment 900102
vlan 1001
  vn-segment 201001
vlan 1002
  vn-segment 201002
vlan 1003
  vn-segment 201003
vlan 1004
  vn-segment 201004
vlan 1005
  vn-segment 201005
vlan 1006
  vn-segment 201006
vlan 1007
  vn-segment 201007
vlan 1008
  vn-segment 201008
vlan 1009
  vn-segment 201009
vlan 1010
  vn-segment 201010
vlan 1011
  vn-segment 201011
vlan 1012
  vn-segment 201012
vlan 1013
  vn-segment 201013
vlan 1014
  vn-segment 201014
vlan 1015
  vn-segment 201015
vlan 1016
  vn-segment 201016
vlan 1017
  vn-segment 201017
vlan 1018
  vn-segment 201018
vlan 1019
  vn-segment 201019
vlan 1020
  vn-segment 201020

ip prefix-list TYPE5 seq 5 permit 145.1.0.0/16
ip prefix-list TYPE5 seq 10 permit 0.0.0.0/0 le 32
ip prefix-list anyip seq 5 permit 0.0.0.0/0
ip prefix-list evpn seq 5 permit 0.0.0.0/16 le 32
route-map AAAA permit 10
  match ip address any
  match route-type internal
route-map RMAP_PERMIT_ALL permit 10
  match ip address prefix-list anyip evpn
  match route-type internal
route-map TYPE52 permit 10
  match ip address prefix-list TYPE5
route-map bgpToOspf permit 10
  match ip address type5555
route-map no-pim-neighbor deny 10
  match ip address prefix-list anyip
route-map ospfToBgp permit 10
  match ip address type5555
  match route-type internal
route-map ssm-1 permit 10
  match ip multicast group 232.0.0.0/8
route-map ssm-1 permit 11
  match ip multicast group 233.0.0.0/8
vrf context 1
  vni 3003001
  address-family ipv4 unicast
vrf context management
  ip route 0.0.0.0/0 10.197.127.1
vrf context vxlan-900101
  vni 900101
  ip pim rp-address 1.2.3.111 group-list 224.0.0.0/4
  ip pim ssm route-map ssm-1
  rd auto
  address-family ipv4 unicast
    route-target both auto
    route-target both auto mvpn
    route-target both auto evpn
    route-target import 100:100
    route-target import 100:100 evpn
    route-target export 100:200
    route-target export 100:200 evpn
  address-family ipv6 unicast
    route-target both auto
    route-target both auto evpn
    route-target import 100:100
    route-target import 100:100 evpn
    route-target export 100:200
    route-target export 100:200 evpn
vrf context vxlan-900102
  vni 900102
  ip pim rp-address 1.2.3.111 group-list 224.0.0.0/4
  ip pim ssm route-map ssm-1
  rd auto
  address-family ipv4 unicast
    route-target both auto
    route-target both auto mvpn
    route-target both auto evpn
    route-target import 100:200
    route-target import 100:200 evpn
    route-target export 100:100
    route-target export 100:100 evpn
  address-family ipv6 unicast
    route-target both auto
    route-target both auto evpn
    route-target import 100:200
    route-target import 100:200 evpn
    route-target export 100:100
    route-target export 100:100 evpn


interface Vlan1

interface Vlan101
  no shutdown
  vrf member vxlan-900101
  ip forward
  ip pim sparse-mode

interface Vlan102
  no shutdown
  vrf member vxlan-900102
  ip forward
  ip pim sparse-mode

interface Vlan1001
  no shutdown
  vrf member vxlan-900101
  ip address 4.1.0.1/16
  ipv6 address 4:0:0:1::1/96
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1002
  no shutdown
  vrf member vxlan-900101
  ip address 4.2.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1003
  no shutdown
  vrf member vxlan-900101
  ip address 4.3.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1004
  no shutdown
  vrf member vxlan-900101
  ip address 4.4.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1005
  no shutdown
  vrf member vxlan-900101
  ip address 4.5.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1006
  no shutdown
  vrf member vxlan-900101
  ip address 4.6.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1007
  no shutdown
  vrf member vxlan-900101
  ip address 4.7.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1008
  no shutdown
  vrf member vxlan-900101
  ip address 4.8.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1009
  no shutdown
  vrf member vxlan-900101
  ip address 4.9.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1010
  no shutdown
  vrf member vxlan-900101
  ip address 4.10.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1011
  no shutdown
  vrf member vxlan-900102
  ip address 4.11.0.1/16
  ipv6 address 4:0:0:1::2801/96
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1012
  no shutdown
  vrf member vxlan-900102
  ip address 4.12.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1013
  no shutdown
  vrf member vxlan-900102
  ip address 4.13.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1014
  no shutdown
  vrf member vxlan-900102
  ip address 4.14.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1015
  no shutdown
  vrf member vxlan-900102
  ip address 4.15.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1016
  no shutdown
  vrf member vxlan-900102
  ip address 4.16.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1017
  no shutdown
  vrf member vxlan-900102
  ip address 4.17.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1018
  no shutdown
  vrf member vxlan-900102
  ip address 4.18.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1019
  no shutdown
  vrf member vxlan-900102
  ip address 4.19.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface Vlan1020
  no shutdown
  vrf member vxlan-900102
  ip address 4.20.0.1/16
  ip pim sparse-mode
  ip pim neighbor-policy no-pim-neighbor
  fabric forwarding mode anycast-gateway

interface port-channel11
  description vpc 11
  switchport
  switchport mode trunk
  switchport trunk allowed vlan 1005-1006,1015-1016
  spanning-tree port type edge trunk

interface nve1
  no shutdown
  host-reachability protocol bgp
  advertise virtual-rmac
  source-interface loopback0
  member vni 201001
    suppress-arp
    ingress-replication protocol bgp
  member vni 201002-201010
    suppress-arp
    mcast-group 239.1.1.1
  member vni 201011-201019
    suppress-arp
    mcast-group 239.1.1.2
  member vni 900101 associate-vrf
  member vni 900102 associate-vrf

   
 
interface Ethernet1/21
  description To spine11
  mtu 9126
  medium p2p
  ip unnumbered loopback0
  ip ospf network point-to-point
  ip ospf mtu-ignore
  ip router ospf UNDERLAY area 0.0.0.0
  ip pim sparse-mode
  no shutdown
   
   

interface loopback0
  ip address 10.1.1.31/32
  ip router ospf UNDERLAY area 0.0.0.0
  ip pim sparse-mode

interface loopback1
  ip address 10.1.1.32/32
  ip router ospf UNDERLAY area 0.0.0.0
  ip pim sparse-mode

interface loopback2
  ip address 10.1.1.33/32
  ip router ospf UNDERLAY area 0.0.0.0
  ip pim sparse-mode

interface loopback99
  vrf member vxlan-900101
  ip address 99.1.1.13/32

interface loopback111
  description Overlay VRF RP Loopback interface
  vrf member vxlan-900101
  ip address 1.2.3.111/32

interface loopback112
  description Overlay VRF RP Loopback interface
  vrf member vxlan-900102
  ip address 1.2.3.112/32
  ip pim sparse-mode
 

router ospf 45
  vrf vxlan-900101
    redistribute bgp 65001 route-map ospfToBgp
router ospf UNDERLAY
  router-id 1.1.1.31
  log-adjacency-changes detail
router bgp 65001
  router-id 10.1.1.32
  address-family ipv4 mvpn
    maximum-paths 32
    retain route-target all
  address-family l2vpn evpn
    advertise-pip
  neighbor 100.1.1.11
    bfd
    remote-as 65001
    update-source loopback1
    address-family ipv4 mvpn
      send-community
      send-community extended
    address-family l2vpn evpn
      send-community
      send-community extended
  neighbor 100.1.1.21
    bfd
    remote-as 65001
    update-source loopback1
    address-family ipv4 mvpn
      send-community
      send-community extended
    address-family l2vpn evpn
      send-community
      send-community extended
  vrf vxlan-900101
    address-family ipv4 unicast
      network 99.1.1.13/32
      advertise l2vpn evpn
      redistribute direct route-map bgpToOspf
      redistribute ospf 45 route-map bgpToOspf
  vrf vxlan-900102
    address-family ipv4 unicast
      advertise l2vpn evpn
evpn
  vni 201001 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201002 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201003 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201004 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201005 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201006 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201007 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201008 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201009 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201010 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201011 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201012 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201013 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201014 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201015 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201016 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201017 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201018 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201019 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 201020 l2
    rd auto
    route-target import auto
    route-target export auto
 