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
        operations_completed = {}

        if self._action_type == "SetupEntityAction":
            self.setup_EntityAction(operations_completed)
        elif self._action_type == "SetupAddConstants":
            self.setup_AddConstants(operations_completed)
        elif self._action_type == "SetupAddDimesions":
            self.setup_AddDimesions(operations_completed)
        elif self._action_type == "SetupAddFunctions":
            self.setup_AddFunctions(operations_completed)

        """----------STATUS----------"""
        self.logger.info('RESULT :')
        for name, status in operations_completed.items():
            self.logger.info(f'Operation: {name} status: {status}')
            if status:
                success = True
            else:
                success = False

        return success

    def setup_EntityAction(self, operations_completed):
        if self._data_file_path:
            """------Usage: 1. (X) Create Entity Type - using a json payload-----"""
            operations_completed['create_entity'] = False
            with open(self._data_file_path, 'r') as f:
                try:
                    op_create = entitytype.create_custom_entitytype(f.read(),
                                                                    credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_create}. \nEntity created successfully')
                    operations_completed['create_entity'] = True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed create Entity Type operation')

    def setup_AddFunctions(self, operations_completed):
        if self._data_file_path:
            """------Usage: 2. (X) Add Function - using a json payload------"""
            operations_completed['add_functions'] = False
            with open(self._data_file_path, 'r') as f:
                try:
                    op_add = kpifunction.add_functions(f.read(),
                                                       credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_add}. \nKPI Functions added successfully')
                    operations_completed['add_functions'] = True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed add functions operation')

    def setup_AddDimesions(self, operations_completed):
        if self._data_file_path:
            """------Usage: 3. (X) Add Dimension - using a json payload------"""
            operations_completed['add_dimension_data'] = False
            with open(self._data_file_path, 'r') as f:
                try:
                    op_add = dimension.add_dimensions_data(f.read(),
                                                           credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_add}. \nDimension data added successfully')
                    operations_completed['add_dimension_data'] = True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed add dimension data operation')

    def setup_AddConstants(self, operations_completed):
        if self._data_file_path:
            """------Usage: 4. (X) Create Constants - using a json payload------"""
            operations_completed['create_constants'] = False
            with open(self._data_file_path, 'r') as f:
                try:
                    op_create = constants.create_constants(f.read(),
                                                           credentials=self._credentials)
                    self.logger.info(f'ret_code is {op_create}. \nConstants created successfully')
                    operations_completed['create_constants'] = True
                except Exception as msg:
                    self.logger.debug(f'FAILED STEP: {msg}\nFailed Create Constants operation')

