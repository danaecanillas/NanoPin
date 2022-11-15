# NanoPin

Project submitted at Datathon 2022 organized by the AED (UPC). The Cracking the Nano team has obtained the third place.

## Challenge
Project proposed by Qualcomm, a company that creates semiconductors, software, and services related to wireless technology. The goal of the challenge is to design a circuit that connects a set of chip pins optimally using the shortest length of wire. This path can be subdivided into different chains (clusters) connected to a set of driver pins that supply power.

## Solution
Our solution focuses on generating radial clusters with an epicenter located in the middle of the drive pins set. To trace the route in each sector, we have used the bisection of each sector: the first half is used to reach the farthest pin of the cluster and the second half is used to return the chain to the power driver pin source.
