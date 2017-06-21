# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six
import os

from st2common.runners.base_action import Action
from st2client.client import Client
from st2common.content import utils as content_utils
from st2common.util import jinja as jinja_utils


class FormatResultAction(Action):
    def __init__(self, config=None, action_service=None):
        super(FormatResultAction, self).__init__(config=config, action_service=action_service)
        
        api_url = os.environ.get('ST2_ACTION_API_URL', None)
        token = os.environ.get('ST2_ACTION_AUTH_TOKEN', None)
        
        self.client = Client(api_url=api_url, token=token)
        
        self.jinja = jinja_utils.get_jinja_environment(allow_undefined=True)
        self.jinja.tests['in'] = lambda item, list: item in list

    def run(self, template_pack, template_path, context, include_execution, include_six):
        if include_six:
            context['six'] = six
            
        if include_execution:
            execution = self._get_execution(include_execution)
            context['__execution'] = execution
        
        pack_path = content_utils.get_pack_base_path(template_pack)
        abs_template_path = os.path.abspath(os.path.join(pack_path, template_path)) 
        
        if not abs_template_path.startswith(pack_path):
            raise ValueError('Template_path points to a file outside pack directory.')
        
        with open(abs_template_path, 'r') as f:
            template = f.read()

        return self.jinja.from_string(template).render(context)

    def _get_execution(self, execution_id):
        if not execution_id:
            raise ValueError('Invalid execution_id provided.')
        execution = self.client.liveactions.get_by_id(id=execution_id)
        if not execution:
            return None
        return execution.to_dict()
