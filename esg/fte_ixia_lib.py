
'''
class IXIA_traffic
    control_ixia_traffic
    collect_ixia_stats
    check_traffic_loss
    ixia_port_handles
    ixia_send_ipv4_arp

'''
import logging
from common_utils.fte_utils_lib import ForkedPdb
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



##########################################################################
#This class is for generic IXIA traffic config or control
# All ixia related operations can be declared under this
#
##########################################################################
class IXIA_traffic(object):
   
    """ Common class for IXIA Traffic  """

    #*********************************************************************#
    #This function is to start , stop traffic and clear stats on ixia
    #options supported are start, stop, clear stats
    #port handle can be list of rx and tx port handles
    #
    #*********************************************************************#
    def control_ixia_traffic(self,ixia_handle,port_handle,action):    
        """This function is to Start or Stop IXIA streams and clear stats """     
     
        if action == "start":
            ### Starting traffic
            ret = ixia_handle.traffic_control(port_handle=port_handle,action='run')
            if ret.status != '1':
                print(ret)
                return 0
            else:
                log.info("#### Started Traffic Successfully ####")
        elif action == "stop":
            ### Stop traffic
            ret = ixia_handle.traffic_control(port_handle=port_handle,action='stop')
            if ret.status != '1':
                print(ret)
                return 0
            else:
                log.info("#### Stopped Traffic Successfully ####")
        elif action == "clear_stats":
            ### Clear IXIA stats
            try:
               ret = ixia_handle.traffic_control(port_handle=port_handle,action='clear_stats')
            except:
               log.error("#### unable to clear ixia stats ####")
               return 0
            log.info("#### Cleared IXIA stats Successfully ####")
        else:
            log.error("Option passed for argument action is not valid: supports only start|stop|clear_stats")     
            return 0

        return 1

    #*********************************************************************#
    #This function is to collect ixia stats in different modes and returns
    # the stats
    #the default mode is aggregate
    #
    #*********************************************************************#
    def collect_ixia_stats(self,ixia_handle,port_handle, mode="aggregate"):
        """This function is to collect ixia stats in different modes """

        agg_stats = ixia_handle.traffic_stats(port_handle=port_handle, mode=mode)
        if agg_stats.status != "1":
            return 0
        else:
            return agg_stats

 
    #*********************************************************************#
    #This function is to find the diff between the provided values
    # specially used for diff of the stats (tx and rx)
    #provided stats should be in integers. Also it takes tolerance into 
    #consideration by default it is set to 50
    #*********************************************************************#
    def check_traffic_loss(self,tx_stats,rx_stats,tolerance=50):
        """This function returns the difference between the tx and rx """


        diff = int(tx_stats) - int(rx_stats)
        log.info("Total TX packets are: %s" % tx_stats)
        log.info("Total RX packets are: %s" % rx_stats)
        if diff >= tolerance:
            log.error('Traffic loss seen')
            return 0
        else:
            log.info("There is no Traffic loss seen and All traffic is Successful")
            return 1

    #*********************************************************************#
    #this proc is used to return IXIA port handles
    #
    #*********************************************************************#
    def ixia_port_handles(self, ixia_device, port_list,connect_ret_val):


        ipv4_addr = ixia_device.connections.alt.ip
        # Break up IPv4 address like '192.168.1.3' into a list ['192',
        # '168', '1', '3']
        quads = str(ipv4_addr).split('.')
        # Go through the nested keys in the strange return value from Ixia
        # connect() operation.
        tmp = connect_ret_val.port_handle
        log.debug('ixia_port_handles: tmp=%s' % (tmp))
        for quad in quads:
            if quad not in tmp:
                return 0
            tmp = tmp[quad]
            log.debug('ixia_port_handles: quad=:%s: tmp=%s' % (quad, tmp))
        # Create 2 dicts:
        # One from ph (port handles) to the combination of Ixia name and port.
        # The other from the combination of Ixia name and port to the ph.
        ixia_name = ixia_device.name
        ixia_ph_to_port = {}
        ixia_port_to_ph = {}
        ixia_port_to_ph[ixia_name] = {}
        for port in tmp:
            port_handle = tmp[port]
            ixia_ph_to_port[port_handle] = {'name':ixia_name, 'port':port}
            ixia_port_to_ph[ixia_name][port] = port_handle
        # Verify that all requested ports are in the return value
        for port in port_list:
            log.debug('ixia_port_handles: checking that port=%s is in ret value' % (port))
            if port not in tmp:
                return 0
        log.debug('ixia_port_handles: ph_to_port=:%s:' % (ixia_ph_to_port))
        log.debug('ixia_port_handles: port_to_ph=:%s:' % (ixia_port_to_ph))
        return {'ph_to_port':ixia_ph_to_port,
            'port_to_ph':ixia_port_to_ph}

    #*********************************************************************#
    #this proc is used to send IXIA ipv4 arp
    #
    #*********************************************************************#
    def ixia_send_ipv4_arp(self, ixia_device, port_handle):
        ret = ixia_device.interface_config(port_handle=port_handle,
                  arp_send_req=1)
        if ret.status != '1':
            self.failed('Sending arp request failed on intf %s of Ixia %s, got status %s: Ret value=%s' % (port_handle,
                                               ixia_device,ret.status,ret))
            return 0
        return 1

    #*********************************************************************#
    #this proc is used to configure IXIA Interfaces for ipv4 tcp
    #
    #*********************************************************************#
    def configure_ixia_stream_ipv4_tcp(self, ixia_conn,src_emu_handle,dst_emu_handle,frame_size,tos_type,tos_value='0',pkts_per_burst='0',
                   mode='create',transmit_mode='single_burst',bidir='0',rate_percent='0',name='ipv4_stream',rate_pps='0',
                   l4_protocol="tcp",src_port= "8000",src_port_count = "1", src_port_mode = "fixed", src_port_step = "1",
                   dest_port = "9000",dst_port_count = "1", dst_port_mode = "fixed", dst_port_step = "1"):

        if tos_type == 'ip_dscp':
            if transmit_mode.lower() == 'continuous':
                if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                elif str(rate_percent) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                elif str(rate_pps) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                else:
                    self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv4')
                    return 0
            else:
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                    circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                    track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                    transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ip_dscp=tos_value,l4_protocol = l4_protocol,
                    tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                    tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
        elif tos_type == 'ip_precedence':
            if transmit_mode.lower() == 'continuous':
                if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                elif str(rate_percent) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                elif str(rate_pps) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                        tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                        tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
                else:
                    self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv4')
                    return 0
            else:
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                    circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                    track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                    transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ip_precedence=tos_value,l4_protocol = l4_protocol,
                    tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                    tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
        else:
            log.info('Unsupported tos_type')
            return 0

        if stream_info.status != '1':
            self.failed('When doing traffic_config mode=create on intf %s to %s of Ixia %s, got status %s: \
                       Ret value=%s' % (testscript.parameters['IXIA_intf1'],testscript.parameters['IXIA_intf4'],\
                       testscript.parameters['IXIA'],stream_info.status, stream_info))
            return 0
        return stream_info['stream_id']

    #*********************************************************************#
    #this proc is used to configure IXIA Interfaces for ipv6
    #
    #*********************************************************************#
    def configure_ixia_stream_ipv6_tcp(self, ixia_conn,src_emu_handle,dst_emu_handle,frame_size,pkts_per_burst='0',tos_value='0',
        mode='create',transmit_mode='single_burst',bidir='0',rate_percent='0',name='ipv6_stream',rate_pps='0',
        l4_protocol="tcp",src_port= "8000",src_port_count = "1", src_port_mode = "fixed", src_port_step = "1",
        dest_port = "9000",dst_port_count = "1", dst_port_mode = "fixed", dst_port_step = "1"):
      
        if transmit_mode.lower() == 'continuous':
            if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step )
            elif str(rate_percent) != str(0):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
            elif str(rate_pps) != str(0):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)
            else:
                self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv6')
                return 0
        else:
            #configuring stream from ixia new interface1 to new interface2
            stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ipv6_traffic_class=tos_value,l4_protocol = l4_protocol,
                tcp_src_port = src_port,  tcp_src_port_mode = src_port_mode, tcp_src_port_count = src_port_count, tcp_src_port_step = src_port_step,
                tcp_dst_port = dest_port, tcp_dst_port_mode = dst_port_mode, tcp_dst_port_count = dst_port_count, tcp_dst_port_step = dst_port_step)

        if stream_info.status != '1':
            self.failed('When doing traffic_config mode=create on intf %s to %s of Ixia %s, got status %s: \
                       Ret value=%s' % (testscript.parameters['IXIA_intf1'],testscript.parameters['IXIA_intf4'],\
                       testscript.parameters['IXIA'],stream_info.status, stream_info))
            return 0
        return stream_info['stream_id']

    #*********************************************************************#
    #this proc is used to configure IXIA Interfaces for ipv4 udp
    #
    #*********************************************************************#
    def configure_ixia_stream_ipv4_udp(self, ixia_conn,src_emu_handle,dst_emu_handle,frame_size,tos_type,tos_value='0',pkts_per_burst='0',
                   mode='create',transmit_mode='single_burst',bidir='0',rate_percent='0',name='ipv4_stream',rate_pps='0',
                   l4_protocol="udp",src_port= "8000",src_port_count = "1", src_port_mode = "fixed", src_port_step = "1",
                   dest_port = "9000",dst_port_count = "1", dst_port_mode = "fixed", dst_port_step = "1"):

        if tos_type == 'ip_dscp':
            if transmit_mode.lower() == 'continuous':
                if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                elif str(rate_percent) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                elif str(rate_pps) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_dscp=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                else:
                    self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv4')
                    return 0
            else:
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                    circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                    track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                    transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ip_dscp=tos_value,l4_protocol = l4_protocol,
                    udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                    udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
        elif tos_type == 'ip_precedence':
            if transmit_mode.lower() == 'continuous':
                if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                elif str(rate_percent) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                elif str(rate_pps) != str(0):
                    #configuring stream from ixia new interface1 to new interface2
                    stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                        circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                        track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ip_precedence=tos_value,
                        transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                        udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                        udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
                else:
                    self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv4')
                    return 0
            else:
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                    circuit_endpoint_type='ipv4',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                    track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                    transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ip_precedence=tos_value,l4_protocol = l4_protocol,
                    udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                    udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
        else:
            log.info('Unsupported tos_type')
            return 0

        if stream_info.status != '1':
            self.failed('When doing traffic_config mode=create on intf %s to %s of Ixia %s, got status %s: \
                       Ret value=%s' % (testscript.parameters['IXIA_intf1'],testscript.parameters['IXIA_intf4'],\
                       testscript.parameters['IXIA'],stream_info.status, stream_info))
            return 0
        return stream_info['stream_id']

    #*********************************************************************#
    #this proc is used to configure IXIA Interfaces for ipv6
    #
    #*********************************************************************#
    def configure_ixia_stream_ipv6_udp(self, ixia_conn,src_emu_handle,dst_emu_handle,frame_size,pkts_per_burst='0',tos_value='0',
        mode='create',transmit_mode='single_burst',bidir='0',rate_percent='0',name='ipv6_stream',rate_pps='0',
        l4_protocol="tcp",src_port= "8000",src_port_count = "1", src_port_mode = "fixed", src_port_step = "1",
        dest_port = "9000",dst_port_count = "1", dst_port_mode = "fixed", dst_port_step = "1"):
      
        if transmit_mode.lower() == 'continuous':
            if (str(rate_percent) != str(0)) and (str(rate_pps) != str(0)):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step )
            elif str(rate_percent) != str(0):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_percent=rate_percent,l4_protocol = l4_protocol,
                udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
            elif str(rate_pps) != str(0):
                #configuring stream from ixia new interface1 to new interface2
                stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',ipv6_traffic_class=tos_value,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,rate_pps=rate_pps,l4_protocol = l4_protocol,
                udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)
            else:
                self.failed('Unknown state of transmit_mode in proc configure_ixia_stream_ipv6')
                return 0
        else:
            #configuring stream from ixia new interface1 to new interface2
            stream_info =ixia_conn.traffic_config(mode=mode,traffic_generator='ixnetwork',name=name,circuit_type='none',
                circuit_endpoint_type='ipv6',emulation_src_handle=src_emu_handle,emulation_dst_handle=dst_emu_handle,
                track_by='endpoint_pair',stream_packing='one_stream_per_endpoint_pair',pkts_per_burst=pkts_per_burst,
                transmit_mode=transmit_mode,bidirectional=bidir,frame_size=frame_size,ipv6_traffic_class=tos_value,l4_protocol = l4_protocol,
                udp_src_port = src_port,  udp_src_port_mode = src_port_mode, udp_src_port_count = src_port_count, udp_src_port_step = src_port_step,
                udp_dst_port = dest_port, udp_dst_port_mode = dst_port_mode, udp_dst_port_count = dst_port_count, udp_dst_port_step = dst_port_step)

        if stream_info.status != '1':
            self.failed('When doing traffic_config mode=create on intf %s to %s of Ixia %s, got status %s: \
                       Ret value=%s' % (testscript.parameters['IXIA_intf1'],testscript.parameters['IXIA_intf4'],\
                       testscript.parameters['IXIA'],stream_info.status, stream_info))
            return 0
        return stream_info['stream_id']

    #*********************************************************************#
    #this proc is used to configures Emulated IXIA Interfaces 
    #
    #*********************************************************************#
    def configEmulatedIxiaInterfaces_1(self,ixiacon,ixiaport_handle,portsrc_mac_addr,portipv4_addr,portipv4_mask,portipv4_gateway,portipv6_addr,
        portipv6_mask,portipv6_gateway,vlanenable = "0",vlanid = '1') :
      """configures Emulated Ixia Interfaces 
      """
     
      ret = {}
      try :
        log.info('####### Configuring IXIA interface %s  #########'%(ixiaport_handle))
        
        emu_int = ixiacon.interface_config(port_handle=ixiaport_handle,mode='config',
          intf_mode='ethernet',phy_mode='fiber', port_rx_mode='capture_and_measure',src_mac_addr=portsrc_mac_addr,
          intf_ip_addr=portipv4_addr,netmask=portipv4_mask,gateway=portipv4_gateway,
          ipv6_intf_addr=portipv6_addr,ipv6_prefix_length= portipv6_mask,ipv6_gateway=portipv6_gateway,vlan = vlanenable, vlan_id = vlanid
          )
        if(emu_int) :
          #testscript.parameters['emulatedixia_intf'][ixiaport_handle]= emu_int
          log.info ("Created Emulated interface for intf %s"%(ixiaport_handle))
          ret['status'] = 1
          ret['emulated_intf'] = emu_int
          return ret    
        else :
          log.info("Failed to create Emulated Ixia interface for intf %s"%(ixiaport_handle))
          ret['status'] = 0
          ret['emulated_intf'] = None
          return ret
      except Exception as e:
        ret['status'] = 0
        ret['emulated_intf'] = e.args
        return  ret

    def configEmulatedIxiaInterfaces(self,ixiacon,ixiaport_handle,portsrc_mac_addr,portipv4_addr,portipv4_mask,portipv4_gateway,portipv6_addr,
        portipv6_mask,portipv6_gateway, intf_mode='ethernet',vlanenable = "0",vlanid = '1',flow_control_type = "",ppm_adjust='0',connected_count="1",intf_ip_addr_step="0.0.0.0",gateway_step="0.0.0.0",
        vlan_id_count="1",vlan_id_step="1",phy_mode="fiber") :
      """configures Emulated Ixia Interfaces 
      """
      log.info ('Inside Emulate Function the Phy mode is :{}'.format(phy_mode))
      ret = {}
      try :
        
        log.info('####### Configuring IXIA interface %s  #########'%(ixiaport_handle))
        if (flow_control_type.lower()=='pfc') or (flow_control_type.lower()=='llfc') :
            
            if phy_mode == "fiber" :        
                intf_mode = 'multis_fcoe' 
            elif phy_mode == "copper":
                intf_mode =  "ethernet_fcoe" 
        else :
            intf_mode = 'ethernet'
        
        if intf_mode == 'ethernet' :
            emu_int = ixiacon.interface_config(port_handle=ixiaport_handle,mode='config',
              internal_ppm_adjust= ppm_adjust,transmit_clock_source = 'internal_ppm_adj',
              intf_mode= intf_mode,phy_mode=phy_mode, port_rx_mode='capture_and_measure',src_mac_addr=portsrc_mac_addr,
              intf_ip_addr=portipv4_addr,netmask=portipv4_mask,gateway=portipv4_gateway,
              ipv6_intf_addr=portipv6_addr,ipv6_prefix_length= portipv6_mask,
              ipv6_gateway=portipv6_gateway,vlan = vlanenable, 
              vlan_id = vlanid,connected_count=connected_count,
              intf_ip_addr_step=intf_ip_addr_step,gateway_step=gateway_step,
              vlan_id_count=vlan_id_count,vlan_id_step=vlan_id_step
              )
        else:
            if (flow_control_type.lower() == 'pfc') :
              flow_control = 'ieee802.1Qbb'
            elif (flow_control_type.lower() == 'llfc'):
              flow_control = 'ieee802.3x'
            
            if (flow_control_type == 'pfc') and (phy_mode == "fiber") :
              emu_int = ixiacon.interface_config(port_handle=ixiaport_handle,mode='config',
                internal_ppm_adjust= ppm_adjust,transmit_clock_source = 'internal_ppm_adj',
                #frame_rate_distribution_port = 'apply_to_all',frame_rate_distribution_stream = 'apply_to_all',
                intf_mode=intf_mode,phy_mode=phy_mode, port_rx_mode='capture_and_measure',src_mac_addr=portsrc_mac_addr,
                intf_ip_addr=portipv4_addr,netmask=portipv4_mask,gateway=portipv4_gateway,
                ipv6_intf_addr=portipv6_addr,ipv6_prefix_length= portipv6_mask,ipv6_gateway=portipv6_gateway,vlan = vlanenable, vlan_id = vlanid,
                fcoe_flow_control_type = flow_control,enable_flow_control = 1, fcoe_priority_group_size = 8,
                fcoe_priority_groups = '0 1 2 3 4 5 6 7',flow_control_directed_addr = '01:80:C2:00:00:01'
                  )
            elif  (flow_control_type == 'pfc') and (phy_mode == "copper") :
              emu_int = ixiacon.interface_config(port_handle=ixiaport_handle,mode='config',
                internal_ppm_adjust= ppm_adjust,transmit_clock_source = 'internal_ppm_adj',
                #frame_rate_distribution_port = 'apply_to_all',frame_rate_distribution_stream = 'apply_to_all',
                intf_mode=intf_mode,phy_mode=phy_mode, port_rx_mode='capture_and_measure',src_mac_addr=portsrc_mac_addr,
                intf_ip_addr=portipv4_addr,netmask=portipv4_mask,gateway=portipv4_gateway,
                ipv6_intf_addr=portipv6_addr,ipv6_prefix_length= portipv6_mask,ipv6_gateway=portipv6_gateway,vlan = vlanenable, vlan_id = vlanid,
                fcoe_flow_control_type = flow_control,enable_flow_control = 1, fcoe_priority_group_size = 8,
                fcoe_priority_groups = '0 1 2 3 4 5 6 7',flow_control_directed_addr = '01:80:C2:00:00:01',speed = 'ether10000lan'
                  )

        if(emu_int) :
          #testscript.parameters['emulatedixia_intf'][ixiaport_handle]= emu_int
          log.info ("Created Emulated interface for intf %s"%(ixiaport_handle))
          ret['status'] = 1
          ret['emulated_intf'] = emu_int
          return ret    
        else :
          log.info("Failed to create Emulated Ixia interface for intf %s"%(ixiaport_handle))
          ret['status'] = 0
          ret['emulated_intf'] = None
          return ret
      except Exception as e:
        ret['status'] = 0
        ret['emulated_intf'] = e.args
        return  ret
    
    #*********************************************************************#
      #this proc is used to unconfigures/removes  Emulated IXIA Interfaces 
      #
    #*********************************************************************#
    def unConfigEmulatedIxiaInterfaces(self,ixiacon,ixiaport_handle):
      """unconfig Emulated Ixia Interfaces
      """
      ret = {}
      try :
        emu_int = ixiacon.interface_config(port_handle=ixiaport_handle,mode='destroy')
        log.info(" enu_int %s"%(emu_int)) 
        ret['status'] = 1
        ret['emulated_intf'] = emu_int
        return ret
      except Exception as e:
        ret['status'] = 0
        ret['emulated_intf'] = e.args
        return  ret
    #*********************************************************************#
      #this proc is used to removes  traffic item/ixia stream 
      #
    #*********************************************************************#

    def removeIxiaStreams(self,ixiacon,trafficitem) :
      """ Removes ixia streams 
      """
      ret = {}

      try :    
        stream_info = ixiacon.traffic_config(mode='remove',stream_id=trafficitem)
        ret['status'] = 1
        ret['value'] = None
        return ret
      except Exception as e:
        ret['status'] = 0
        ret['value'] = e.args
        return  ret



    
    



