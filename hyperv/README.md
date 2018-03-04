# Microsoft Hyper-V Integration Pack

# <a name="Introduction"></a> Introduction
This pack provides an integration between StackStorm and Microsoft Hyper-V.
It is designed to mimic the Hyper-V Cmdlets for PowerShell:

- [Server 2012 Docs](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=winserver2012-ps)
- [Server 2016 Docs](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps)

This pack works by executing Hyper-V PowerShell commands on a remote
windows hosts.


# <a name="QuickStart"></a> Quick Start


**Steps**

1. Install the pack

    ``` shell
    st2 pack install hyperv
    ```

2. Configure WinRM on a remote Windows host by running the [setup PowerShell
   script](https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1)

   ``` PowerShell
   Invoke-WebRequest https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 -OutFile "ConfigureRemotingForAnsible.ps1"
   .\ConfigureRemotingForAnsible.ps1
   ```

3. Install Remote Server Administration Tools (RSAT):

    ``` shell
    st2 run activedirectory.install_rsat_ad_powershell hostname='remotehost.domain.com' username='Administrator' password='xxx'
    ```

4. Execute an action (example: check if HOSTTOGET is a member of AD)

    ``` shell
    st2 run activedirectory.get_ad_computer hostname='remotehost.domain.com' username='Administrator' password='xxx' args='HOSTTOGET'
    ```



# <a name="Prerequisites"></a> Prerequisites
This pack works by executing PowerShell commands on a remote Windows host that
has the following setup:

1. WinRM needs to be configured
   Execute the following script on all hosts that this pack will be running
   commands on:
   https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1

2. Install Remote Server Administration Tools (RSAT) tools for Hyper-V
   Install the "Active Directory Domain Services (AD DS) Tools and Active
   Directory Lightweight Directory Services (AD LDS) Tools" component of
   RSAT on all hosts that this pack will be running commands on.
   **Note** : This only works on Windows Server OSes.

## Manual Install
``` PowerShell
Import-Module Servermanager
Install-WindowsFeature -Name RSAT-AD-PowerShell
```

## Install using st2 action (from this pack)
``` shell
st2 run activedirectory.install_rsat_ad_powershell hostname='remotehost.domain.com' username='xxx' password='xxx'
```

# <a name="Installation"></a> Installation
Currently this pack is in incubation, so installation must be performed from the
github page.

``` shell
st2 pack install https://github.com/EncoreTechnologies/stackstorm-activedirectory
```

Once it is added to the exchange you can install it like so:

``` shell
st2 pack install activedirectory
```

# <a name="Configuration"></a> Configuration
You will need to specify Active Directory credentials that will be
using to connect to the remote Windows hosts in the
`/opt/stackstorm/config/activedirectory.yaml` file. You can specify multiple
sets of credentials using nested values.

**Note** : `st2 pack config` doesn't handle nested schemas very well (known bug)
    so it's best to create the configuraiton file yourself and copy it into
    `/opt/stackstorm/configs/activedirectory.yaml` then run `st2ctl reload --register-configs`


## <a name="Schema"></a> Schema

``` yaml
---
port: <default port number to use for WinRM connections: default = '5986'>
transport: <default transport to use for WinRM connections: default = 'ntlm'>

activedirectory:
  <credential-name-1>:
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
  <credential-name-2>:
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
    port: <port number override to use for WinRM connections: default = '5986'>
    transport: <transport override to use for WinRM connections: default = 'ntlm'>
  ...
```

## <a name="SchemaExample"></a> Schema Example
``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  dev:
    username: username@dev.domain.tld
    password: xxx
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
  prod:
    username: produser@domain.tld
    password: xxx
    port: 6611
    transport: kerberos
  prod-svc:
    username: prodsvc@domain.tld
    password: xxx
    port: 1234
    transport: basic
