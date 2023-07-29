#!/usr/bin/env python3

import html

from nested_diff.formatters import HtmlFormatter, TextFormatter

import tests.data.formatters


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
        except Exception as e:
            txt = '<div class="error">ERROR: ' + str(e) + '</div>'
        else:
            txt = '<pre>' + html.escape(txt) + '</pre>'

        try:
            htm = HtmlFormatter(**fmt_obj_opts).format(diff)
        except Exception as e:
            htm = '<div class="error">ERROR: ' + str(e) + '</div>'

        print('<tr><td colspan=2 class="label">' + name + '</td></tr>')
        print('<tr><td>' + txt + '</td>')
        print('<td>' + htm + '</td></tr>')

    print('</table></center></body></html>')


if __name__ == '__main__':
    main()
