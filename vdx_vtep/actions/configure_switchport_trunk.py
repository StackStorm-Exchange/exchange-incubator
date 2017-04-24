from st2actions.runners.pythonrunner import Action
import pynos.device

class CreateSwitchPort(Action):
    """
       Implements the logic to create switch-port on an interface on VDX Switches .
       This action acheives the below functionality
           1.Check specified interface is L2 or L3,continue only if L2 interface.
           2.Configure switch port trunk allowed vlan add with vlan specified by user on the L2
           interface .
    """
    
    def __init__(self, config=None):
        super(CreateSwitchPort, self).__init__(config=config)

    def run(self, host=None, username=None, password=None, intf_type=None, vlan=None, switch_ports=None):
        """Run helper methods to implement the desired state.
        """
        if host is None:
            host = self.config['vip']
            
        if username is None:
            username = self.config['username']
            
        if password is None:
            password = self.config['password']
            
        if intf_type is None:
           intf_type = self.config['intf_type']

        if vlan is None:
            vlan =self.config['vlan']
            
        switch_ports = switch_ports.split(",")
            
        conn = (host, '22')
        auth = (username, password)
        changes = {}

        with pynos.device.Device(conn=conn, auth=auth) as device:
            for intf_name in switch_ports:
                if intf_name:
                    changes['switchport_trunk_config' + intf_name] = self._create_switchport(device, intf_type,intf_name, vlan)
                    changes['tag_native_vlan' + intf_name] = self._tag_native_vlan(device, intf_type, intf_name)
        return changes

    def _check_requirements_L2_interface(self, device, intf_type, intf_name):
        """Fail the task if interface is an L3 interface .
        """
        try:
            version1 = 4
            version2 = 6
            get_ipv4 = device.interface.get_ip_addresses(int_type=intf_type, name=intf_name,
                                                         version=version1)
            get_ipv6 = device.interface.get_ip_addresses(int_type=intf_type, name=intf_name,
                                                         version=version2)
            if get_ipv4 or get_ipv6:
                self.logger.warning("Interface %s %s specified is an L3 interface", intf_type,
                                    intf_name)
                return False
            else:
                self.logger.info("Interface is L2 interface.")
                return True

        except (ValueError):
            self.logger.info("interface type or name invalid.")
        return False

    def _check_requirements_switchport_exists(self, device, intf_type, intf_name, vlan):
        """ Fail the task if switch port exists.
        """

        try:
            return_code = device.interface.switchport(int_type=intf_type, name=intf_name,
                                                      get='True')
            parse_string = return_code.data.find('.//{*}switchport-basic')
            if parse_string is not None:
                result = device.interface.switchport_list
                vlan_range = (list(self._validate_vlan(vlan)))
                for intf in result:
                    if intf['interface-name'] == intf_name:
                        if intf['mode'] == 'trunk':
                            if intf['vlan-id'] is not None:
                                if len(intf['vlan-id']) > len(vlan_range):
                                    return False
                                ret = self._check_list(vlan_range, intf['vlan-id'])
                                if ret:
                                    if len(ret) == len(vlan_range):
                                        return False
                            else:
                                return True
                        else:
                            self.logger.info("Access mode is configured on interface,\
                                 Pls removed and re-configure")
                            return False
        except (ValueError):
            self.logger.info("Fetching Switch port enable failed")
            return False
        return True

    def _check_list(self, input_list, switch_list):
        """ Check if the input list is in switch list """
        return_list = []
        for vid in input_list:
            if str(vid) in switch_list:
                return_list.append(vid)
        return return_list

    def _create_switchport(self, device, intf_type, intf_name, vlan):
        """ Configuring Switch port trunk allowed vlan add on the interface with the vlan."""
        try:
            #If port is a port-profile-port then disable it and enable switchport
            if device.interface.port_profile_port(inter_type=intf_type, inter=intf_name):
                device.interface.port_profile_port(inter_type=intf_type, inter=intf_name,enable=False)

            #Logic to set interface mode trunk and add allowed vlans.
            device.interface.enable_switchport(inter_type=intf_type, inter=intf_name)
            device.interface.switchport(int_type=intf_type, name=intf_name)
            device.interface.trunk_mode(int_type=intf_type, name=intf_name, mode='trunk')
            device.interface.trunk_allowed_vlan(int_type=intf_type, name=intf_name, action='all')

        except Exception as e:
            self.logger.error("Configuring interface as a switchport failed with error:%s" %e)

        return True

    def _disable_isl(self, device, intf_type, intf_name):
        """Disable ISL on the interface.
        """
        conf = device.interface.fabric_isl(get=True, name=intf_name, int_type=intf_type)
        conf = conf.data.find('.//{*}fabric-isl')
        if conf is None:
            return False
        self.logger.info("disabling isl on %s %s", intf_type, intf_name)
        device.interface.fabric_isl(enabled=False, name=intf_name, int_type=intf_type)
        return True

    def _disable_fabric_trunk(self, device, intf_type, intf_name):
        """Disable ISL Fabric Trunk on the interface.
        """
        conf = device.interface.fabric_trunk(get=True, name=intf_name, int_type=intf_type)
        conf = conf.data.find('.//{*}fabric-trunk')
        if conf is None:
            return False
        self.logger.info("disabling fabric trunk on %s %s", intf_type, intf_name)
        device.interface.fabric_trunk(enabled=False, name=intf_name, int_type=intf_type)
        return True
        
    def _tag_native_vlan(self, device, intf_type, intf_name):
        try:
            output = device.interface.tag_native_vlan(int_type = 'tengigabitethernet', name = intf_name, enabled = True)
            output = device.interface.tag_native_vlan(int_type = 'tengigabitethernet', name = intf_name, enabled = False)
        except ValueError:
            self.logger.info("Configuring Switch port trunk failed")
        return True
        
    def _validate_vlan(self, vlan_id):
        """Fail the task if vlan id is zero or one or above 4096 .
        """

        re_pattern1 = r"^(\d+)$"
        re_pattern2 = r"^(\d+)\-?(\d+)$"

        if re.search(re_pattern1, vlan_id):
            try:
                vlan_id = (int(vlan_id),)
            except ValueError:
                self.logger.info("Could not convert data to an integer.")
                return None
        elif re.search(re_pattern2, vlan_id):
            try:
                vlan_id = re.match(re_pattern2, vlan_id)
            except ValueError:
                self.logger.info("Not in valid range format.")
                return None

            if int(vlan_id.groups()[0]) == int(vlan_id.groups()[1]):
                self.logger.warning("Use range command only for diff vlans")
            vlan_id = range(int(vlan_id.groups()[0]), int(vlan_id.groups()[1]) + 1)

        else:
            self.logger.info("Invalid vlan format")
            return None

        for vid in vlan_id:
            if vid > 4096:
                extended = "true"
            else:
                extended = "false"
            tmp_vlan_id = pynos.utilities.valid_vlan_id(vid, extended=extended)
            reserved_vlan_list = range(4087, 4096)
            reserved_vlan_list.append(1002)

            if not tmp_vlan_id:
                self.logger.info("'Not a valid VLAN %s", vid)
                return None
            if vid == 1:
                self.logger.info("vlan %s is default vlan", vid)
                return None
            elif vid in reserved_vlan_list:
                self.logger.info("Vlan cannot be created, as it is not a user/fcoe vlan %s", vid)
                return None

        return vlan_id
