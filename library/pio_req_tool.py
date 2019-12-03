#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright: (c) 2019, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: pio_req_tool
short_description: Configuring Blocking Web Attack Programs
description:
   - You can manage Blocking Web Attck Programs of the WEBFRONT-K.
version_added: '2.10'
requirements:
   - requests
options:
   host:
     description:
       - Enter the IPv4 address of the WEBFRONT-K.
     required: True
     type: str
   port:
     description:
       - Enter the port number of the WEBFRONT-K.
     required: True
     type: str
   username:
     description:
       - Enter the User ID of the WEBFRONT-K. The ID must have permissions for the WEBFRONT-K.
     required: True
     type: str
   password:
     description:
         - Enter the user's password.
            required: True
     type: str
   app_name:
     description:
       - Enter the application name. "Application" means the applications provided by the WEBFRONT-K.
     required: True
     type: str
   status:
     description:
       - Enter one of the following numbers to configure the state of Blocking Web Attack Programs.
       - 0: Disable
       - 1: Enable
     required: True
     default: 0
     choices: [0, 1]
     type: int
   block:
     description:
       - Enter one of the following numbers to allow or drop packets matching the Blocking Web Attack Programs policies.
       - 0: Allow
       - 1: Drop
     required: True
     default: 0
     choices: [0, 1]
     type: int
   log:
     description:
       - Enter one of the following numbers to collect log files or not for packets matching the Blocking Web Attack Programs policies.
       - 0: Disable
       - 1: Enable
     required: True
     default: 0
     choices: [0, 1]
     type: int
author: Seonil Kim(@sikim-piolink)
'''

EXAMPLES = r'''
---
- name: Request Inspection Web Attack Management
  hosts: localhost
  collections:
      - sikim_piolink.wfktest
  tasks:
      - name: Set Req tool Config
        pio_req_sql:
            host: "{{ host }}"
            port: "{{ port }}"
            username: "{{ username }}"
            password: "{{ password }}"
            app_name: ansible_test
            status: 1
            block: 0
            log: 0
...
'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
#from ansible_collections.sikim_piolink.wfktest.plugins.module_utils.prest_utils import PrestUtils
from ansible.module_utils.prest_utils import PrestUtils
#from ansible_collections.sikim_piolink.wfktest.plugins.module_utils.prest_module import CMD_APP_TYPE
from ansible.module_utils.prest_module import CMD_APP_TYPE

module_args = dict(
    host=dict(type='str', required=True),
    port=dict(type='str', required=True),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    app_name=dict(type='str', required=True),
    status=dict(type='int', required=True, choices=[0, 1]),
    block=dict(type='int', required=True, choices=[0, 1]),
    log=dict(type='int', required=True, choices=[0, 1]),
)


class PioReqTool(PrestUtils):
    def __init__(self, module):
        super(PioReqTool, self).__init__(module)

    def set_req_tool_status(self, app_id):
        url = self.set_url(CMD_APP_TYPE, 'req-tool', 'status', app_id, None)
        status = self.module.params['status']
        block = self.module.params['block']
        log = self.module.params['log']
        body = {'enable': status, 'block': block, 'log': log}
        self.resp = self.put(url, body)

    def run(self):
        if self.module.check_mode:
            return self.result

        app_id = self.get_app_id()
        self.set_req_tool_status(app_id)


def main():
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    req_tool = PioReqTool(module)
    req_tool.init_args()
    req_tool.run()
    req_tool.set_result()


if __name__ == '__main__':
    main()
