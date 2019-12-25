# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019 NITK Surathkal

##########################################
# Note: This script should be run as root
##########################################

import os
import subprocess

def exec_subprocess(cmd, block = True):
    """
    executes a command

    :param cmd: command to be executed
    :type cmd: String
    :param block: A flag to indicate whether the command 
                    should be executed asynchronously
    :type block: boolean
    """
    temp = subprocess.Popen(cmd.split())
    if block:
        temp.communicate()
    else:
        pass

############################################
# CONVENTION: 
# - In parameter list, namespace 
#   names come before interface names.
# - Peers are entities at the ends points of
#   the network.
# - Router connects atleast 2 hosts.
# - Host represents either peer or router
#   based on context.
############################################

def create_ns(ns_name):
    """
    Create namespace if it doesn't already exist
    
    :param ns_name: namespace name
    :type ns_name: string
    """
    exec_subprocess('ip netns add ' + ns_name)

def delete_ns(ns_name):
    """
    Drops the namespace if it already exists.

    :param ns_name: namespace name
    :type ns_name: string
    """
    exec_subprocess('ip netns del ' + ns_name)

def en_ip_forwarding(ns_name):
    """
    Enables ip forwarding in a namespace. Used for routers

    :param ns_name: namespace name
    :type ns_name: String
    """
    exec_subprocess('ip netns exec ' + ns_name + ' sysctl -w net.ipv4.ip_forward=1')

#TODO: delete a veth
def create_veth(dev_name1, dev_name2):
    """
    Create a veth pair

    :param dev_name1, dev_name2: interface names
    :type dev_name1, dev_name2: string 
    """
    exec_subprocess('ip link add ' + dev_name1 +' type veth peer name ' + dev_name2)

def add_int_to_ns(ns_name, dev_name):
    """
    Add interface to a namespace

    :param ns_name: namespace name
    :type ns_name: string
    :param dev_name: interface name
    :type dev_name: string 
    """
    exec_subprocess('ip link set ' + dev_name + ' netns ' + ns_name)

def set_int_up(ns_name, dev_name):
    """
    Set interface mode to up

    :param ns_name: namespace name
    :type ns_name: string
    :param dev_name: interface name
    :type dev_name: string 
    """
    exec_subprocess('ip netns exec ' + ns_name + ' ip link set dev ' + dev_name + ' up')

# Use this function for `high level convinience`
def setup_veth(ns_name1, ns_name2, dev_name1, dev_name2):
    """
    Sets up veth connection between interafaces. The interfaces are set up as well.
    
    :param ns_name1, ns_name2: namespace names
    :type ns_name1, ns_name2: string
    :param dev_name1: interface name associated with ns_name1
    :type dev_name1: string
    :param dev_name2: interface name associated with ns_name2
    :type dev_name2: string
    """
    create_veth(dev_name1, dev_name2)
    add_int_to_ns(ns_name1, dev_name1)
    add_int_to_ns(ns_name2, dev_name2)
    set_int_up(ns_name1, dev_name1)
    set_int_up(ns_name2, dev_name2)

def create_peer(peer_name):
    """
    Creates a peer and adds it to the existing topology.

    :param peer_name: name of the peer namespace
    :type peer_name: string
    """
    create_ns(peer_name)

def create_router(router_name):
    """
    Creates a router and adds it to 
    the existing topology.

    :param router_name: name of the router namespace
    :type router_name: string
    """
    create_ns(router_name)
    en_ip_forwarding(router_name)

def assign_ip(host_name, dev_name, ip_address):
    """
    Assigns ip address to interface

    :param host_name: name of the host namespace
    :type host_name: string
    :param dev_name: name of the interface
    :type dev_name: string
    :param ip_address: ip address to be assigned to the interface
    :type ip_address: string
    """
    #TODO: Support for ipv6
    exec_subprocess('ip netns exec ' + host_name + ' ip address add ' + ip_address + ' dev ' + dev_name)

def add_route(host_name, dest_ip, next_hop_ip, via_int):
    """
    Adds a route in routing table of host.

    :param host_name: name of the host namespace
    :type host_name: string
    :param dest_ip: the destination ip for the route
    :type dest_ip: string
    :param next_hop_ip: IP of the very next interface
    :type next_hop_ip: string
    :param via_int: the corresponding interface in the host
    :type via_int: string
    """
    exec_subprocess('ip netns exec {} ip route add {} via {} dev {}'.format(host_name, dest_ip, next_hop_ip, via_int))

def set_interface_mode(ns_name, dev_name, mode):
    exec_subprocess('ip netns exec ' + ns_name + ' ip link set dev ' + dev_name + ' ' + mode)

# Only bandwith and latency is considered
# Assuming tc on egress 
# Using Netem
def add_traffic_control(host_name, dev_name, rate, latency):
    """
    Add traffic control to host

    :param host_name: name of the host namespace
    :type host_name: string
    :param rate: rate of the bandwidth
    :type rate: string
    :param latency: latency of the link
    :type latency: string
    """
    exec_subprocess('ip netns exec {} tc qdisc add dev {} root netem rate {} latency {}'.format(host_name, dev_name, rate, latency))

def run_iperf_server(ns_name):
    """
    Run Iperf Server on a namesapce
    :param ns_name: name of the server namespace
    :type ns_name: string
    """
    #TODO: iperf3?
    exec_subprocess('ip netns {} iperf -s'.format(ns_name))

def run_iperf_client(ns_name, server_ip):
    """
    Run Iperf Client

    :param ns_name: name of the client namespace
    :type ns_name: string
    :param server_ip: the ip of server to which it has to connect
    :type server_ip: string
    """
    exec_subprocess('ip netns {} iperf -c {}'.format(ns_name, server_ip))