"""Autogenerated, do not edit manually!"""
import sys

RESULTS = {
    '0_vs_0': {
        'result': '  0\x1b[0m\n',
    },
    '0_vs_0_noU': {
        'result': '',
    },
    '0_vs_1': {
        'result': '\x1b[31m- 0\x1b[0m\n\x1b[32m+ 1\x1b[0m\n',
    },
    '0_vs_empty_string': {
        'result': "\x1b[31m- 0\x1b[0m\n\x1b[32m+ ''\x1b[0m\n",
    },
    '0_vs_undef': {
        'result': '\x1b[31m- 0\x1b[0m\n\x1b[32m+ None\x1b[0m\n',
    },
    '1.0_vs_1.0_as_string': {
        'result': "\x1b[31m- 1\x1b[0m\n\x1b[32m+ '1.0'\x1b[0m\n",
    },
    '1_vs_-1': {
        'result': '\x1b[31m- 1\x1b[0m\n\x1b[32m+ -1\x1b[0m\n',
    },
    '1_vs_1.0': {
        'result': '  1\x1b[0m\n',
    },
    '1_vs_1_as_string': {
        'result': "\x1b[31m- 1\x1b[0m\n\x1b[32m+ '1'\x1b[0m\n",
    },
    'a_vs_a': {
        'result': "  'a'\x1b[0m\n",
    },
    'a_vs_b': {
        'result': "\x1b[31m- 'a'\x1b[0m\n\x1b[32m+ 'b'\x1b[0m\n",
    },
    'brackets': {
        'result': "  {'('}\x1b[0m\n\x1b[31m-   ')'\x1b[0m\n\x1b[32m+   '('\x1b[0m\n  {'<'}\x1b[0m\n\x1b[31m-   '>'\x1b[0m\n\x1b[32m+   '<'\x1b[0m\n  {'['}\x1b[0m\n\x1b[31m-   ']'\x1b[0m\n\x1b[32m+   '['\x1b[0m\n  {'{'}\x1b[0m\n\x1b[31m-   '}'\x1b[0m\n\x1b[32m+   '{'\x1b[0m\n",
    },
    'comment_is_empty_string': {
        'result': "\x1b[31m- 'old'\x1b[0m\n\x1b[32m+ 'new'\x1b[0m\n",
    },
    'comment_is_multiline_string': {
        'result': "\x1b[34m# multi\x1b[0m\n\x1b[34m# line\x1b[0m\n\x1b[34m# comment\x1b[0m\n\x1b[31m- 'old'\x1b[0m\n\x1b[32m+ 'new'\x1b[0m\n",
    },
    'comment_vs_type_hint': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,2 +1,2 @@\x1b[0m\n\x1b[31m- two\x1b[0m\n\x1b[32m+ 2\x1b[0m\n  lines\x1b[0m\n',
    },
    'comment_with_HTML_tags': {
        'result': "\x1b[34m# <h1>comment</h1>\x1b[0m\n  'same'\x1b[0m\n",
    },
    'comments': {
        'result': "\x1b[34m# C-D\x1b[0m\n  {'k'}\x1b[0m\n\x1b[34m#   C-NO\x1b[0m\n\x1b[31m-   'v'\x1b[0m\n\x1b[32m+   'V'\x1b[0m\n",
    },
    'deeply_nested_hash_vs_empty_hash': {
        'result': "\x1b[1;31m- {'one'}\x1b[0m\n\x1b[31m-   {'two': {'three': 3}}\x1b[0m\n",
    },
    'deeply_nested_hash_vs_empty_hash_trimR': {
        'result': "\x1b[1;31m- {'one'}\x1b[0m\n\x1b[31m-   None\x1b[0m\n",
    },
    'deeply_nested_list_vs_empty_list': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   [[0, 1]]\x1b[0m\n',
    },
    'deeply_nested_list_vs_empty_list_trimR': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   None\x1b[0m\n',
    },
    'deeply_nested_subhash_removed_from_hash': {
        'result': "  {'four'}\x1b[0m\n    4\x1b[0m\n\x1b[1;31m- {'one'}\x1b[0m\n\x1b[31m-   {'two': {'three': 3}}\x1b[0m\n",
    },
    'deeply_nested_subhash_removed_from_hash_trimR': {
        'result': "  {'four'}\x1b[0m\n    4\x1b[0m\n\x1b[1;31m- {'one'}\x1b[0m\n\x1b[31m-   None\x1b[0m\n",
    },
    'deeply_nested_sublist_removed_from_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   [[0, 1]]\x1b[0m\n',
    },
    'deeply_nested_sublist_removed_from_list_trimR': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   None\x1b[0m\n',
    },
    'empty_hash_vs_empty_hash': {
        'result': '  {}\x1b[0m\n',
    },
    'empty_hash_vs_empty_hash_noU': {
        'result': '',
    },
    'empty_hash_vs_empty_list': {
        'result': '\x1b[31m- {}\x1b[0m\n\x1b[32m+ []\x1b[0m\n',
    },
    'empty_hash_vs_hash_with_one_key': {
        'result': "\x1b[1;32m+ {'one'}\x1b[0m\n\x1b[32m+   1\x1b[0m\n",
    },
    'empty_hash_vs_hash_with_one_key_noA': {
        'result': '',
    },
    'empty_list_vs_deeply_nested_list': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   [[0, 1]]\x1b[0m\n',
    },
    'empty_list_vs_empty_hash': {
        'result': '\x1b[31m- []\x1b[0m\n\x1b[32m+ {}\x1b[0m\n',
    },
    'empty_list_vs_empty_list': {
        'result': '  []\x1b[0m\n',
    },
    'empty_list_vs_empty_list_noU': {
        'result': '',
    },
    'empty_list_vs_list_with_one_item': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   0\x1b[0m\n',
    },
    'empty_list_vs_list_with_one_item_noA': {
        'result': '',
    },
    'empty_string_vs_0': {
        'result': "\x1b[31m- ''\x1b[0m\n\x1b[32m+ 0\x1b[0m\n",
    },
    'empty_string_vs_text': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1 +1,2 @@\x1b[0m\n\x1b[31m- \x1b[0m\n\x1b[32m+ A\x1b[0m\n\x1b[32m+ B\x1b[0m\n',
    },
    'empty_string_vs_undef': {
        'result': "\x1b[31m- ''\x1b[0m\n\x1b[32m+ None\x1b[0m\n",
    },
    'escaped_symbols': {
        'result': "  {'\\n'}\x1b[0m\n\x1b[31m-   '\\r\\n'\x1b[0m\n\x1b[32m+   '\\n'\x1b[0m\n",
    },
    'frozenset_extended': {
        'result': '\x1b[34m# <frozenset>\x1b[0m\n  1\x1b[0m\n\x1b[32m+ 2\x1b[0m\n',
    },
    'frozensets_lcs': {
        'result': '\x1b[34m# <frozenset>\x1b[0m\n\x1b[31m- 1\x1b[0m\n  2\x1b[0m\n\x1b[32m+ 3\x1b[0m\n',
    },
    'hash_with_one_key_vs_empty_hash': {
        'result': "\x1b[1;31m- {'one'}\x1b[0m\n\x1b[31m-   1\x1b[0m\n",
    },
    'hash_with_one_key_vs_empty_hash_noR': {
        'result': '',
    },
    'hashes_with_different_value_onlyU': {
        'result': "  {'one'}\x1b[0m\n    1\x1b[0m\n",
    },
    'hashes_with_one_different_value_noN': {
        'result': "  {'one'}\x1b[0m\n\x1b[31m-   1\x1b[0m\n",
    },
    'hashes_with_one_different_value_noO': {
        'result': "  {'one'}\x1b[0m\n\x1b[32m+   2\x1b[0m\n",
    },
    'inf_vs_inf': {
        'result': '  inf\x1b[0m\n',
    },
    'line_added_to_empty_string': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1 +1,2 @@\x1b[0m\n  \x1b[0m\n\x1b[32m+ \x1b[0m\n',
    },
    'list_with_one_item_vs_empty_list': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n',
    },
    'list_with_one_item_vs_empty_list_noR': {
        'result': '',
    },
    'lists_LCS_added_items': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   0\x1b[0m\n\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n  [3]\x1b[0m\n    3\x1b[0m\n\x1b[1;32m+ [4]\x1b[0m\n\x1b[32m+   4\x1b[0m\n  [5]\x1b[0m\n    5\x1b[0m\n\x1b[1;32m+ [6]\x1b[0m\n\x1b[32m+   6\x1b[0m\n\x1b[1;32m+ [7]\x1b[0m\n\x1b[32m+   7\x1b[0m\n',
    },
    'lists_LCS_added_items_noU': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   0\x1b[0m\n\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n\x1b[1;32m+ [2]\x1b[0m\n\x1b[32m+   4\x1b[0m\n\x1b[1;32m+ [3]\x1b[0m\n\x1b[32m+   6\x1b[0m\n\x1b[1;32m+ [4]\x1b[0m\n\x1b[32m+   7\x1b[0m\n',
    },
    'lists_LCS_changed_items': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n    1\x1b[0m\n  [2]\x1b[0m\n\x1b[31m-   2\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [3]\x1b[0m\n\x1b[31m-   3\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [4]\x1b[0m\n    4\x1b[0m\n  [5]\x1b[0m\n\x1b[31m-   5\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [6]\x1b[0m\n    6\x1b[0m\n  [7]\x1b[0m\n    7\x1b[0m\n',
    },
    'lists_LCS_changed_items_noOU': {
        'result': '  [2]\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [3]\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [5]\x1b[0m\n\x1b[32m+   9\x1b[0m\n',
    },
    'lists_LCS_changed_items_noU': {
        'result': '  [2]\x1b[0m\n\x1b[31m-   2\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [3]\x1b[0m\n\x1b[31m-   3\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [5]\x1b[0m\n\x1b[31m-   5\x1b[0m\n\x1b[32m+   9\x1b[0m\n',
    },
    'lists_LCS_complex': {
        'result': "\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   'a'\x1b[0m\n  [1]\x1b[0m\n    'b'\x1b[0m\n  [2]\x1b[0m\n    'c'\x1b[0m\n\x1b[1;32m+ [3]\x1b[0m\n\x1b[32m+   'd'\x1b[0m\n  [4]\x1b[0m\n    'e'\x1b[0m\n  [5]\x1b[0m\n\x1b[31m-   'h'\x1b[0m\n\x1b[32m+   'f'\x1b[0m\n  [6]\x1b[0m\n    'j'\x1b[0m\n\x1b[1;32m+ [7]\x1b[0m\n\x1b[32m+   'k'\x1b[0m\n  [8]\x1b[0m\n    'l'\x1b[0m\n  [9]\x1b[0m\n    'm'\x1b[0m\n  [10]\x1b[0m\n\x1b[31m-   'n'\x1b[0m\n\x1b[32m+   'r'\x1b[0m\n  [11]\x1b[0m\n\x1b[31m-   'p'\x1b[0m\n\x1b[32m+   's'\x1b[0m\n\x1b[1;32m+ [12]\x1b[0m\n\x1b[32m+   't'\x1b[0m\n",
    },
    'lists_LCS_complex_noAU': {
        'result': "\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   'a'\x1b[0m\n  [4]\x1b[0m\n\x1b[31m-   'h'\x1b[0m\n\x1b[32m+   'f'\x1b[0m\n  [8]\x1b[0m\n\x1b[31m-   'n'\x1b[0m\n\x1b[32m+   'r'\x1b[0m\n  [9]\x1b[0m\n\x1b[31m-   'p'\x1b[0m\n\x1b[32m+   's'\x1b[0m\n",
    },
    'lists_LCS_complex_noRU': {
        'result': "\x1b[1;32m+ [3]\x1b[0m\n\x1b[32m+   'd'\x1b[0m\n  [4]\x1b[0m\n\x1b[31m-   'h'\x1b[0m\n\x1b[32m+   'f'\x1b[0m\n\x1b[1;32m+ [6]\x1b[0m\n\x1b[32m+   'k'\x1b[0m\n  [8]\x1b[0m\n\x1b[31m-   'n'\x1b[0m\n\x1b[32m+   'r'\x1b[0m\n  [9]\x1b[0m\n\x1b[31m-   'p'\x1b[0m\n\x1b[32m+   's'\x1b[0m\n\x1b[1;32m+ [10]\x1b[0m\n\x1b[32m+   't'\x1b[0m\n",
    },
    'lists_LCS_complex_noU': {
        'result': "\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   'a'\x1b[0m\n\x1b[1;32m+ [3]\x1b[0m\n\x1b[32m+   'd'\x1b[0m\n  [4]\x1b[0m\n\x1b[31m-   'h'\x1b[0m\n\x1b[32m+   'f'\x1b[0m\n\x1b[1;32m+ [6]\x1b[0m\n\x1b[32m+   'k'\x1b[0m\n  [8]\x1b[0m\n\x1b[31m-   'n'\x1b[0m\n\x1b[32m+   'r'\x1b[0m\n  [9]\x1b[0m\n\x1b[31m-   'p'\x1b[0m\n\x1b[32m+   's'\x1b[0m\n\x1b[1;32m+ [10]\x1b[0m\n\x1b[32m+   't'\x1b[0m\n",
    },
    'lists_LCS_complex_onlyU': {
        'result': "  [1]\x1b[0m\n    'b'\x1b[0m\n  [2]\x1b[0m\n    'c'\x1b[0m\n  [3]\x1b[0m\n    'e'\x1b[0m\n  [5]\x1b[0m\n    'j'\x1b[0m\n  [6]\x1b[0m\n    'l'\x1b[0m\n  [7]\x1b[0m\n    'm'\x1b[0m\n",
    },
    'lists_LCS_removed_items': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n  [3]\x1b[0m\n    3\x1b[0m\n\x1b[1;31m- [4]\x1b[0m\n\x1b[31m-   4\x1b[0m\n  [5]\x1b[0m\n    5\x1b[0m\n\x1b[1;31m- [6]\x1b[0m\n\x1b[31m-   6\x1b[0m\n\x1b[1;31m- [7]\x1b[0m\n\x1b[31m-   7\x1b[0m\n',
    },
    'lists_LCS_removed_items_noU': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n\x1b[1;31m- [4]\x1b[0m\n\x1b[31m-   4\x1b[0m\n\x1b[1;31m- [6]\x1b[0m\n\x1b[31m-   6\x1b[0m\n\x1b[1;31m- [7]\x1b[0m\n\x1b[31m-   7\x1b[0m\n',
    },
    'lists_with_one_different_item': {
        'result': '  [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n\x1b[32m+   1\x1b[0m\n',
    },
    'lists_with_one_different_item_noN': {
        'result': '  [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n',
    },
    'lists_with_one_different_item_noO': {
        'result': '  [0]\x1b[0m\n\x1b[32m+   1\x1b[0m\n',
    },
    'mixed_specific_structures': {
        'result': '  (0)\x1b[0m\n\x1b[31m-   ()\x1b[0m\n\x1b[32m+   frozenset()\x1b[0m\n  (1)\x1b[0m\n\x1b[34m#   <set>\x1b[0m\n\x1b[32m+   True\x1b[0m\n',
    },
    'nan_vs_0.0_nans_equal_opt_enabled': {
        'result': '\x1b[31m- nan\x1b[0m\n\x1b[32m+ 0.0\x1b[0m\n',
    },
    'nan_vs_None_nans_equal_opt_enabled': {
        'result': '\x1b[31m- nan\x1b[0m\n\x1b[32m+ None\x1b[0m\n',
    },
    'nan_vs_nan_nans_equal_opt_disabled': {
        'result': '\x1b[31m- nan\x1b[0m\n\x1b[32m+ nan\x1b[0m\n',
    },
    'nan_vs_nan_nans_equal_opt_enabled': {
        'result': '  nan\x1b[0m\n',
    },
    'nan_vs_nan_nans_equal_opt_enabled_noU': {
        'result': '',
    },
    'nested_hashes': {
        'result': "\x1b[1;32m+ {'four'}\x1b[0m\n\x1b[32m+   4\x1b[0m\n  {'one'}\x1b[0m\n    1\x1b[0m\n\x1b[1;31m- {'three'}\x1b[0m\n\x1b[31m-   3\x1b[0m\n  {'two'}\x1b[0m\n    {'nine'}\x1b[0m\n\x1b[31m-     9\x1b[0m\n\x1b[32m+     8\x1b[0m\n    {'ten'}\x1b[0m\n      10\x1b[0m\n",
    },
    'nested_hashes_noU': {
        'result': "\x1b[1;32m+ {'four'}\x1b[0m\n\x1b[32m+   4\x1b[0m\n\x1b[1;31m- {'three'}\x1b[0m\n\x1b[31m-   3\x1b[0m\n  {'two'}\x1b[0m\n    {'nine'}\x1b[0m\n\x1b[31m-     9\x1b[0m\n\x1b[32m+     8\x1b[0m\n",
    },
    'nested_hashes_with_one_different_value': {
        'result': "  {'one'}\x1b[0m\n    {'two'}\x1b[0m\n      {'three'}\x1b[0m\n\x1b[31m-       3\x1b[0m\n\x1b[32m+       4\x1b[0m\n",
    },
    'nested_hashes_with_one_equal_value': {
        'result': "  {'one': {'two': {'three': 3}}}\x1b[0m\n",
    },
    'nested_hashes_with_one_equal_value_noU': {
        'result': '',
    },
    'nested_lists': {
        'result': "  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n    [[100]]\x1b[0m\n  [2]\x1b[0m\n    [0]\x1b[0m\n      20\x1b[0m\n    [1]\x1b[0m\n\x1b[31m-     '30'\x1b[0m\n\x1b[32m+     '31'\x1b[0m\n  [3]\x1b[0m\n\x1b[31m-   4\x1b[0m\n\x1b[32m+   5\x1b[0m\n",
    },
    'nested_lists_noU': {
        'result': "  [2]\x1b[0m\n    [1]\x1b[0m\n\x1b[31m-     '30'\x1b[0m\n\x1b[32m+     '31'\x1b[0m\n  [3]\x1b[0m\n\x1b[31m-   4\x1b[0m\n\x1b[32m+   5\x1b[0m\n",
    },
    'nested_lists_with_one_different_item': {
        'result': '  [0]\x1b[0m\n    [0]\x1b[0m\n\x1b[31m-     0\x1b[0m\n\x1b[32m+     1\x1b[0m\n',
    },
    'nested_lists_with_one_equal_item': {
        'result': '  [[0]]\x1b[0m\n',
    },
    'nested_lists_with_one_equal_item_noU': {
        'result': '',
    },
    'nested_mixed_structures': {
        'result': "  {'one'}\x1b[0m\n    [0]\x1b[0m\n      {'two'}\x1b[0m\n        {'three'}\x1b[0m\n          [0]\x1b[0m\n            7\x1b[0m\n          [1]\x1b[0m\n\x1b[31m-           4\x1b[0m\n\x1b[32m+           3\x1b[0m\n    [1]\x1b[0m\n      8\x1b[0m\n",
    },
    'nested_mixed_structures_noOU': {
        'result': "  {'one'}\x1b[0m\n    [0]\x1b[0m\n      {'two'}\x1b[0m\n        {'three'}\x1b[0m\n          [1]\x1b[0m\n\x1b[32m+           3\x1b[0m\n",
    },
    'one_item_changed_in_the_middle_of_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_changed_in_the_middle_of_list_noN': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_changed_in_the_middle_of_list_noNO': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_changed_in_the_middle_of_list_noO': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n\x1b[32m+   9\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_changed_in_the_middle_of_list_noU': {
        'result': '  [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n\x1b[32m+   9\x1b[0m\n',
    },
    'one_item_inserted_in_the_middle_of_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_inserted_in_the_middle_of_list_noA': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [1]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_inserted_in_the_middle_of_list_noU': {
        'result': '\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n',
    },
    'one_item_popped_from_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n',
    },
    'one_item_popped_from_list_noU': {
        'result': '\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n',
    },
    'one_item_pushed_to_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n',
    },
    'one_item_pushed_to_list_noU': {
        'result': '\x1b[1;32m+ [1]\x1b[0m\n\x1b[32m+   1\x1b[0m\n',
    },
    'one_item_removed_from_the_middle_of_list': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_removed_from_the_middle_of_list_noR': {
        'result': '  [0]\x1b[0m\n    0\x1b[0m\n  [2]\x1b[0m\n    2\x1b[0m\n',
    },
    'one_item_removed_from_the_middle_of_list_noU': {
        'result': '\x1b[1;31m- [1]\x1b[0m\n\x1b[31m-   1\x1b[0m\n',
    },
    'one_item_shifted_from_list': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n  [1]\x1b[0m\n    1\x1b[0m\n',
    },
    'one_item_shifted_from_list_noU': {
        'result': '\x1b[1;31m- [0]\x1b[0m\n\x1b[31m-   0\x1b[0m\n',
    },
    'one_item_unshifted_to_list': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   0\x1b[0m\n  [1]\x1b[0m\n    1\x1b[0m\n',
    },
    'one_item_unshifted_to_list_noU': {
        'result': '\x1b[1;32m+ [0]\x1b[0m\n\x1b[32m+   0\x1b[0m\n',
    },
    'one_key_added_to_subhash': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;32m+   {'three'}\x1b[0m\n\x1b[32m+     3\x1b[0m\n    {'two'}\x1b[0m\n      2\x1b[0m\n",
    },
    'one_key_added_to_subhash_noU': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;32m+   {'three'}\x1b[0m\n\x1b[32m+     3\x1b[0m\n",
    },
    'one_key_removed_from_subhash': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;31m-   {'three'}\x1b[0m\n\x1b[31m-     3\x1b[0m\n    {'two'}\x1b[0m\n      2\x1b[0m\n",
    },
    'one_key_removed_from_subhash_noU': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;31m-   {'three'}\x1b[0m\n\x1b[31m-     3\x1b[0m\n",
    },
    'quote_symbols': {
        'result': '  {\'"double"\'}\x1b[0m\n\x1b[31m-   \'""\'\x1b[0m\n\x1b[32m+   \'"\'\x1b[0m\n  {"\'single\'"}\x1b[0m\n\x1b[31m-   "\'\'"\x1b[0m\n\x1b[32m+   "\'"\x1b[0m\n  {\'`backticks`\'}\x1b[0m\n\x1b[31m-   \'``\'\x1b[0m\n\x1b[32m+   \'`\'\x1b[0m\n',
    },
    'redefined_depth': {
        'result': '\x1b[31m-       0\x1b[0m\n\x1b[32m+       1\x1b[0m\n',
    },
    'set_extended': {
        'result': '\x1b[34m# <set>\x1b[0m\n  1\x1b[0m\n\x1b[32m+ 2\x1b[0m\n',
    },
    'sets_empty_diff': {
        'result': '',
    },
    'sets_lcs': {
        'result': '\x1b[34m# <set>\x1b[0m\n\x1b[31m- 1\x1b[0m\n  2\x1b[0m\n\x1b[32m+ 3\x1b[0m\n',
    },
    'sets_lcs_noAR': {
        'result': '\x1b[34m# <set>\x1b[0m\n  2\x1b[0m\n',
    },
    'sets_lcs_noU': {
        'result': '\x1b[34m# <set>\x1b[0m\n\x1b[31m- 1\x1b[0m\n\x1b[32m+ 3\x1b[0m\n',
    },
    'sets_lcs_trimR': {
        'result': '\x1b[34m# <set>\x1b[0m\n\x1b[31m- 1\x1b[0m\n  2\x1b[0m\n\x1b[32m+ 3\x1b[0m\n',
    },
    'simple_strings_in_text_mode': {
        'result': "\x1b[31m- 'bar'\x1b[0m\n\x1b[32m+ 'baz'\x1b[0m\n",
    },
    'str_vs_bytes': {
        'result': "\x1b[31m- 'a'\x1b[0m\n\x1b[32m+ b'a'\x1b[0m\n",
    },
    'subhash_emptied': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;31m-   {'two'}\x1b[0m\n\x1b[31m-     2\x1b[0m\n",
    },
    'subhash_emptied_noR': {
        'result': '',
    },
    'subhash_filled': {
        'result': "  {'one'}\x1b[0m\n\x1b[1;32m+   {'two'}\x1b[0m\n\x1b[32m+     2\x1b[0m\n",
    },
    'subhash_filled_noA': {
        'result': '',
    },
    'sublist_emptied': {
        'result': '  [0]\x1b[0m\n\x1b[1;31m-   [0]\x1b[0m\n\x1b[31m-     0\x1b[0m\n',
    },
    'sublist_emptied_noR': {
        'result': '',
    },
    'sublist_filled': {
        'result': '  [0]\x1b[0m\n\x1b[1;32m+   [0]\x1b[0m\n\x1b[32m+     0\x1b[0m\n',
    },
    'sublist_filled_noA': {
        'result': '',
    },
    'text_diff_disabled': {
        'result': "\x1b[31m- 'A\\nB'\x1b[0m\n\x1b[32m+ 'B\\nC'\x1b[0m\n",
    },
    'text_equal': {
        'result': '',
    },
    'text_lcs': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,3 +1,2 @@\x1b[0m\n  A\x1b[0m\n\x1b[31m- B\x1b[0m\n  C\x1b[0m\n',
    },
    'text_line_added': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,2 +1,3 @@\x1b[0m\n\x1b[32m+ A\x1b[0m\n  B\x1b[0m\n  C\x1b[0m\n',
    },
    'text_line_changed': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,3 +1,3 @@\x1b[0m\n  A\x1b[0m\n\x1b[31m- B\x1b[0m\n\x1b[32m+ b\x1b[0m\n  C\x1b[0m\n',
    },
    'text_line_changed_ctx_0': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -2 +2 @@\x1b[0m\n\x1b[31m- B\x1b[0m\n\x1b[32m+ b\x1b[0m\n',
    },
    'text_line_removed': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,3 +1,2 @@\x1b[0m\n  A\x1b[0m\n\x1b[31m- B\x1b[0m\n  C\x1b[0m\n',
    },
    'text_multiple_hunks': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1 +1 @@\x1b[0m\n\x1b[32m+ A\x1b[0m\n\x1b[35m  @@ -3 +4 @@\x1b[0m\n\x1b[31m- C\x1b[0m\n',
    },
    'text_trailing_newlines': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,3 +1,3 @@\x1b[0m\n  A\x1b[0m\n\x1b[31m- B\x1b[0m\n\x1b[32m+ b\x1b[0m\n  \x1b[0m\n',
    },
    'text_vs_empty_string': {
        'result': '\x1b[34m# <str>\x1b[0m\n\x1b[35m  @@ -1,2 +1 @@\x1b[0m\n\x1b[31m- A\x1b[0m\n\x1b[31m- B\x1b[0m\n\x1b[32m+ \x1b[0m\n',
    },
    'tuple_extended': {
        'result': '  (0)\x1b[0m\n    1\x1b[0m\n\x1b[1;32m+ (1)\x1b[0m\n\x1b[32m+   2\x1b[0m\n',
    },
    'tuples_lcs': {
        'result': '\x1b[1;32m+ (0)\x1b[0m\n\x1b[32m+   0\x1b[0m\n  (1)\x1b[0m\n    1\x1b[0m\n  (2)\x1b[0m\n    2\x1b[0m\n  (3)\x1b[0m\n\x1b[31m-   4\x1b[0m\n\x1b[32m+   3\x1b[0m\n\x1b[1;31m- (4)\x1b[0m\n\x1b[31m-   5\x1b[0m\n',
    },
    'tuples_lcs_noOU': {
        'result': '\x1b[1;32m+ (0)\x1b[0m\n\x1b[32m+   0\x1b[0m\n  (2)\x1b[0m\n\x1b[32m+   3\x1b[0m\n\x1b[1;31m- (3)\x1b[0m\n\x1b[31m-   5\x1b[0m\n',
    },
    'type_hints_disabled': {
        'result': '\x1b[35m  @@ -1,2 +1,2 @@\x1b[0m\n\x1b[31m- two\x1b[0m\n\x1b[32m+ 2\x1b[0m\n  lines\x1b[0m\n',
    },
    'undef_vs_0': {
        'result': '\x1b[31m- None\x1b[0m\n\x1b[32m+ 0\x1b[0m\n',
    },
    'undef_vs_empty_hash': {
        'result': '\x1b[31m- None\x1b[0m\n\x1b[32m+ {}\x1b[0m\n',
    },
    'undef_vs_empty_hash_noNO': {
        'result': '',
    },
    'undef_vs_empty_list': {
        'result': '\x1b[31m- None\x1b[0m\n\x1b[32m+ []\x1b[0m\n',
    },
    'undef_vs_empty_string': {
        'result': "\x1b[31m- None\x1b[0m\n\x1b[32m+ ''\x1b[0m\n",
    },
    'undef_vs_negative_number': {
        'result': '\x1b[31m- None\x1b[0m\n\x1b[32m+ -1\x1b[0m\n',
    },
    'undef_vs_undef': {
        'result': '  None\x1b[0m\n',
    },
    'unsupported_extension': {
        'raises': ValueError,
    },
}


if __name__ == '__main__':
    names = sys.argv[1:] if len(sys.argv) > 1 else sorted(RESULTS.keys())
    headers = len(names) > 1

    for name in names:
        if headers:
            print('========== ' + name + ' ==========')
        print(RESULTS[name].get('result', None), end='')
