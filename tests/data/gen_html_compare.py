import html

from nested_diff.formatters import HtmlFormatter, TextFormatter

import tests.data.formatters


def main():
    print('<!DOCTYPE html><html><head><style type="text/css">')
    print(HtmlFormatter().get_css())
    print('pre {margin: 0}')
    print('</style></head><body><table border=1 cellspacing=0>')

    for name, test in sorted(tests.data.formatters.get_tests().items()):
        if 'raises' in test:
            continue

        diff = test['diff']
        fmt_obj_opts = test.get('formatter_opts', {})
        fmt_func_opts = test.get('format_func_opts', {})

        try:
            txt = TextFormatter(**fmt_obj_opts).format(diff, **fmt_func_opts)
            htm = HtmlFormatter(**fmt_obj_opts).format(diff, **fmt_func_opts)
        except ValueError as e:
            if str(e).startswith('unsupported extension: '):
                continue
            raise

        print('<tr><td colspan=2>' + name + '</td></tr>')
        print('<tr><td><pre>')
        print(html.escape(txt), end='')
        print('</pre></td><td>')
        print(htm)
        print('</td></tr>')

    print('</table></body></html>')


if __name__ == '__main__':
    main()
