## Piolink Webfront-K Ansible Collection
***

The Collection is the Piolink Webfront-k Ansible Automation project.

## installation

1. Install or upgrade to Ansible 2.9+
2. Download this collection from galaxy: ansible-galaxy collection install sikim_piolink.wfktest

## Requirements 
* Ansible 2.9+ is required to support the newer Ansible Collections format
* requests module

## Modules
The collection provides the following modules:

* `pio_app`   You can manage the WEBFRONT-K applications.
* `pio_req_appac`  You can manage Application Access Control of the WEBFRONT-K.
* `pio_req_buffer`  You can manage Blocking Buffer Overflow of the WEBFRONT-K.
* `pio_req_sql`  You can manage Blocking SQL Injection of the WEBFRONT-K.
* `pio_req_tool`  You can manage Blocking Web Attck Programs of the WEBFRONT-K.
* `pio_req_xss`  You can manage Blocking XSS (Cross-site scripting) of the WEBFRONT-K.
* `pio_sig_up`  You can manage Signature Management of the WEBFRONT-K.
* `pio_user_sig_up`  You can manage User-defined Signature Management of the WEBFRONT-K.

## Usage
The following example is used to configure an application in webfront-k.
Create pio_app.yml with the following template
```yaml
---
- name: Application Management
  hosts: localhost
  roles:
  - sikim_piolink.wfk_test
  tasks:
      - name: Set App Config
        pio_app:
            host: "{{ host }}"
            port: "{{ port }}"
            username: "{{ username }}"
            password: "{{ password }}"
            app_name: ansible_test
            app_ip_list:
                - app_ip: 1.1.1.1
                  app_port: 80
                - app_ip: 2.2.2.2
                  app_port: 80
            app_domain_list:
                - app_domain: 1.1.1.1
                - app_domain: 2.2.2.2
```

Run the test:
```bash
ansible-playbook pio_app.yml
```

