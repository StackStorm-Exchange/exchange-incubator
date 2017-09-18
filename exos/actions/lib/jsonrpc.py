import json
import requests

#
# This class contains the specifics of constructing a JSONRPC message and
# returning the results
class JsonRPC(object):

    def __init__(self, ipaddress, username=None, password=None, method='cli'):
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.transaction = 0
        self.cookie = None
        # construct a URL template for the EXOS JSONRPC POST message
        self.url = 'http://{ip}/jsonrpc'.format(ip=self.ipaddress)
        self.json_request = {'method' : method,
                            'id' : self.transaction,
                            'jsonrpc' : '2.0',
                            'params' : None
                            }

    def send(self, cmds):
        # This method:
        #   fills out the JSONRPC POST data structures
        #   Sends the POST via HTTP to the EXOS switch
        #   gets the POST response
        #   returns the decoded JSON in native python structures

        # http headers
        headers = {'Content-Type': 'application/json'}

        # after the first authentication, EXOS returns a cookie we can use
        # in JSONRCP transactions to avoid re-authenticating for every transaction
        #
        # if we have a cookie from previsous authentication, use it
        if self.cookie is not None:
            headers['Cookie'] = 'session={0}'.format(self.cookie)

        # increment the JSONRPC transaction counter
        self.transaction += 1
        self.json_request['id'] = self.transaction

        # JSONRPC defines params as a list
        # EXOS expects the CLI command to be a string in a single list entry
        self.json_request['params'] = [cmds]

        # send the JSONRPC message to the EXOS switch
        response = requests.post(self.url,
            headers=headers,
            auth=(self.username, self.password),
            data=json.dumps(self.json_request))

        # interpret the response from the EXOS switch
        # first check the HTTP error code to see if HTTP was successful
        # delivering the message
        if response.status_code == requests.codes.ok:
            # if we have a cookie, store it so we can use it later
            self.cookie = response.cookies.get('session')
            try:
                # ensure the response is JSON encoded
                jsonrpc_response = json.loads(response.text)
            except:
                raise ValueError("response not in JSON format")
        else:
            # raise http exception
            response.raise_for_status()

        rslt_list = jsonrpc_response.get('result')
        if rslt_list is None:
            raise ValueError("JSON result field is not present in response")

        #handle debug cfgmgr cli
        if isinstance(rslt_list, dict):
            debug_data = rslt_list.get('data')
            if debug_data is not None:
                return debug_data
        elif isinstance(rslt_list, list):
            for row in rslt_list:
                # check the EXOS command response for errors by scraping the CLI output
                cli_output = row.get('CLIoutput')
                if cli_output is None:
                    continue

                row_lines = cli_output.splitlines()
                for line in row_lines:
                    lower_case_line = line.lower()
                    if lower_case_line.startswith('run time error'):
                        raise RuntimeError(line)
                    if lower_case_line.startswith('error'):
                        raise RuntimeError(line)
        else:
            raise ValueError("Unexpected JSON result data format")

        # return the JSONRPC result to the caller
        return rslt_list
