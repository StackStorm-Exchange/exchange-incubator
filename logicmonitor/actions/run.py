import logicmonitor_sdk
from logicmonitor_sdk.rest import ApiException
from pprint import pprint
from st2common.runners.base_action import Action

class ActionWrapper(Action):
  def __init__(self, config):
      super(ActionWrapper, self).__init__(config)
      self.company = config['company']
      self.access_id = config['access_id']
      self.access_key = config['access_key']

  def run(self, **kwargs):
      # Configure API key authorization: LMv1
      configuration = logicmonitor_sdk.Configuration()
      configuration.company = self.company
      configuration.access_id = self.access_id
      configuration.access_key = self.access_key
      # configuration.verify_ssl = False # set to false to make testing easier

      api_instance = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(configuration))
      sdk_method = kwargs.pop('method')
      for key in kwargs.copy():
        if kwargs[key] == None:
            kwargs.pop(key)

      try:
          api_response = getattr(api_instance, sdk_method)(**kwargs)
          pprint(api_response)
      except ApiException as e:
          print('Exception when calling LMApi->' + sdk_method + ': %s\n' % e)