```

**Note** : All actions allow you to specify a set of credentials as inputs
           to the action instead of requiring a configuration. See the [Actions](#Actions)
           section for more information.

# <a name="Actions"></a> Actions

Actions in this pack are based off of the PowerShell cmdlets in ActiveDirectory module [link](https://technet.microsoft.com/en-us/itpro/powershell/windows/addsadministration/activedirectory).

The actions from these cmdlets are auto-generated based on a the file `etc/cmdlets.txt`
using the generation script `etc/cmdlets_generate.py`

Below is a list of the currently implemented actions based on cmdlets.

| Action | PowerShell Cmdlet | Description |
|--------|-------------------|-------------|
| add_vm_dvd_drive | [Add-VMDvdDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmdvddrive)  | Adds a DVD drive to a virtual machine. |
| add_vm_fibre_channel_hba | [Add-VMFibreChannelHba](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmfibrechannelhba)  | Adds a virtual Fibre Channel host bus adapter to a virtual machine. |
| add_vm_group_member | [Add-VMGroupMember](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmgroupmember)  | Adds group members to a virtual machine group. |
| add_vm_hard_disk_drive | [Add-VMHardDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmharddiskdrive)  | Adds a hard disk drive to a virtual machine. |
| add_vm_migration_network | [Add-VMMigrationNetwork](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmmigrationnetwork)  | Adds a network for virtual machine migration on one or more virtual machine hosts. |
| add_vm_network_adapter | [Add-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmnetworkadapter)  | Adds a virtual network adapter to a virtual machine. |
| add_vm_network_adapter_acl | [Add-VMNetworkAdapterAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmnetworkadapteracl)  | Creates an ACL to apply to the traffic through a virtual machine network adapter. |
| add_vm_network_adapter_extended_acl | [Add-VMNetworkAdapterExtendedAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmnetworkadapterextendedacl)  | Creates an extended ACL for a virtual network adapter. |
| add_vm_remote_fx3d_video_adapter | [Add-VMRemoteFx3dVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmremotefx3dvideoadapter)  | Adds a RemoteFX video adapter in a virtual machine. |
| add_vm_scsi_controller | [Add-VMScsiController](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmscsicontroller)  | Adds a SCSI controller in a virtual machine. |
| add_vm_storage_path | [Add-VMStoragePath](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmstoragepath)  | Adds a path to a storage resource pool. |
| add_vm_switch | [Add-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmswitch)  | Adds a virtual switch to an Ethernet resource pool. |
| add_vm_switch_extension_port_feature | [Add-VMSwitchExtensionPortFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmswitchextensionportfeature)  | Adds a feature to a virtual network adapter. |
| add_vm_switch_extension_switch_feature | [Add-VMSwitchExtensionSwitchFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmswitchextensionswitchfeature)  | Adds a feature to a virtual switch. |
| add_vm_switch_team_member | [Add-VMSwitchTeamMember](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmswitchteammember)  | Adds members to a virtual switch team. |
| add_vm_network_adapter_routing_domain_mapping | [Add-VmNetworkAdapterRoutingDomainMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/add-vmnetworkadapterroutingdomainmapping)  | Adds a routing domain and virtual subnets to a virtual network adapter. |
| checkpoint_vm | [Checkpoint-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/checkpoint-vm)  | Creates a checkpoint of a virtual machine. |
| compare_vm | [Compare-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/compare-vm)  | Compares a virtual machine and a virtual machine host for compatibility, returning a compatibility report. |
| complete_vm_failover | [Complete-VMFailover](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/complete-vmfailover)  | Completes a virtual machine's failover process on the Replica server. |
| connect_vm_network_adapter | [Connect-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/connect-vmnetworkadapter)  | Connects a virtual network adapter to a virtual switch. |
| connect_vm_san | [Connect-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/connect-vmsan)  | Associates a host bus adapter with a virtual storage area network (SAN). |
| convert_vhd | [Convert-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/convert-vhd)  | Converts the format, version type, and block size of a virtual hard disk file. |
| copy_vm_file | [Copy-VMFile](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/copy-vmfile)  | Copies a file to a virtual machine. |
| debug_vm | [Debug-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/debug-vm)  | Debugs a virtual machine. |
| disable_vm_console_support | [Disable-VMConsoleSupport](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmconsolesupport)  | Disables keyboard, video, and mouse for virtual machines. |
| disable_vm_eventing | [Disable-VMEventing](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmeventing)  | Disables virtual machine eventing. |
| disable_vm_integration_service | [Disable-VMIntegrationService](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmintegrationservice)  | Disables an integration service on a virtual machine. |
| disable_vm_migration | [Disable-VMMigration](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmmigration)  | Disables migration on one or more virtual machine hosts. |
| disable_vm_remote_fx_physical_video_adapter | [Disable-VMRemoteFXPhysicalVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmremotefxphysicalvideoadapter)  | Disables one or more RemoteFX physical video adapters from use with RemoteFX-enabled virtual machines. |
| disable_vm_resource_metering | [Disable-VMResourceMetering](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmresourcemetering)  | Disables collection of resource utilization data for a virtual machine or resource pool. |
| disable_vm_switch_extension | [Disable-VMSwitchExtension](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmswitchextension)  | Disables one or more extensions on one or more virtual switches. |
| disable_vmtpm | [Disable-VMTPM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disable-vmtpm)  | Disables TPM functionality on a virtual machine. |
| disconnect_vm_network_adapter | [Disconnect-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disconnect-vmnetworkadapter)  | Disconnects a virtual network adapter from a virtual switch or Ethernet resource pool. |
| disconnect_vm_san | [Disconnect-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/disconnect-vmsan)  | Removes a host bus adapter from a virtual storage area network (SAN). |
| dismount_vhd | [Dismount-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/dismount-vhd)  | Dismounts a virtual hard disk. |
| enable_vm_console_support | [Enable-VMConsoleSupport](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmconsolesupport)  | Enables keyboard, video, and mouse for virtual machines. |
| enable_vm_eventing | [Enable-VMEventing](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmeventing)  | Enables virtual machine eventing. |
| enable_vm_integration_service | [Enable-VMIntegrationService](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmintegrationservice)  | Enables an integration service on a virtual machine. |
| enable_vm_migration | [Enable-VMMigration](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmmigration)  | Enables migration on one or more virtual machine hosts. |
| enable_vm_remote_fx_physical_video_adapter | [Enable-VMRemoteFXPhysicalVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmremotefxphysicalvideoadapter)  | Enables one or more RemoteFX physical video adapters for use with RemoteFX-enabled virtual machines. |
| enable_vm_replication | [Enable-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmreplication)  | Enables replication of a virtual machine. |
| enable_vm_resource_metering | [Enable-VMResourceMetering](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmresourcemetering)  | Collects resource utilization data for a virtual machine or resource pool. |
| enable_vm_switch_extension | [Enable-VMSwitchExtension](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmswitchextension)  | Enables one or more extensions on one or more switches. |
| enable_vmtpm | [Enable-VMTPM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/enable-vmtpm)  | Enables TPM functionality on a virtual machine. |
| export_vm | [Export-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/export-vm)  | Exports a virtual machine to disk. |
| export_vm_snapshot | [Export-VMSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/export-vmsnapshot)  | Exports a virtual machine checkpoint to disk. |
| get_vhd | [Get-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vhd)  | Gets the virtual hard disk object associated with a virtual hard disk. |
| get_vhd_set | [Get-VHDSet](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vhdset)  | Gets information about a VHD set. |
| get_vhd_snapshot | [Get-VHDSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vhdsnapshot)  | Gets information about a checkpoint in a VHD set. |
| get_vm | [Get-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vm)  | Gets the virtual machines from one or more Hyper-V hosts. |
| get_vm_bios | [Get-VMBios](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmbios)  | Gets the BIOS of a virtual machine or snapshot. |
| get_vm_com_port | [Get-VMComPort](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmcomport)  | Gets the COM ports of a virtual machine or snapshot. |
| get_vm_connect_access | [Get-VMConnectAccess](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmconnectaccess)  | Gets entries showing users and the virtual machines to which they can connect on one or more Hyper-V hosts. |
| get_vm_dvd_drive | [Get-VMDvdDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmdvddrive)  | Gets the DVD drives attached to a virtual machine or snapshot. |
| get_vm_fibre_channel_hba | [Get-VMFibreChannelHba](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmfibrechannelhba)  | Gets the Fibre Channel host bus adapters associated with one or more virtual machines. |
| get_vm_firmware | [Get-VMFirmware](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmfirmware)  | Gets the firmware configuration of a virtual machine. |
| get_vm_floppy_disk_drive | [Get-VMFloppyDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmfloppydiskdrive)  | Gets the floppy disk drives of a virtual machine or snapshot. |
| get_vm_group | [Get-VMGroup](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmgroup)  | Gets virtual machine groups. |
| get_vm_hard_disk_drive | [Get-VMHardDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmharddiskdrive)  | Gets the virtual hard disk drives attached to one or more virtual machines. |
| get_vm_host | [Get-VMHost](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmhost)  | Gets a Hyper-V host. |
| get_vm_host_cluster | [Get-VMHostCluster](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmhostcluster)  | Gets virtual machine host clusters. |
| get_vm_host_numa_node | [Get-VMHostNumaNode](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmhostnumanode)  | Gets the NUMA topology of a virtual machine host. |
| get_vm_host_numa_node_status | [Get-VMHostNumaNodeStatus](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmhostnumanodestatus)  | Gets the status of the virtual machines on the non-uniform memory access (NUMA) nodes of a virtual machine host or hosts. |
| get_vm_host_supported_version | [Get-VMHostSupportedVersion](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmhostsupportedversion)  | Returns a list of virtual machine configuration versions that are supported on a host. |
| get_vm_ide_controller | [Get-VMIdeController](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmidecontroller)  | Gets the IDE controllers of a virtual machine or snapshot. |
| get_vm_integration_service | [Get-VMIntegrationService](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmintegrationservice)  | Gets the integration services of a virtual machine or snapshot. |
| get_vm_key_protector | [Get-VMKeyProtector](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmkeyprotector)  | Retrieves a key protector for a virtual machine. |
| get_vm_memory | [Get-VMMemory](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmmemory)  | Gets the memory of a virtual machine or snapshot. |
| get_vm_migration_network | [Get-VMMigrationNetwork](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmmigrationnetwork)  | Gets the networks added for migration to one or more virtual machine hosts. |
| get_vm_network_adapter | [Get-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapter)  | Gets the virtual network adapters of a virtual machine, snapshot, management operating system, or of a virtual machine and management operating system. |
| get_vm_network_adapter_acl | [Get-VMNetworkAdapterAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapteracl)  | Gets the ACLs configured for a virtual machine network adapter. |
| get_vm_network_adapter_extended_acl | [Get-VMNetworkAdapterExtendedAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapterextendedacl)  | Gets extended ACLs configured for a virtual network adapter. |
| get_vm_network_adapter_failover_configuration | [Get-VMNetworkAdapterFailoverConfiguration](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapterfailoverconfiguration)  | Gets the IP address of a virtual network adapter configured to be used when a virtual machine fails over. |
| get_vm_network_adapter_routing_domain_mapping | [Get-VMNetworkAdapterRoutingDomainMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapterroutingdomainmapping)  | Gets members of a routing domain. |
| get_vm_network_adapter_team_mapping | [Get-VMNetworkAdapterTeamMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapterteammapping)  | Gets mapping for the virtual network adapters of a virtual machine to the management operating systems network team adapters. |
| get_vm_network_adapter_vlan | [Get-VMNetworkAdapterVlan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadaptervlan)  | Gets the virtual LAN settings configured on a virtual network adapter. |
| get_vm_processor | [Get-VMProcessor](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmprocessor)  | Gets the processor of a virtual machine or snapshot. |
| get_vm_remote_fx_physical_video_adapter | [Get-VMRemoteFXPhysicalVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmremotefxphysicalvideoadapter)  | Gets the RemoteFX physical graphics adapters on one or more Hyper-V hosts. |
| get_vm_remote_fx3d_video_adapter | [Get-VMRemoteFx3dVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmremotefx3dvideoadapter)  | Gets the RemoteFX video adapter of a virtual machine or snapshot. |
| get_vm_replication | [Get-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmreplication)  | Gets the replication settings for a virtual machine. |
| get_vm_replication_authorization_entry | [Get-VMReplicationAuthorizationEntry](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmreplicationauthorizationentry)  | Gets the authorization entries of a Replica server. |
| get_vm_replication_server | [Get-VMReplicationServer](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmreplicationserver)  | Gets the replication and authentication settings of a Replica server. |
| get_vm_resource_pool | [Get-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmresourcepool)  | Gets the resource pools on one or more virtual machine hosts. |
| get_vm_san | [Get-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsan)  | Gets the available virtual machine storage area networks on a Hyper-V host or hosts. |
| get_vm_scsi_controller | [Get-VMScsiController](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmscsicontroller)  | Gets the SCSI controllers of a virtual machine or snapshot. |
| get_vm_security | [Get-VMSecurity](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsecurity)  | Gets security information about a virtual machine. |
| get_vm_snapshot | [Get-VMSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsnapshot)  | Gets the checkpoints associated with a virtual machine or checkpoint. |
| get_vm_storage_path | [Get-VMStoragePath](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmstoragepath)  | Gets the storage paths in a storage resource pool. |
| get_vm_switch | [Get-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitch)  | Gets virtual switches from one or more virtual Hyper-V hosts. |
| get_vm_switch_extension | [Get-VMSwitchExtension](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchextension)  | Gets the extensions on one or more virtual switches. |
| get_vm_switch_extension_port_data | [Get-VMSwitchExtensionPortData](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchextensionportdata)  | Retrieves the status of a virtual switch extension feature applied to a virtual network adapter. |
| get_vm_switch_extension_port_feature | [Get-VMSwitchExtensionPortFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchextensionportfeature)  | Gets the features configured on a virtual network adapter. |
| get_vm_switch_extension_switch_data | [Get-VMSwitchExtensionSwitchData](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchextensionswitchdata)  | Gets the status of a virtual switch extension feature applied on a virtual switch. |
| get_vm_switch_extension_switch_feature | [Get-VMSwitchExtensionSwitchFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchextensionswitchfeature)  | Gets the features configured on a virtual switch. |
| get_vm_switch_team | [Get-VMSwitchTeam](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmswitchteam)  | Gets virtual switch teams from Hyper-V hosts. |
| get_vm_system_switch_extension | [Get-VMSystemSwitchExtension](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsystemswitchextension)  | Gets the switch extensions installed on a virtual machine host. |
| get_vm_system_switch_extension_port_feature | [Get-VMSystemSwitchExtensionPortFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsystemswitchextensionportfeature)  | Gets the port-level features supported by virtual switch extensions on one or more Hyper-V hosts. |
| get_vm_system_switch_extension_switch_feature | [Get-VMSystemSwitchExtensionSwitchFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmsystemswitchextensionswitchfeature)  | Gets the switch-level features on one or more Hyper-V hosts. |
| get_vm_video | [Get-VMVideo](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmvideo)  | Gets video settings for virtual machines. |
| get_vm_network_adapter_isolation | [Get-VmNetworkAdapterIsolation](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/get-vmnetworkadapterisolation)  | Gets isolation settings for a virtual network adapter. |
| grant_vm_connect_access | [Grant-VMConnectAccess](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/grant-vmconnectaccess)  | Grants a user or users access to connect to a virtual machine or machines. |
| import_vm | [Import-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/import-vm)  | Imports a virtual machine from a file. |
| import_vm_initial_replication | [Import-VMInitialReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/import-vminitialreplication)  | Imports initial replication files for a Replica virtual machine to complete the initial replication when using external media as the source. |
| measure_vm | [Measure-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/measure-vm)  | Reports resource utilization data for one or more virtual machines. |
| measure_vm_replication | [Measure-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/measure-vmreplication)  | Gets replication statistics and information associated with a virtual machine. |
| measure_vm_resource_pool | [Measure-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/measure-vmresourcepool)  | Reports resource utilization data for one or more resource pools. |
| merge_vhd | [Merge-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/merge-vhd)  | Merges virtual hard disks. |
| mount_vhd | [Mount-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/mount-vhd)  | Mounts one or more virtual hard disks. |
| move_vm | [Move-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/move-vm)  | Moves a virtual machine to a new Hyper-V host. |
| move_vm_storage | [Move-VMStorage](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/move-vmstorage)  | Moves the storage of a virtual machine. |
| new_vfd | [New-VFD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vfd)  | Creates a virtual floppy disk. |
| new_vhd | [New-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vhd)  | Creates one or more new virtual hard disks. |
| new_vm | [New-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vm)  | Creates a new virtual machine. |
| new_vm_group | [New-VMGroup](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vmgroup)  | Creates a virtual machine group. |
| new_vm_replication_authorization_entry | [New-VMReplicationAuthorizationEntry](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vmreplicationauthorizationentry)  | Creates a new authorization entry that allows one or more primary servers to replicate data to a specified Replica server. |
| new_vm_resource_pool | [New-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vmresourcepool)  | Creates a resource pool. |
| new_vm_san | [New-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vmsan)  | Creates a new virtual storage area network (SAN) on a Hyper-V host. |
| new_vm_switch | [New-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/new-vmswitch)  | Creates a new virtual switch on one or more virtual machine hosts. |
| optimize_vhd | [Optimize-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/optimize-vhd)  | Optimizes the allocation of space used by virtual hard disk files, except for fixed virtual hard disks. |
| optimize_vhd_set | [Optimize-VHDSet](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/optimize-vhdset)  | Optimizes VHD set files. |
| remove_vhd_snapshot | [Remove-VHDSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vhdsnapshot)  | Removes a checkpoint from a VHD set file. |
| remove_vm | [Remove-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vm)  | Deletes a virtual machine. |
| remove_vm_dvd_drive | [Remove-VMDvdDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmdvddrive)  | Deletes a DVD drive from a virtual machine. |
| remove_vm_fibre_channel_hba | [Remove-VMFibreChannelHba](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmfibrechannelhba)  | Removes a Fibre Channel host bus adapter from a virtual machine. |
| remove_vm_group | [Remove-VMGroup](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmgroup)  | Removes a virtual machine group. |
| remove_vm_group_member | [Remove-VMGroupMember](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmgroupmember)  | Removes members from a virtual machine group. |
| remove_vm_hard_disk_drive | [Remove-VMHardDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmharddiskdrive)  | Deletes a hard disk drive from a virtual machine. |
| remove_vm_migration_network | [Remove-VMMigrationNetwork](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmmigrationnetwork)  | Removes a network from use with migration. |
| remove_vm_network_adapter | [Remove-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmnetworkadapter)  | Removes one or more virtual network adapters from a virtual machine. |
| remove_vm_network_adapter_acl | [Remove-VMNetworkAdapterAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmnetworkadapteracl)  | Removes an ACL applied to the traffic through a virtual network adapter. |
| remove_vm_network_adapter_extended_acl | [Remove-VMNetworkAdapterExtendedAcl](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmnetworkadapterextendedacl)  | Removes an extended ACL for a virtual network adapter. |
| remove_vm_network_adapter_routing_domain_mapping | [Remove-VMNetworkAdapterRoutingDomainMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmnetworkadapterroutingdomainmapping)  | Removes a routing domain from a virtual network adapter. |
| remove_vm_network_adapter_team_mapping | [Remove-VMNetworkAdapterTeamMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmnetworkadapterteammapping)  | Removes mapping for the virtual network adapters of a virtual machine to the management operating systems network team adapters. |
| remove_vm_remote_fx3d_video_adapter | [Remove-VMRemoteFx3dVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmremotefx3dvideoadapter)  | Removes a RemoteFX 3D video adapter from a virtual machine. |
| remove_vm_replication | [Remove-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmreplication)  | Removes the replication relationship of a virtual machine. |
| remove_vm_replication_authorization_entry | [Remove-VMReplicationAuthorizationEntry](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmreplicationauthorizationentry)  | Removes an authorization entry from a Replica server. |
| remove_vm_resource_pool | [Remove-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmresourcepool)  | Deletes a resource pool from one or more virtual machine hosts. |
| remove_vm_san | [Remove-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmsan)  | Removes a virtual storage area network (SAN) from a Hyper-V host. |
| remove_vm_saved_state | [Remove-VMSavedState](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmsavedstate)  | Deletes the saved state of a saved virtual machine. |
| remove_vm_scsi_controller | [Remove-VMScsiController](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmscsicontroller)  | Removes a SCSI controller from a virtual machine. |
| remove_vm_snapshot | [Remove-VMSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmsnapshot)  | Deletes a virtual machine checkpoint. |
| remove_vm_storage_path | [Remove-VMStoragePath](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmstoragepath)  | Removes a path from a storage resource pool. |
| remove_vm_switch | [Remove-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmswitch)  | Deletes a virtual switch. |
| remove_vm_switch_extension_port_feature | [Remove-VMSwitchExtensionPortFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmswitchextensionportfeature)  | Removes a feature from a virtual network adapter. |
| remove_vm_switch_extension_switch_feature | [Remove-VMSwitchExtensionSwitchFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmswitchextensionswitchfeature)  | Removes a feature from a virtual switch. |
| remove_vm_switch_team_member | [Remove-VMSwitchTeamMember](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/remove-vmswitchteammember)  | Removes a member from a virtual machine switch team. |
| rename_vm | [Rename-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vm)  | Renames a virtual machine. |
| rename_vm_group | [Rename-VMGroup](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmgroup)  | Renames virtual machine groups. |
| rename_vm_network_adapter | [Rename-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmnetworkadapter)  | Renames a virtual network adapter on a virtual machine or on the management operating system. |
| rename_vm_resource_pool | [Rename-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmresourcepool)  | Renames a resource pool on one or more Hyper-V hosts. |
| rename_vm_san | [Rename-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmsan)  | Renames a virtual storage area network (SAN). |
| rename_vm_snapshot | [Rename-VMSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmsnapshot)  | Renames a virtual machine checkpoint. |
| rename_vm_switch | [Rename-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/rename-vmswitch)  | Renames a virtual switch. |
| repair_vm | [Repair-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/repair-vm)  | Repairs one or more virtual machines. |
| reset_vm_replication_statistics | [Reset-VMReplicationStatistics](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/reset-vmreplicationstatistics)  | Resets the replication statistics of a virtual machine. |
| reset_vm_resource_metering | [Reset-VMResourceMetering](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/reset-vmresourcemetering)  | Resets the resource utilization data collected by Hyper-V resource metering. |
| resize_vhd | [Resize-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/resize-vhd)  | Resizes a virtual hard disk. |
| restart_vm | [Restart-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/restart-vm)  | Restarts a virtual machine. |
| restore_vm_snapshot | [Restore-VMSnapshot](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/restore-vmsnapshot)  | Restores a virtual machine checkpoint. |
| resume_vm | [Resume-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/resume-vm)  | Resumes a suspended (paused) virtual machine. |
| resume_vm_replication | [Resume-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/resume-vmreplication)  | Resumes a virtual machine replication that is in a state of Paused, Error, Resynchronization Required, or Suspended. |
| revoke_vm_connect_access | [Revoke-VMConnectAccess](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/revoke-vmconnectaccess)  | Revokes access for one or more users to connect to a one or more virtual machines. |
| save_vm | [Save-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/save-vm)  | Saves a virtual machine. |
| set_vhd | [Set-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vhd)  | Sets properties associated with a virtual hard disk. |
| set_vm | [Set-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vm)  | Configures a virtual machine. |
| set_vm_bios | [Set-VMBios](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmbios)  | Configures the BIOS of a Generation 1 virtual machine. |
| set_vm_com_port | [Set-VMComPort](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmcomport)  | Configures the COM port of a virtual machine. |
| set_vm_dvd_drive | [Set-VMDvdDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmdvddrive)  | Configures a virtual DVD drive. |
| set_vm_fibre_channel_hba | [Set-VMFibreChannelHba](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmfibrechannelhba)  | Configures a Fibre Channel host bus adapter on a virtual machine. |
| set_vm_firmware | [Set-VMFirmware](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmfirmware)  | Sets the firmware configuration of a virtual machine. |
| set_vm_floppy_disk_drive | [Set-VMFloppyDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmfloppydiskdrive)  | Configures a virtual floppy disk drive. |
| set_vm_hard_disk_drive | [Set-VMHardDiskDrive](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmharddiskdrive)  | Configures a virtual hard disk. |
| set_vm_host | [Set-VMHost](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmhost)  | Configures a Hyper-V host. |
| set_vm_host_cluster | [Set-VMHostCluster](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmhostcluster)  | Configures a virtual machine host cluster. |
| set_vm_key_protector | [Set-VMKeyProtector](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmkeyprotector)  | Configures a key protector for a virtual machine. |
| set_vm_memory | [Set-VMMemory](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmmemory)  | Configures the memory of a virtual machine. |
| set_vm_migration_network | [Set-VMMigrationNetwork](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmmigrationnetwork)  | Sets the subnet, subnet mask, and/or priority of a migration network. |
| set_vm_network_adapter | [Set-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadapter)  | Configures features of the virtual network adapter in a virtual machine or the management operating system. |
| set_vm_network_adapter_failover_configuration | [Set-VMNetworkAdapterFailoverConfiguration](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadapterfailoverconfiguration)  | Configures the IP address of a virtual network adapter to be used when a virtual machine fails over. |
| set_vm_network_adapter_team_mapping | [Set-VMNetworkAdapterTeamMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadapterteammapping)  | Configures mapping for the virtual network adapters of a virtual machine to the management operating systems network team adapters. |
| set_vm_network_adapter_vlan | [Set-VMNetworkAdapterVlan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadaptervlan)  | Configures the virtual LAN settings for the traffic through a virtual network adapter. |
| set_vm_processor | [Set-VMProcessor](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmprocessor)  | Configures one or more processors of a virtual machine. |
| set_vm_remote_fx3d_video_adapter | [Set-VMRemoteFx3dVideoAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmremotefx3dvideoadapter)  | Configures the RemoteFX 3D video adapter of a virtual machine. |
| set_vm_replication | [Set-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmreplication)  | Modifies the replication settings of a virtual machine. |
| set_vm_replication_authorization_entry | [Set-VMReplicationAuthorizationEntry](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmreplicationauthorizationentry)  | Modifies an authorization entry on a Replica server. |
| set_vm_replication_server | [Set-VMReplicationServer](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmreplicationserver)  | Configures a host as a Replica server. |
| set_vm_resource_pool | [Set-VMResourcePool](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmresourcepool)  | Sets the parent resource pool for a selected resource pool. |
| set_vm_san | [Set-VMSan](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmsan)  | Configures a virtual storage area network (SAN) on one or more Hyper-V hosts. |
| set_vm_security | [Set-VMSecurity](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmsecurity)  | Configures security settings for a virtual machine. |
| set_vm_security_policy | [Set-VMSecurityPolicy](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmsecuritypolicy)  | Configures the security policy for a virtual machine. |
| set_vm_switch | [Set-VMSwitch](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmswitch)  | Configures a virtual switch. |
| set_vm_switch_extension_port_feature | [Set-VMSwitchExtensionPortFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmswitchextensionportfeature)  | Configures a feature on a virtual network adapter. |
| set_vm_switch_extension_switch_feature | [Set-VMSwitchExtensionSwitchFeature](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmswitchextensionswitchfeature)  | Configures a feature on a virtual switch. |
| set_vm_switch_team | [Set-VMSwitchTeam](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmswitchteam)  | Configures a virtual switch team. |
| set_vm_video | [Set-VMVideo](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmvideo)  | Configures video settings for virtual machines. |
| set_vm_network_adapter_isolation | [Set-VmNetworkAdapterIsolation](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadapterisolation)  | Modifies isolation settings for a virtual network adapter. |
| set_vm_network_adapter_routing_domain_mapping | [Set-VmNetworkAdapterRoutingDomainMapping](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/set-vmnetworkadapterroutingdomainmapping)  | Sets virtual subnets on a routing domain. |
| start_vm | [Start-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/start-vm)  | Starts a virtual machine. |
| start_vm_failover | [Start-VMFailover](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/start-vmfailover)  | Starts failover on a virtual machine. |
| start_vm_initial_replication | [Start-VMInitialReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/start-vminitialreplication)  | Starts replication of a virtual machine. |
| start_vm_trace | [Start-VMTrace](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/start-vmtrace)  | Starts tracing to a file. |
| stop_vm | [Stop-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/stop-vm)  | Shuts down, turns off, or saves a virtual machine. |
| stop_vm_failover | [Stop-VMFailover](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/stop-vmfailover)  | Stops failover of a virtual machine. |
| stop_vm_initial_replication | [Stop-VMInitialReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/stop-vminitialreplication)  | Stops an ongoing initial replication. |
| stop_vm_replication | [Stop-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/stop-vmreplication)  | Cancels an ongoing virtual machine resynchronization. |
| stop_vm_trace | [Stop-VMTrace](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/stop-vmtrace)  | Stops tracing to file. |
| suspend_vm | [Suspend-VM](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/suspend-vm)  | Suspends, or pauses, a virtual machine. |
| suspend_vm_replication | [Suspend-VMReplication](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/suspend-vmreplication)  | Suspends replication of a virtual machine. |
| test_vhd | [Test-VHD](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/test-vhd)  | Tests a virtual hard disk for any problems that would make it unusable. |
| test_vm_network_adapter | [Test-VMNetworkAdapter](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/test-vmnetworkadapter)  | Tests connectivity between virtual machines. |
| test_vm_replication_connection | [Test-VMReplicationConnection](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/test-vmreplicationconnection)  | Tests the connection between a primary server and a Replica server. |
| update_vm_version | [Update-VMVersion](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/update-vmversion)  | Updates the version of virtual machines. |
|  | [](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/)  |  |
|  | [](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/)  |  |
|  | [](https://docs.microsoft.com/en-us/powershell/module/hyper-v/?view=win10-ps/)  |  |

## <a name="Usage"></a> Usage

### <a name="BasicUsage"></a> Basic Usage

The actions that are created are fairly simplistic, simply executing the PowerShell
cmdlet that they represent along with any arguments that are passed in via the `args`
parameter on the action.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld'
st2 run activedirectory.new_ad_computer args='NEWCOMPUTER' hostname='windowshost.domain.tld'
```

