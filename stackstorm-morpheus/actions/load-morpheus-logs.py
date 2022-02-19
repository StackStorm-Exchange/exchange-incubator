

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

__all__ = [
    'LoadDb'
]


class LoadDb(MongoBaseAction):
    def run(self, logs):

        mydb = self.dbclient["app_db"]
        known = mydb["morpheuslogs"]

        new_log = {}

        for log in logs:
            myquery = {"u_id": logs[10]}
            records = known.find(myquery).count()
            if records == 0:
                new_log['u_typeCode'] = log[0]
                new_log['u_ts'] = log[1]
                new_log['u_level'] = log[2]
                new_log['u_sourceType'] = log[3]
                new_log['u_message'] = log[4]
                new_log['u_hostname'] = log[5]
                new_log['u_title'] = log[6]
                new_log['u_logSignature'] = log[7]
                new_log['u_objectId'] = log[8]
                new_log['u_seq'] = log[9]
                new_log['u_id'] = log[10]
                new_log['u_signatureVerified'] = log[11]
                new_log['u_process'] = 'no'
                write_record = known.insert_one(new_log)
                print(write_record)
                new_log = {}

            else:
                records = 'Fail to write mongo record, possible duplicate'
                # write_record = process.insert_one(alarm)
        return (records)
