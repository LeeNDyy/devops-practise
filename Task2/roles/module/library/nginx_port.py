#!/usr/bin/python

import os
import re
from ansible.module_utils.basic import AnsibleModule

def main():
    module_args = dict(
        port=dict(type='int', required=True),
        config_path=dict(type='str', default='/tmp/nginx-test/nginx.conf')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    port = module.params['port']
    config_path = module.params['config_path']

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    if not os.path.exists(config_path):
        module.fail_json(msg=f'Конфигурационный файл не найден: {config_path}', **result)

    try:
        with open(config_path, 'r') as f:
            content = f.read()
    except Exception as e:
        module.fail_json(msg=f'Не удалось прочитать файл {config_path}: {str(e)}', **result)

    pattern = re.compile(r'(listen\s+)[0-9]+;')
    
    # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
    # Используем синтаксис \g<1> для явного указания группы
    # и raw f-string (fr'...') для корректной обработки
    new_content = pattern.sub(fr'\g<1>{port};', content, count=1)
    # --- КОНЕЦ ИСПРАВЛЕНИЯ ---

    if content != new_content:
        result['changed'] = True
        result['message'] = f'Порт в файле {config_path} изменен на {port}.'

        if not module.check_mode:
            try:
                with open(config_path, 'w') as f:
                    f.write(new_content)
            except Exception as e:
                module.fail_json(msg=f'Не удалось записать в файл {config_path}: {str(e)}', **result)
    else:
        result['message'] = f'Порт в файле {config_path} уже установлен на {port}.'

    module.exit_json(**result)

if __name__ == '__main__':
    main()
