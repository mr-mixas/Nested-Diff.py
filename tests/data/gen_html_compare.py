#!/usr/bin/env python3

import html

import tests.data.formatters
from nested_diff.formatters import HtmlFormatter, TextFormatter


def main():
    print('<!DOCTYPE html><html><head><style type="text/css">')
    print(HtmlFormatter().get_css())
    print('pre {margin: 0}')
    print('td.label {background-color: #ddd}')
    print('div.error {color: #f00; font-family:monospace}')
    print('</style></head><body><center><table border=1 cellspacing=0>')

    for name, test in sorted(tests.data.formatters.get_tests().items()):
        diff = test['diff']
        fmt_obj_opts = test.get('formatter_opts', {})

        try:
            txt = TextFormatter(**fmt_obj_opts).format(diff)
        except Exception as e:  # noqa: BLE001
            txt = f'<div class="error">ERROR: {e}</div>'
        else:
            txt = f'<pre>{html.escape(txt)}</pre>'

        try:
            htm = HtmlFormatter(**fmt_obj_opts).format(diff)
        except Exception as e:  # noqa: BLE001
            htm = f'<div class="error">ERROR: {e}</div>'

        print(f'<tr><td colspan=2 class="label">{name}</td></tr>')
        print(f'<tr><td>{txt}</td>')
        print(f'<td>{htm}</td></tr>')

    print('</table></center></body></html>')


if __name__ == '__main__':
    main()
