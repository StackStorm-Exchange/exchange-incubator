import yaml
from st2common.runners.base_action import Action
from mam.sdk import entitytype

__all__ = ["IngestCsvDataAction"]


class IngestCsvDataAction(Action):
    def __init__(self, config):
        super(IngestCsvDataAction, self).__init__(config)
        self._config = self.config
        self._credentials = self._config.get('credentials', None)
        self._data_file_path = '/opt/stackstorm/packs/monitor_ingest/etc/' \
                                'clean_data_output/clean_data.csv'
        self._entity_name = self._config.get('entity_name', None)
        
        if not self._config:
            raise ValueError('Missing config yaml')
        if not self._credentials:
            raise ValueError('Missing IBM Watson IoT credentials in config file')
        if not self._data_file_path:
            raise ValueError('Missing CSV data file path in config file')
        if not self._entity_name:
            raise ValueError('Missing Entity name in config file')
            
    def run(self):
        success = False
        if self._data_file_path:
            """-------Usage: 1. (X) Load Csv Data - using a CSV payload-------"""
            try:
                entitytype.load_metrics_data_from_csv(self._entity_name, 
                                                      self._data_file_path, 
                                                      credentials = self._credentials)
                success = True
            except Exception as msg:
                print(f"FAILED STEP: {msg}\nFailed loading CSV data")
        return success
