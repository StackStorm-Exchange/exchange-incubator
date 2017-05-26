import requests
import urllib
import urlparse
import ubersmith_client

from st2actions.runners.pythonrunner import Action

CONNECTION_ITEMS = ['url', 'api_user', 'api_token']
API_VERSION = "/api/2.0/"

class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__( config )
        
        if config is None:
            raise ValueError("No connection configuration details found")
        
        if "instance" in config:
            if config['instance'] is None:
                raise ValueError("'instance' config defined but empty.")
            else:
                pass
        else:
            raise KeyError("Config.yaml Missing Ubersmith Configuration" )
        
        self.api = None
         
    def establish_connection( self, ubersmith ):
        if ( self._connect( ubersmith ) ):
            return True
        
    def _connect(self, ubersmith):
        if self.check_connection():
            return True
        
        if ubersmith:
            connection = self.config['instance'].get(ubersmith)
        
            for item in CONNECTION_ITEMS:
                if item in connection:
                    pass
                else:
                    raise KeyError("Config.yaml Missing: instance:%s:%s"
                                   % (ubersmith, item))
        else:
            connection = self.config

        self.api = ubersmith_client.api.init( url = connection['url'] + API_VERSION, user = connection['api_user'], password = connection['api_token'] )
        
        return True

    def check_connection(self):
        ## If we're already connected
        if self.api is not None:
            return True
        
        return False
        
########################################################################################################

    def request(self, command, params):
        if not self.check_connection():
            return False

        methods = command.split('.')       

        if len( methods ) is not 2:
            raise ValueError("Incorrect API command : " + command)
        
        module = getattr( self.api, methods[0] )

        if params is None:
            return getattr( module , methods[1] )( )
        else:
            return getattr( module , methods[1] )( **params )
        