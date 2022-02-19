

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick@rickkauffman.com"

import urllib3
from lib.actions import MorpheusBaseAction
from pypheus.logs import Logs
urllib3.disable_warnings()

__all__ = [
    'LogData'
]


class LogData(MorpheusBaseAction):
    def run(self):
        log_list = []
        logs = Logs(self.client[0], self.client[1], self.client[2])
        log_data = logs.get_all_logs()

        for i in log_data['data']:
            info = [
                    i['typeCode'],
                    i['ts'],
                    i['level'],
                    i['sourceType'],
                    i['message'],
                    i['hostname'],
                    i['title'],
                    i['logSignature'],
                    i['objectId'],
                    i['seq'],
                    i['_id'],
                    i['signatureVerified']
                    ]

            log_list.append(info)
            info = []
        return log_list