Every cmdlet action has a required `hostname` parameter that is the hostname of
the remote windows box that we will execute the cmdlet on. Please ensure that
hosts have the [Prerequisites](#Prerequisites) installed properly (WinRM and RSAT tools)

### <a name="Authentication"></a> Authentication

When logging in to a system and invoking commands you will need to authenticate
to login to the host, and maybe need to pass in a different set of credentials
to the cmdlet. When logging in to the remote system there are two ways to pass
in authentication credentials to the action.

#### Options:
- username/password parameters passed directly to the action
- credential_name parameter passed to the action

#### username/password parameters
In this case the username/password are specified where the action is invoked,
thus allowing you to pass in credentials on the commandline for easy testing.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld' username='user@domain.com' password='Password1'
```

#### credential_name parameter
In this case the name of the credential to used is passed in where the action
is invoked, and the actual credentials themselves are stored in the pack's
configuration file `/opt/stackstorm/configs/activedirectory.yaml`.

Let's say we had a configuration file with the contents:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  dev:
    username: username@dev.domain.tld
    password: xxx
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
```

We could invoke an action using the `dev` credentials to login to `hostname` like so:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev'
```

Similarly if we wanted to invoke the same action using the `test` credentials:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='testhost.domain.tld' credential_name='test'
```

### <a name="CmdletAuthentication"></a> Cmdlet Authentication

When executing a PowerShell cmdlet the it normally uses the credentials of
the currently logged in user. In our case this would either be `username/password`
or the username/password associated with the `credential_name` in the config.
Alternativey, the cmdlets in the ActiveDirectory PowerShell module can take an
optional `-Credential` parameter that is used to provide different credentials
for the executin of the command itself (example, maybe a specific command requires
an elevated set of priveleges). The PowerShell for a normal command looks like:

``` PowerShell
Get-ADUser someuser
```

To execute this with a different set of credentials it would look like:

``` PowerShell
$securepass = ConvertTo-SecureString "Password!" -AsPlainText -Force
$admincreds = New-Object System.Management.Automation.PSCredential("username@domain.com", $securepass)
Get-ADUser -Credential $admincreds someuser
```

Because it is a fairly common scenario this use-case has been baked into the actions
within this pack. To execute a command with an elevated set of credentials there
are two options, just like host authentication.

#### Options:
- cmdlet_username/cmdlet_password parameters passed directly to the action
- cmdlet_credential_name parameter passed to the action


#### cmdlet_username/cmdlet_password parameters
In this case the cmdlet_username/cmdlet_password are specified where the action
is invoked, thus allowing you to pass in credentials on the commandline for easy
testing.

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='windowshost.domain.tld' username='user@domain.com' password='Password1' cmdlet_username='elevated@domain.com' cmdlet_password='SuperSecurePassword'
```

#### cmdlet_credential_name parameter
In this case the name of the credential to used is passed in where the action
is invoked, and the actual credentials themselves are stored in the pack's
configuration file `/opt/stackstorm/configs/activedirectory.yaml`.

Let's say we had a configuration file with the contents:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  dev:
    username: username@dev.domain.tld
    password: xxx
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
  elevated:
    username: username@test.domain.tld
    password: xxx
    port: 5522
```

We could invoke an action using the `dev` credentials to login to `hostname` and
then using the `elevated` set of credentials for the cmdlet execution like so:

``` shell
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev' cmdlet_credential_name='elevated'
```

### <a name="TransportPort"></a> Transport/Port

We provide the ability to specialize _how_ we connect to a host using WinRM by
allowing the `transport` and `port` to be overridden. The `transport` is the connection
protocol used to perform WinRM authentication. The `port` is the network port to
use to make the connection to the remote host.

The default, and recommended `transport` and `port` is: `transport='ntlm' port='5986'`

This pack supports all transports that are supported by the [pywinrm](https://github.com/diyan/pywinrm/)
python module. As of the time of writing the valid transports are:

- `basic`
- `plaintext`
- `certificate`
- `ssl`
- `kerberos`
- `ntlm`
- `credssp`

For more info on how to use and setup your Windows host for these various transports
please refer to the [pywinrm](https://github.com/diyan/pywinrm/) documentation.


#### Transport/Port Overrides

We provide the following options for specifying what `transport` and `port` to use
for the connection (ordered in terms of highest priority):

1. if transport/port specified as action params, use this
2. if transport/port specified as params on the credentials in config
3. if transport/port specified at root level in the config
4. else, use the default transport/port (5986/ntlm)


#### Transport/Port as Action Params

The most specific case is passing in the `transport`/`port` as parameters to
the action when you invoke it:

``` shell
# will use transport='basic' and port='1234' from the invokation
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name='dev' port='1234' transport='basic'
```

#### Transport/Port as From Credentials in Config

Alternatively, if you pass in a `credential_name` to the action invokation
and that credential has the `transport` and `port` options set in the config, then
we'll automatically look up and utilize those values.

Example config:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
    port: 5522
    transport: basic
```

``` shell
# will use transport='basic' and port=5522 from the 'test' credential in the config
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


#### Transport/Port as From Config Root

If the credential doesn't have `transport`/`port` defined then we'll use the "global"
settings for `transport` and `port` at the root level of the config

Example config:

``` yaml
---
port: 5986
transport: ntlm

activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
```

``` shell
# will use transport='ntlm' and port=5986 from the root of the config
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


#### Transport/Port default

Finally if there are no `transport`/`port` specified as params, or in the config
we'll use our packs built-in default of `transport='ntlm' port='5986'`.

Example config:

``` yaml
---
activedirectory:
  test:
    username: username@test.domain.tld
    password: xxx
```

``` shell
# will use transport='ntlm' and port=5986 from the pack's built-in defaults
st2 run activedirectory.get_ad_computer args='COMPUTERTOFIND' hostname='devhost.domain.tld' credential_name=test'
```


## <a name="Output"></a> Output

In an effort to be flexible and play well with StackStorm we have coded up this
pack to allow for the output of the actions to be in one of the following formats:

- json (default)
- raw

### <a name="JSON"></a> JSON

JSON output works by appending `| ConvertTo-Json` to the end of the powershell
cmdlet being run and converts any exceptions that are thrown into JSON. The
exact code that gets executed is:

``` PowerShell
Try
{
  <cmdlet> | ConvertTo-Json
}
Catch
{
  $formatted_output = ConvertTo-Json -InputObject $_
  $host.ui.WriteErrorLine($formatted_output)
  exit 1
}
```

This takes the resulting PowerShell object and converts it to
JSON representation. The benefit of this is that by using JSON it allows us
to parse it into a python `dict` and then return it from the action. This allows
the end-user to utilize the output in a meaningful way within workflows. To utilize
this dictionary parsed output there are two variables `stdout_dict` and `stderr_dict`
that are populated. If no output is present an empty dictionary is returned.

**Example Mistral workflow usage:**

``` yaml
version: '2.0'

activedirectory.json-example:
    description: Workflow demoing the json parsed output
    type: direct
    input:
        - hostname
        - username
        - password
        - computer
    output:
        dns_hostname: <% $.dns_hostname %>
    tasks:
        task1:
            action: activedirectory.get_ad_computer hostname=<% $.hostname %> args="<% $.computer %>" username=<% $.username %> password=<% $.password %> cmdlet_username=<% $.username %> cmdlet_password=<% $.password %>
            publish:
                dns_hostname: <% task(task1).result.result.stdout_dict.DNSHostName %>
                stderr_dict: <% task(task1).result.result.stderr_dict %>
```

### <a name="Raw"></a> Raw

Raw output is simply the stdout/stderr strings returned to you. In this case
the output variables `stdout` and `stderr` would be your interaction point.
The variables `stdout_dict` and `stderr_dict` will be set to empty dictionaries.



# <a name="FutureIdeas"></a> Future Ideas
-  Create action to install Active Directory
   https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-#BKMK_PS
   Active Directory Deployment Services (ADDS) cmdlets: https://technet.microsoft.com/en-us/itpro/powershell/windows/addsdeployment/addsdeployment
   ``` PowerShell
   Import-Module ServerManager
   Install-WindowsFeature -IncludeManagementTools -Name AD-Domain-Services
   Import-Module ADDSDeployment
   Get-Command -Module ADDSDeployment
   ???
   ```
- Create sensors that monitor events in AD
  - Users added/removed
  - Computers added/removed
  - Groups added/removed
  - Users added/removed from groups
