

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law. or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick#rickkauffman.com"

from lib.actions import MongoBaseAction
import json

__all__ = [
    'GetDb'
]


class GetDb(MongoBaseAction):
    def run(self):

        mydb = self.dbclient["app_db"]
        known = mydb["morpheuslogs"]

        list_to_process = []
        log = {}

        myquery = {"u_process": 'no'}
        records = list(known.find(myquery))

        for r in records:
            log['u_typeCode'] = r['u_typeCode']
            log['u_ts'] = r['u_ts']
            log['u_level'] = r['u_level']
            log['u_sourceType'] = r['u_sourceType']
            log['u_message'] = r['u_message']
            log['u_hostname'] = r['u_hostname']
            log['u_title'] = r['u_title']
            log['u_logSignature'] = r['u_logSignature']
            log['u_objectId'] = r['u_objectId']
            log['u_seq'] = r['u_seq']
            log['u_id'] = r['u_id']
            log['u_signatureVerified'] = r['u_signatureVerified']
            log = json.dumps(log)
            list_to_process.append(log)
            log = {}

        return (list_to_process)
