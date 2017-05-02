import paramiko
import time
import io
import logging

class SSH(object):

    def __init__(self,**kwargs):
        self._host = kwargs.pop('host')
        self._method = kwargs.pop('method', 'telnet')
        self._auth = kwargs.pop('auth', (None, None))
        self._enable = kwargs.pop('enable', None)
        self._port = kwargs.pop('port',22)
        self._client=None
        self._args={}
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._logger = logging.getLogger(__name__)
        try:
            self._client.connect(self._host, username=self._auth[0], password=self._auth[1], look_for_keys=False, allow_agent=False,port=self._port)
            self._client_conn = self._client.invoke_shell()
            self._logger.info("Connection established to the host:%r"%self._host)
            time.sleep(0.5)
            self.output = self.recv()

            while True:
                if "Network OS is not ready" in self.output:
                    self._logger.info ("SSH:Waiting till Network OS is ready")
                    time.sleep(30)
                    self._client_conn.send("\n")
                    self.output = self.recv()
                else:
                    break

            # Check for error
            if "incorrect" in self.output:
                raise Exception('Incorrect authentication details')

            # We should be in enable at this point
            if "#" in self.output:
                self._client_conn.send("\n")
                self.output = self.recv()
                self._hostname = self.output.translate(None, '\r\n')
                self._client_conn.send("terminal length 0\r\n")
                self.output = self.recv()
            else:
                self._client_conn.send("\n")
                self.output = self.recv()
                self._hostname = self.output.translate(None, '\r\n')
                self._client_conn.send("terminal length 0\r\n")
                self.output = self.recv()


        except Exception, err:

            self._logger.error('ERROR for host %s - %s\n:' % (self._host, err))
            return

    def send(self,command,expcted_str='#'):
        '''
        Executes the command on the switch
        :param command: Command to be executed on the device.
               expected_str: Expected string till which terminal will be read
        :return: CLI output after command execution.
        '''
        self._output = ''

        if self.connected:
            self._client_conn.send("\r\n")

            self.recv('#')
            self._client_conn.send("%s\r\n" % command)

            self._temp_line = self.recv(expcted_str)
            self._response = self._temp_line
            self._temp_data = io.BytesIO(self._response)
            self._output = self._temp_data.readlines()
        else:
            self._logger.info("Channel is not open")
        return self._output

    @property
    def connected(self):
        if self._client.get_transport().is_active() and \
                        self._client.get_transport() is not None:

            return True
        else:
            return False


    def recv(self,*args):
        '''
        Reads the remote device terminal till expected string occurs
        :param args: Expected string
        :return: CLI terminal output
        '''
        _output = ""
        _block = True
        _count = 1

        while _block:
            if not args:
                _block = False

            if _count >= 2:
                _block = False


            while not self._client_conn.recv_ready():
                time.sleep(0.1)
            while self._client_conn.recv_ready():
                time.sleep(0.3)
                _output += self._client_conn.recv(1000000)
                _count += 1
            if args:
                for _arg in args:
                    if _arg or "[y/n]" or "y" in _output:
                        _block = False
        return _output

    def read(self,command):
        '''
        Executes the global mode commands(ex:show) on the device
        :param command: Command to be excuted
        :return: CLI response of the command on execution.
        '''
        _returnlist = []
        self._client_conn.send(command + "\n")
        time.sleep(3)
        self.output = self.recv(self._hostname)
        stream = io.BytesIO(self.output)
        self.count = 0

        while self.count < 1:
            stream.readline()
            self.count += 1

        _lines = stream.readlines()
        for line in _lines:
            if line != '\r\n' and line != self._hostname:
                line = line.translate(None, '\r\n')
                if line != command:
                    _returnlist.append(line)
        return _returnlist

    @property
    def hostname(self):
        return self._hostname


