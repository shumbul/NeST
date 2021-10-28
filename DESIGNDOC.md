# Extend NeST to support emulation of Multipath TCP
Team Details:
- Shumbul Arifa (181CO152)
- Srikrishna G. Yaji (181CO153)
- Tarun S. Anur (181CO255)

<hr>

## About the project
Multipath TCP (MPTCP) is an ongoing effort of the Internet Engineering Task Force's(IETF) Multipath TCP working group, that aims at allowing a Transmission Control Protocol (TCP) connection to use multiple paths to maximize resource usage and increase redundancy. 
It has been quite challenging for the research community to perform experiments with MPTCP because it is not supported in popular network simulators. 
The main aim of this project is to leverage the Linux implementation of MPTCP by building user-friendly APIs in NeST.

## Design
After our initial understanding, two possible approaches were found in order to incorporate MPTCP.

### Approach-1
Since NeST uses Linux network namespaces under the hood we can run the `ip mptcp` [command](https://man7.org/linux/man-pages/man8/ip-mptcp.8.html) to emulate it. 

Advantages:
- No Linux kernel updation required.

Task to be done:
- A new separate API has to be developed starting from the node creation.

### Approach-2
Tweak the implementation of Linux kernel to get, 
```
ip link set dev <ethernet> multipath <on/off> 
ip link set dev <ethernet> multipath backup
```
commands to make the network use MPTCP and also specify how should the additional connection act.

Following this approach we should create, 
1. A function which checks if the required protocol is MPTCP? If yes, then Multipath TCP switched on else off.
2. A function which checks if the requirements are satisfied by the system for MPTCP protocol to be used.
3. A function which executes and emulates the MPTCP connection, making a link as backup 
