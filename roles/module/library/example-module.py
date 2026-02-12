#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule


def main():
    module_args = dict(
        message=dict(type='str', required=False, default='hello from module')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    msg = module.params['message']

    result = {
        'changed': False,
        'message': msg,
    }

    # если хотим показать, что что‑то «изменили»
    if msg != 'hello from module':
        result['changed'] = True

    module.exit_json(**result)


if __name__ == '__main__':
    main()
