from ubersmithlib.actions import BaseAction

class ApiCommand(BaseAction):
    def run(self, ubersmith = None, command = None, params = None):
        self.establish_connection( ubersmith )
        if command is not None:
            return self.request( command, params )
        
        return
