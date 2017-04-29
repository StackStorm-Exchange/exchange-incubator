# Brocade HW-VTEP Appliance UI
## Introduction
Virtual machines (VMs) operate over a VXLAN virtual network. In many large scale data centers, VMs on VXLAN networks require access to resources hosted on physical networks which use VLAN to connect. To achieve efficient communication between VXLAN to VLAN, a separate physical VTEP device is required to perform the network translation. Brocade VDX 6740 series switches help to achieve this configuration. For more about Brocade Gateways for VMware NSX, read the Solution Brief.

Created by GS Lab, the StackStorm Integration Pack for the Brocade VCS Gateway for VMware NSX makes configuring a hardware gateway simple, especially for teams with little to no experience with Brocade networking technology. The user simply plugs in the VDX 6740 switches, enters basic environment data into a browser-based form, and the StackStorm Integration Pack does the rest. Post installation, all VTEP management functions are carried out through the VMware NSX interface. As with all StackStorm Integration Packs, this configuration tool is community created and supported.

***Key Benefits***
* Reduce time to deploy a hardware gateway with pre-configured automation workflows
* Reduce operational costs by automating switch and fabric configuration tasks
* Ensure configuration accuracy and consistency for VDX 6740 switch deployment

***Components***
</br>This appliance consist of three components 
* UI
* NSX-VTEP pack for stackstorm
* VDX-VTEP pack for Stackstorm
 
# Installation
***Prerequisites***
* To install Brocade HW-VTEP Appliance, you need the 64-bit version of one of theseUbuntu/RHEL/CentOS versions
  * Ubuntu 14.04
  * Ubuntu 16.04
  * RHEL 7 / CentOS 7
  * RHEL 6 / CentOS 6
* StackStorm v2.2
* Python 2.7
* git

***Installation Steps***
* Install vdx_vtep and nsx_vtep pack
  ```
  st2 pack install vdx_vtep nsx_vtep
  ```
* Install Brocade HW-VTEP Appliance UI.
  1. Get the Brocade HW-VTEP Appliance UI source code from Github.
  ```
  git clone https://github.com/GSLabDev/brocade-vtep-appliance-ui.git
  ```
  2. Install python dependencies
  ```
  cd brocade-vtep-appliance-ui/
  pip install -r requirements.txt
  ```
* Start the Brocade HW-VTEP Appliance UI using CLI.
  1. Go to cloned repository of Brocade HW-VTEP Appliance UI on your local system.
  ```
  cd /<path>/<to>/<cloned>/<repo>/brocade-vtep-appliance-ui/
  ```
  2. Start the appliance.
  ```
  python application.py
  ```
* Stop the Brocade HW-VTEP Appliance UI
  * To stop the appliance just kill the process stared in above step by pressing "Ctrl C".

***Access the appliance:***
> Please note that this application works best in Chrome browser.
* To access UI please hit below URL from browser.
  ```
  http://<appliance_server_ip>:5000
  ```

## FAQ
## Maintainers
* Ravindra Yadav (GSLAB)
* Yugendra Khonde (GSLAB)
* Aditi Kulkarni (GSLAB)
