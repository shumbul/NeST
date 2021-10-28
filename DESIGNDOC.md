# Extend NeST to support emulation of Multipath TCP

Team Details:
- Shumbul Arifa (181CO152)
- Srikrishna G. Yaji (181CO153)
- Tarun S. Anur (181CO255)

<hr>

## About the project

Multipath TCP (MPTCP) is an ongoing effort of the Internet Engineering Task Force's(IETF) Multipath TCP working group, that aims at allowing a Transmission Control Protocol (TCP) connection to use multiple paths to maximize resource usage and increase
redundancy. 
It has been quite challenging for the research community to perform experiments with MPTCP because it is not supported in popular network simulators. 
The main aim of this project is to leverage the Linux implementation of MPTCP by building user-friendly APIs in NeST.

## Design

Two possible approaches were found in order to incorporate MPTCP.

### Approach-1)

Since NeSt uses executes linux network namespaces under the hood we can run the ```ip mptcp``` command (https://man7.org/linux/man-pages/man8/ip-mptcp.8.html) to emulate it. 

Advantages:
- No kernal updation required.

Disadvantages:
- A new separate API has to be developed starting from the node creation which seems problematic.


### Approach-2)

Update the linux kernel to support MPTCP.
This provides us with 
```
ip link set dev <ethernet> multipath <on/off> 
ip link set dev <ethernet> multipath backup
```
commands to make the network use mptcp and also specify how should the additional connection act.

Following approach-2 we should create, 
1. a function which executes, making a link as backup
2. a function which checks if the required protocol is MPTCP ? if yes..then multipath switched on else off.
3. a function which checks if the requirements are satisfied by the system for MPTCP protocol to be used. 
