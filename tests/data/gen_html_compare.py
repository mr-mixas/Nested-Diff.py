import html

from nested_diff.formatters import HtmlFormatter, TextFormatter

import tests.data.formatters


print('<!DOCTYPE html><html><head><style type="text/css">')
print(HtmlFormatter().get_css())
print('pre {margin: 0}')
print('</style></head><body><table border=1 cellspacing=0>')

for name, test in sorted(tests.data.formatters.get_tests().items()):
    fmt_obj_opts = test.get('formatter_opts', {})
    fmt_func_opts = test.get('format_func_opts', {})

    print('<tr><td colspan=2>' + name + '</td></tr>')
    print('<tr><td><pre>')
    print(html.escape(TextFormatter(**fmt_obj_opts).format(test['diff'], **fmt_func_opts)), end='')
    print('</pre></td><td>')
    print(HtmlFormatter(**fmt_obj_opts).format(test['diff'], **fmt_func_opts))
    print('</td></tr>')

print('</table></body></html>')
