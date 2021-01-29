import json
from decimal import Decimal

import numpy as np
import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation
from st2common.runners.base_action import Action

__all__ = ["CleanCsvDataAction"]


class CleanCsvDataAction(Action):
    def __init__(self, config):
        super(CleanCsvDataAction, self).__init__(config)
        self._config = self.config
        self._data_file_path = self._config.get('data_file_path', None)
        self._json_schema_path = self._config.get('json_schema_path', None)

        if not self._config:
            raise ValueError('Missing config yaml')
        if not self._data_file_path:
            raise ValueError('Missing CSV data file path in config file')
        if not self._json_schema_path:
            raise ValueError('Missing JSON Schema data file path in config file')

    def check_decimal(dec):
        try:
            Decimal(dec)
        except ValueError:
            return False
        return True

    def check_time_stamp(dt):
        try:
            pd.to_datetime(dt)
        except ValueError:
            return False
        return True

    def check_int(num):
        try:
            int(num)
        except ValueError:
            return False
        return True

    def run(self):
        # define validation elements
        print('1. Starting data Clean Action ..')
        success = False
        VALIDATORS = {
            'decimal': CustomElementValidation(
                lambda d: CleanCsvDataAction.check_decimal(d), 'is not decimal'),
            'int': CustomElementValidation(lambda i: CleanCsvDataAction.check_int(i),
                                           'is not integer'),
            'null': CustomElementValidation(lambda d: d is not np.nan,
                                            'this field cannot be null'),
            'time_stamp': CustomElementValidation(
                lambda d: CleanCsvDataAction.check_time_stamp(d),
                'time_stamp format is not valid')
        }
        print('2. Loading Schema ..')
        with open(self._json_schema_path, 'r') as my_json:
            json_schema = json.load(my_json)
        column_list = [Column(k, [VALIDATORS[v] for v in vals]) for k, vals in
                       json_schema.items()]
        schema = pandas_schema.Schema(column_list)
        print('3. Loading CSV Data ..')
        data = pd.read_csv(self._data_file_path)
        print(data)
        try:
            print('4. Validating input CSV data ..')
            errors = schema.validate(data)
            for e in errors:
                print(e)
            if errors:
                errors_index_rows = [e.row for e in errors]
                print('5. Cleaning input CSV data ..')
                data_clean = data.drop(index=errors_index_rows)
                pathoffile = '/opt/stackstorm/packs/monitor_mqtt/etc/clean_data_output' \
                          '/errors.csv'
                message = 'Error Data file: ' + pathoffile
                print(message)
                pd.DataFrame({'col': errors}).to_csv(
                    '/opt/stackstorm/packs/monitor_mqtt/etc/clean_data_output/errors.csv')
            else:
                print('5. Couldn`t found issue with input CSV ..')
                data_clean = data
                cleanpath = '/opt/stackstorm/packs/monitor_mqtt/etc/clean_data_output' \
                          '/clean_data.csv'
                cleanmessage = 'Clean Data path: ' + cleanpath
            print(cleanmessage)
            data_clean.to_csv(
                '/opt/stackstorm/packs/monitor_mqtt/etc/clean_data_output/clean_data.csv')
            success = True
            print('Action Completed Successfully')
        except Exception as msg:
            print(f"FAILED STEP: {msg}\n FAILED: Clean Data Action")
        return success
