#!/usr/bin/env python3

import html

from nested_diff.formatters import HtmlFormatter, TextFormatter

import tests.data.formatters


def main():
    print('<!DOCTYPE html><html><head><style type="text/css">')
    print(HtmlFormatter().get_css())
    print('pre {margin: 0}')
    print('</style></head><body><center><table border=1 cellspacing=0>')

    for name, test in sorted(tests.data.formatters.get_tests().items()):
        if 'raises' in test:
            continue

        diff = test['diff']
        fmt_obj_opts = test.get('formatter_opts', {})

        txt = TextFormatter(**fmt_obj_opts).format(diff)
        htm = HtmlFormatter(**fmt_obj_opts).format(diff)

        print('<tr><td colspan=2>' + name + '</td></tr>')
        print('<tr><td><pre>')
        print(html.escape(txt), end='')
        print('</pre></td><td>')
        print(htm)
        print('</td></tr>')

    print('</table></center></body></html>')


if __name__ == '__main__':
    main()
