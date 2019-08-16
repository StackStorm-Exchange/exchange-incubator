from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import os
import time
import subprocess
import sys
from st2common.runners.base_action import Action


    
class cisco_rom_mon_upgrade(Action):

    def run(self,IP,USERNAME,PASSWORD,ROM_MON_IMAGE,MD5_CHECKSUM):
        """
        This function is used by stack storm to run the code and based
        on the return code see if is successful or if it failed.
        """

        """
        Setting the device values for netmiko to connect to the device.
        """
        rom_image = ROM_MON_IMAGE
        md5_checksum = MD5_CHECKSUM

        device_profile = {
                'device_type' : 'cisco_ios',
                'ip' : IP,
                'username': USERNAME,
                'password': PASSWORD,
            }
        try:
            net_connect = ConnectHandler(**device_profile)
        except (AuthenticationException):
            print ("Authentication failure ")
        except (NetMikoTimeoutException):
            print (' Timeout to device ')
        except (EOFError):
            print (' End of file while attempting device ')
        except (SSHException):
            print ('SSH issue. Are you sure SSH is enable ')
        except Exception as unknown_error:
            print (' Some other Error:' + unknown_error)
        
        current_rom_mon_version = net_connect.send_command('sh rom-monitor R0 | in Version')
        
        print("-------------------------------------------------")
        print('Checking ROM-MON MD5 Checksum - Please Wait')
        print("-------------------------------------------------")
        """
        Connects to the device via netmiko and run the command "verify /md5 bootflash:" and the rom image provided
        """
        checking_md5 = net_connect.send_command('verify /md5 bootflash:{}'.format(rom_image))
        
        """
        Perform MD5 Checksum match with the value provided when the image was transfer.
        If the MD5 checksum matches it will clear the boot variables and configure the 
        new boot template on the device, if the MD5 checksum does not match the sript will cancel himself
        """

        if md5_checksum in checking_md5:
            print("-------------------------------------------------")
            print("ROM-MON MD5 Checksum Matched")
            print("-------------------------------------------------")
        else:
            print("-------------------------------------------------")
            print("ERROR ROM-MON MD5 CODE DOES NOT MATCH")
            print("-------------------------------------------------")
            return False, "ERROR ROM-MON MD5 CODE DOES NOT MATCH"
            exit()

        print("-------------------------------------------------")
        print("Upgrading ROM-MON Now")
        print("-------------------------------------------------")
        rom_mon_upgrade = net_connect.send_command('upgrade rom-monitor filename bootflash:{} all\n'.format(rom_image),
        delay_factor=10)
        print("-------------------------------------------------")
        print(rom_mon_upgrade)
        print("-------------------------------------------------")

        rom_mon_upgrade_result = 'To make the new ROMMON permanent, you must restart the RP'

        if rom_mon_upgrade_result in rom_mon_upgrade:
            print("-------------------------------------------------")
            print("Rebooting Device Now")
            print("-------------------------------------------------")
        else:
            print("-------------------------------------------------")
            print('Breaking Script')
            print("-------------------------------------------------")
            return False, "ROM MON Upgrade result was not the expected one, Cancelling device reboot."
            exit()

        """
        Reboots the router
        """
        reboot = net_connect.send_command_timing('reload')
        enter  = net_connect.send_command_timing('\n')

        time.sleep(30)
        
        proc = subprocess.Popen(
            ['ping', '-q', '-c', '3', IP],
            stdout=subprocess.DEVNULL)
        proc.wait()
        
        
        animation = "|/-\\"
        idx = 0
        """
        This is a loop that sends ping to the device and if it does not reply it will continue to send pings to the 
        device, there is a animation configured so while we wait for the device to comeback the scripts looks like is loading,
        once the device is backup the loop will end and the script will print that the device is back up.
        """
        while proc.returncode != 0:
            proc = subprocess.Popen(
            ['ping', '-q', '-c', '1', IP],
            stdout=subprocess.DEVNULL)
            proc.wait()
            print("Waitting for Device to Return:")
            idx += 1
        else:
            sys.stdout.flush()
            print("-------------------------------------------------")
            print("Device is now up")
            print("-------------------------------------------------")

        print("-------------------------------------------------")
        print("Checking if ROM-MON Upgrade was successful")
        print("-------------------------------------------------")
        
        time.sleep(10)

        try:
            net_connect = ConnectHandler(**device_profile)
        except (AuthenticationException):
            print ("Authentication failure " )
        except (NetMikoTimeoutException):
            print (' Timeout to device ' )
        except (EOFError):
            print (' End of file while attempting device ')
        except (SSHException):
            print ('SSH issue. Are you sure SSH is enable ')
        except Exception as unknown_error:
            print (' Some other Error:' + unknown_error)

        new_rom_mon_version = net_connect.send_command('sh rom-monitor R0 | in Version')

        print("-------------------------------------------------")
        print(new_rom_mon_version)
        print("-------------------------------------------------")

        if new_rom_mon_version == current_rom_mon_version:
            return False, "ROM MON version did not changed "
        else:
            return True, "ROM MON version has been upgraded"


