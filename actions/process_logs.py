

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
# __email__ = "rick@rickkauffman.com"

from lib.actions import MongoBaseAction

__all__ = [
    'LoadDb'
]


class LoadDb(MongoBaseAction):
    def run(self, logs):

        mydb = self.dbclient["app_db"]
        col = mydb["morpheus-logs"]

        for log in logs:
            col.updateOne({"_id": log['_id']}, {"$set": {"u_process": "yes"}})

        return ()
