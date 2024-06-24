#!/usr/bin/env python

# python
 
def generateTraffic2222(src_handle,dst_handle):          

    countdown(30) 
    rate_pps = 10000
    frame_size = 500

    #def Ixia_Configure_Traffic(topology_1_handle, topology_2_handle, rate_pps, frame_size):
    print("Configuring L2-L3 traffic")
    _result_ = ixiangpf.traffic_config(
        mode='create',
        endpointset_count='1',
        emulation_src_handle=src_handle,
        emulation_dst_handle=dst_handle,
        name='Traffic_1_Item',
        circuit_endpoint_type='ipv4',
        rate_pps=rate_pps,
        frame_size=frame_size,
        mac_dst_mode='fixed',
        mac_src_mode='fixed',
        track_by='trackingenabled0',
    )

    if _result_['status'] != IxiaHlt.SUCCESS:
        trafficItem_handle = 0
        ErrorHandler('traffic_config', _result_)
    else:
        trafficItem_handle = _result_["stream_id"]
    
    return trafficItem_handle
