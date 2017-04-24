from NSX.nsx import NSX
from st2actions.runners.pythonrunner import Action
import logging
import os

class addHardwareGw(Action):
    def run(self, nsx_mgr_ip=None, nsx_mgr_user=None, nsx_mgr_pass=None, gw_name=None, nsx_cert=None):
        if nsx_mgr_ip is None:
            nsx_mgr_ip = self.config['nsx_mgr_ip']

        if nsx_mgr_user is None:
            nsx_mgr_user = self.config['nsx_mgr_user']

        if nsx_mgr_pass is None:
            nsx_mgr_pass = self.config['nsx_mgr_pass']

        if gw_name is None:
            gw_name = self.config['gw_name']
        
        cert = nsx_cert

        self.logger = logging.getLogger(__name__)
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        file_path =  os.path.relpath("nsxraml/nsxvapi.raml")
        controller = NSX(raml_file= file_path, password=nsx_mgr_pass, username=nsx_mgr_user, ip=nsx_mgr_ip)
        changes = {}
        changes['pre_requisites'] = self._check_requirements(controller, cert, gw_name)
        changes['add_hw_gw'] = False
        if changes['pre_requisites']:
            changes['add_hw_gw'] = self._add_hw_gw_cert(controller, cert, gw_name)
        else:
            self.logger.info('Pre-requisites validation failed for hardware gateway addition.')
        if changes['add_hw_gw']:
            self.logger.info(
                'closing connection to %s after configuring hardware gateway successfully!' % nsx_mgr_ip)
            return changes
        else:
            self.logger.info('Hardware gateway: %s installation failed.' % gw_name)
            exit(1)

    def _check_requirements(self,controller, cert, hw_gw):
        '''
        Checks if hardware_gw with the same name exists.
        '''

        # Logic to check of hw_gw is configured on the nsx-controller.
        result = controller.get_hwdevice()
        gws = []
        if result is not None:
            gws = result['hardwareGateway']
        hwgw_present = False
        if isinstance(gws, dict):
            if gws['name'] == str(hw_gw):
                hwgw_present = True
        else:
            for gw in gws:
                if gw['name'] == str(hw_gw):
                    hwgw_present = True
                    break
        if hwgw_present:
            self.logger.info('Hardware gateway: %s present on the nsx-controller' % hw_gw)
            return False

        #Logic to cvalidate certificate.
        if 'BEGIN CERTIFICATE' and 'END CERTIFICATE'not in cert:
            self.logger.info('Invalid Certificate')
            return False

        return True

    def _add_hw_gw_cert(self, controller, cert, gw_name):
        '''
        Install a hardware gateway
        '''
        try:
            result = controller.add_hwdevice_cert(cert=cert, name=gw_name, bfd=True)
            return result
        except Exception as e:
            self.logger.error('Failed to add hardware gateway with error: %s' %e)
            return "ssss"
            return False
