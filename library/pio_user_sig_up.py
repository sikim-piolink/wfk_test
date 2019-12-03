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
module: pio_user_sig_up
short_description: Configuring User-defined Signature Management
description:
   - You can manage User-defined Signature Management of the WEBFRONT-K.
version_added: '2.10'
requirements:
   - requests
options:
   host:
     description:
       - Enter the IPv4 address of the WEBFRONT-K.
     required: True
   port:
     description:
       - Enter the port number of the WEBFRONT-K.
     required: True
   username:
     description:
       - Enter the User ID of the WEBFRONT-K. The ID must have permissions for the WEBFRONT-K.
     required: True
   password:
     description:
       - Enter the user's password.
     required: True
   app_name:
     description:
       - Enter the application names to apply configurations of the user-defined signatures. "Application" means the applications provided by the WEBFRONT-K. If the "app_name" is ALL, the configurations are applied to all applications.
     required: True
   sig_list:
     description:
       - Enter the lists of the user-defined signatures.
     required: True
     type: list
     suboptions:
       sig_content:
         description:
          - Enter the content of the user-defined signature.
         required: True
       sig_status:
         description:
          - Enter one of the following numbers to modify the state of the user-defined signature.
          - 1: Detection
          - 2: Block
          - 3: Exception
         required: True
         choices: ["1", "2", "3"]
       sig_type:
         description:
          - Enter one of the following numbers to modify the type of the user-defined signature.
          - 1: Regular Expression
          - 2: URL
          - 3: PCRE"
         required: True
         choices: ["0", "1", "2", "3"]
       sig_ko_desc:
         description:
          - Enther a description of the user-defined signature.
         required: True

author: Seonil Kim(@sikim-piolink)
'''

EXAMPLES = r'''
---
- name: User Define Signature Management - Access Control
  hosts: localhost
  collections:
      - sikim_piolink.wfktest
  tasks:
      - name: Set Signature
        pio_user_sig_up:
            host: "{{ host }}"
            port: "{{ port }}"
            username: "{{ username }}"
            password: "{{ password }}"
            app_name: ALL
            sig_class: sig_req_appac
            sig_list:
                - sig_content: /test1
                  sig_status: 1
                  sig_type: 0
                  sig_ko_desc: "ansible test1"
                - sig_content: /test2
                  sig_status: 2
                  sig_type: 0
                  sig_ko_desc: "ansible test2"
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

sig_class_list = [
    'sig_req_appac',
    'sig_req_buffer',
    'sig_req_sql',
    'sig_req_xss',
    'sig_req_upload',
    'sig_req_download',
    'sig_req_include',
    'sig_req_sqllogin',
    'sig_req_filter',
    'sig_req_url',
]

sig_entry = dict(
    sig_content=dict(type='str', required=True),
    sig_status=dict(type='str', required=True, choices=["1", "2", "3"]),
    sig_type=dict(type='str', required=True, choices=["0", "1", "2", "3"]),
    sig_ko_desc=dict(type='str', required=True),
)

module_args = dict(
    host=dict(type='str', required=True),
    port=dict(type='str', required=True),
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    app_name=dict(type='str', required=True),
    sig_class=dict(type='str', required=True, choices=sig_class_list),
    sig_list=dict(type='list', required=True,
                  elements='dict', options=sig_entry),
)


class PioUserSigUp(PrestUtils):
    def __init__(self, module):
        super(PioUserSigUp, self).__init__(module)
        self.post_body_list = list()
        self.put_body_list = list()

    def set_sig_body(self, app_id):
        get_url = self.set_url(CMD_SITE_TYPE, 'paf_sig_base',
                               self.module.params['sig_class'],
                               None, None)
        sig_list = self.module.params['sig_list']
        for idx in range(0, len(sig_list)):
            sig_entry = sig_list[idx]
            src_sig_entry = self.get_entry(get_url, 'sig_content',
                                           sig_entry['sig_content'],
                                           self.module.params['sig_class'],
                                           'sig_entry')
            if src_sig_entry is None:
                body_dict = {'sig_content': sig_entry['sig_content'],
                             'sig_status': sig_entry['sig_status'],
                             'sig_type': sig_entry['sig_type'],
                             'sig_ko_desc': sig_entry['sig_ko_desc']}
                self.post_body_list.append(body_dict)
            else:
                if app_id == '0':
                    if self.module.params['sig_class'] == 'sig_req_appac' or \
                            self.module.params['sig_class'] == \
                            'sig_req_include':
                        body_dict = {'sig_id': src_sig_entry['sig_id'],
                                     'sig_status': sig_entry['sig_status'],
                                     'sig_ko_desc': sig_entry['sig_ko_desc']}
                    else:
                        body_dict = {'sig_id': src_sig_entry['sig_id'],
                                     'sig_content': sig_entry['sig_content'],
                                     'sig_status': sig_entry['sig_status'],
                                     'sig_type': sig_entry['sig_type'],
                                     'sig_ko_desc': sig_entry['sig_ko_desc']}
                else:
                    body_dict = {'sig_id': src_sig_entry['sig_id'],
                                 'sig_status': sig_entry['sig_status'],
                                 'app_id': app_id}

                self.put_body_list.append(body_dict)

    def send_sig(self, app_id):
        if app_id == '0':
            url = self.set_url(CMD_SITE_TYPE, 'paf_sig_base',
                               self.module.params['sig_class'], None, None)
        else:
            url = self.set_url(CMD_SITE_TYPE, 'paf_sig_settle',
                               self.module.params['sig_class'], None, None)

        if len(self.post_body_list) is not 0:
            body = {'sig_entry': self.post_body_list}
            self.resp = self.post(url, body)
        if len(self.put_body_list) is not 0:
            body = {'sig_entry': self.put_body_list}
            self.resp = self.put(url, body)

    def run(self):
        if self.module.check_mode:
            return self.result

        app_id = self.get_app_id()
        self.set_sig_body(app_id)
        self.send_sig(app_id)


def main():
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    sig = PioUserSigUp(module)
    sig.init_args()
    sig.run()
    sig.set_result()


if __name__ == '__main__':
    main()
