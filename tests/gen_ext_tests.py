#!/usr/bin/env python

from __future__ import unicode_literals

import json
import os
import sys


DIR_INPUT = sys.argv[1]
DIR_OUTPUT = sys.argv[2]


for file_name in os.listdir(DIR_INPUT):
    with open(os.path.join(DIR_INPUT, file_name)) as f:
        data = json.load(f)

    test_name = file_name.replace('.json', '')
    test_name = test_name.replace('.', 'dot')
    test_name = test_name.replace('-', 'minus')

    test_opts = {}
    if 'opts' in data:
        for o in data['opts']:
            if o.startswith('no'):
                test_opts[o.replace('no', '')] = False
            elif o == 'trimR':
                test_opts['trimR'] = True

    with open(os.path.join(DIR_OUTPUT, 'test_' + test_name + '.py'), 'w') as f:
        f.write('"""\n')
        f.write('Do not edit manually! Generated from\n')
        f.write('https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/' + file_name)
        f.write('\n"""\n\n')
        f.write('from __future__ import unicode_literals\n')
        f.write('import nested_diff\n\n\n')

        f.write('def test_' + test_name + '():\n')
        f.write('    a = ' + repr(data['a']) + '\n')
        f.write('    b = ' + repr(data['b']) + '\n')
        f.write('    diff = ' + repr(data['diff']) + '\n')
        f.write('    opts = ' + repr(test_opts) + '\n')
        f.write('    assert diff == nested_diff.diff(a, b, **opts)\n')
