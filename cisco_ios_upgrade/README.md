### cisco_ios_upgrade

 This is a simple pack that allows users to transfer files from a folder inside /opt/stackstorm/files_repo/ to a cisco device and then easily perform an IOS upgrade or ROM MON upgrade on the device.

1. First this is to install the pack using the command below, after that is complete you will need to create a folder called files_repo in the directory /opt/stackstorm/ to store ios images and rom mon packages.

```
make sure the virtual enviroment is python 3.
##CentOS
st2 pack install https://github.com/NetDevLazg/cisco_ios_upgrade.git --python3
##Ubuntu
st2 pack install https://github.com/NetDevLazg/cisco_ios_upgrade.git
```

2. After you create the folder files_repo create two new folder inside and called them ios_repo and rom_mon_repo.

3. Store ios images insides ios_repo and rom_mon packages inside rom_mon_repo.

```
Example of File path:

/opt/stackstorm/files_repo/
├── ios_repo
│   ├── csr1000v-universalk9.16.06.06.SPA.bin
│   └── csr1000v-universalk9.16.09.03.SPA.bin
└── rom_mon_repo
    └── isr4200_4300_rommon_1612_1r_SPA.pkg

2 directories, 3 files

```

4. After the folder is created and the corresponding image is inside you can start to use the actions to transfer the images to the devices and then run the upgrade.

## prerequisites
1. Make sure the virtual enviroment has netmiko
2. Make sure the cisco device has scp enable if not then run this command
```
ip scp server enable
```
