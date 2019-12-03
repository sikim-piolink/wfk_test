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
module: pio_sig_up
short_description: Configuring Signature Management
description:
   - You can manage Signature Management of the WEBFRONT-K.
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
       - Enter the application names to apply configurations of the signatures. "Application" means the applications provided by the WEBFRONT-K.
If the "app_name" is ALL, the configurations will be applied to all applications.
     required: True
     type: str
   sig_list:
description:
       - Enter the lists of the signatures.
     required: True
     type: list
     suboptions:
       sig_id:
         description:
           - Enter the signature ID to modify the state.
         required: True
         type: str
       sig_status:
         description:
           - "Enter one of the following numbers to configure the state of the signature.
           - 1: Detection
           - 2: Block
           - 3: Exception"
         choices: ["1", "2", "3"]
         type: str
author: Seonil Kim(@sikim-piolink)
'''

EXAMPLES = r'''
---
- name: Signature Management - Access Control
  hosts: localhost
  collections:
      - sikim_piolink.wfktest
  tasks:
      - name: Set Signature
        pio_sig_up:
            host: "{{ host }}"
            port: "{{ port }}"
            username: "{{ username }}"
            password: "{{ password }}"
            app_name: ALL
            sig_list:
                - sig_id: "110100001"
                  sig_status: "2"
                - sig_id: "110100002"
                  sig_status: "2"
...
'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
#from ansible_collections.sikim_piolink.wfktest.plugins.module_utils.prest_utils import PrestUtils
from ansible.module_utils.prest_utils import PrestUtils
#from ansible_collections.sikim_piolink.wfktest.plugins.module_utils.prest_module import CMD_SITE_TYPE
from ansible.module_utils.prest_module import CMD_SITE_TYPE

sig_class_dict = {
    '1101': 'sig_req_appac',
    '1105': 'sig_req_buffer',
    '1106': 'sig_req_sql',
    '1107': 'sig_req_xss',
    '1111': 'sig_req_upload',
    '1112': 'sig_req_download',
    '1114': 'sig_req_include',
    '1115': 'sig_req_tool',
    '1116': 'sig_req_uploadfile',
    '1117': 'sig_req_sqllogin',
    '1118': 'sig_req_filter',
    '1201': 'sig_req_url',
}

sig_entry = dict(
    sig_id=dict(type='str', required=True),
    sig_status=dict(type='str', required=True, choices=["1", "2", "3"]),
)

module_args = dict(
    host=dict(type='str', required=True),
    port=dict(type='str', required=True),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    app_name=dict(type='str', required=True),
    sig_list=dict(type='list', required=True,
                  elements='dict', options=sig_entry),
)


class PioSigUp(PrestUtils):
    def __init__(self, module):
        super(PioSigUp, self).__init__(module)

    def set_sig(self, app_id):
        # sig_dict = {sig_class: [{sig_id, sig_status}, {..., ...}], ...}
        sig_dict = dict()

        sig_list = self.module.params['sig_list']
        for idx in range(0, len(sig_list)):
            sig_entry = sig_list[idx]

            # sig_id 앞의 4자리
            sig_class = sig_entry['sig_id'][:4]
            if sig_class not in sig_class_dict.keys():
                self.module.fail_json(msg="Invalid \"sig_id\": %s"
                                      % sig_entry['sig_id'])

            if sig_class not in sig_dict.keys():
                sig_class_list = list()
                sig_dict.update({sig_class: sig_class_list})

            sig_class_entry = {'sig_id': sig_entry['sig_id'],
                               'sig_status': sig_entry['sig_status'],
                               'app_id': app_id}
            sig_dict[sig_class].append(sig_class_entry)

        return sig_dict

    def set_sig_status(self, sig_dict, app_id):
        for k, v in sig_dict.items():
            if app_id == '0':
                url = self.set_url(CMD_SITE_TYPE, 'paf_sig_base',
                                   sig_class_dict[k], None, None)
            else:
                url = self.set_url(CMD_SITE_TYPE, 'paf_sig_settle',
                                   sig_class_dict[k], None, None)
            body = {'sig_entry': sig_dict[k]}
            self.resp = self.put(url, body)

    def run(self):
        if self.module.check_mode:
            return self.result

        app_id = self.get_app_id()
        sig_dict = self.set_sig(app_id)
        self.set_sig_status(sig_dict, app_id)


def main():
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    sig = PioSigUp(module)
    sig.init_args()
    sig.run()
    sig.set_result()


if __name__ == '__main__':
    main()
