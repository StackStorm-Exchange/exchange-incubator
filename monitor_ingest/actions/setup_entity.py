import yaml
from st2common.runners.base_action import Action
from mam.sdk import (entitytype, constants, kpifunction, dimension)

__all__ = ['SetupEntityAction']


class SetupEntityAction(Action):
    def __init__(self, config):
        super(SetupEntityAction, self).__init__(config)
        self._config = self.config
        self._credentials = self._config.get('credentials', None)
        self._data_file_path = self._config.get('data_file_path', None)
        self._action_type = self._config.get('action_type', None)

        if not self._config:
            raise ValueError('Missing config yaml')
        if not self._credentials:
            raise ValueError('Missing IBM Watson IoT credentials in config file')
        if not self._data_file_path:
            raise ValueError('Missing data file path in config file')
        if not self._action_type:
            raise ValueError('Missing action type key in config file')

    def run(self):
        status = False
        if self._action_type == "SetupEntityAction":
            self.setup_EntityAction()
        elif self._action_type == "SetupAddConstants":
            self.setup_AddConstants()
        elif self._action_type == "SetupAddDimensions":
            self.setup_AddDimensions()
        elif self._action_type == "SetupAddFunctions":
            self.setup_AddFunctions()
        return status

    def setup_EntityAction(self):
        if self._data_file_path:
            """------Usage: 1. (X) Create Entity Type - using a json payload-----"""
            with open(self._data_file_path, 'r') as f:
                try:
                    op_create = entitytype.create_custom_entitytype(f.read(),
                                                                    credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_create}. \nEntity created successfully')
                    return True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed create Entity Type operation')
                    return False

    def setup_AddFunctions(self):
        if self._data_file_path:
            """------Usage: 2. (X) Add Function - using a json payload------"""
            with open(self._data_file_path, 'r') as f:
                try:
                    op_add = kpifunction.add_functions(f.read(),
                                                       credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_add}. \nKPI Functions added successfully')
                    return True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed add functions operation')
                    return False

    def setup_AddDimensions(self):
        if self._data_file_path:
            """------Usage: 3. (X) Add Dimension - using a json payload------"""
            with open(self._data_file_path, 'r') as f:
                try:
                    op_add = dimension.add_dimensions_data(f.read(),
                                                           credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_add}. \nDimension data added successfully')
                    return True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed add dimension data operation')
                    return False

    def setup_AddConstants(self):
        if self._data_file_path:
            """------Usage: 4. (X) Create Constants - using a json payload------"""
            with open(self._data_file_path, 'r') as f:
                try:
                    op_create = constants.create_constants(f.read(),
                                                           credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_create}. \nConstants created successfully')
                    return True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed Create Constants operation')
                    return False
