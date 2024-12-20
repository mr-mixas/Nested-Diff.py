"""Autogenerated, do not edit manually!"""
import sys

RESULTS = {
    '0_vs_0': {
        'result': '  0\n',
    },
    '0_vs_0_noU': {
        'result': '',
    },
    '0_vs_1': {
        'result': '- 0\n+ 1\n',
    },
    '0_vs_empty_string': {
        'result': "- 0\n+ ''\n",
    },
    '0_vs_undef': {
        'result': '- 0\n+ None\n',
    },
    '1.0_vs_1.0_as_string': {
        'result': "- 1\n+ '1.0'\n",
    },
    '1_vs_-1': {
        'result': '- 1\n+ -1\n',
    },
    '1_vs_1.0': {
        'result': '  1\n',
    },
    '1_vs_1_as_string': {
        'result': "- 1\n+ '1'\n",
    },
    'a_vs_a': {
        'result': "  'a'\n",
    },
    'a_vs_b': {
        'result': "- 'a'\n+ 'b'\n",
    },
    'brackets': {
        'result': "  {'('}\n-   ')'\n+   '('\n  {'<'}\n-   '>'\n+   '<'\n  {'['}\n-   ']'\n+   '['\n  {'{'}\n-   '}'\n+   '{'\n",
    },
    'comment_is_empty_string': {
        'result': "- 'old'\n+ 'new'\n",
    },
    'comment_is_multiline_string': {
        'result': "# multi\n# line\n# comment\n- 'old'\n+ 'new'\n",
    },
    'comment_vs_type_hint': {
        'result': '# <str>\n  @@ -1,2 +1,2 @@\n- two\n+ 2\n  lines\n',
    },
    'comment_with_HTML_tags': {
        'result': "# <h1>comment</h1>\n  'same'\n",
    },
    'comments': {
        'result': "# C-D\n  {'k'}\n#   C-NO\n-   'v'\n+   'V'\n",
    },
    'deeply_nested_hash_vs_empty_hash': {
        'result': "- {'one'}\n-   {'two': {'three': 3}}\n",
    },
    'deeply_nested_hash_vs_empty_hash_trimR': {
        'result': "- {'one'}\n-   None\n",
    },
    'deeply_nested_list_vs_empty_list': {
        'result': '- [0]\n-   [[0, 1]]\n',
    },
    'deeply_nested_list_vs_empty_list_trimR': {
        'result': '- [0]\n-   None\n',
    },
    'deeply_nested_subhash_removed_from_hash': {
        'result': "  {'four'}\n    4\n- {'one'}\n-   {'two': {'three': 3}}\n",
    },
    'deeply_nested_subhash_removed_from_hash_trimR': {
        'result': "  {'four'}\n    4\n- {'one'}\n-   None\n",
    },
    'deeply_nested_sublist_removed_from_list': {
        'result': '  [0]\n    0\n- [1]\n-   [[0, 1]]\n',
    },
    'deeply_nested_sublist_removed_from_list_trimR': {
        'result': '  [0]\n    0\n- [1]\n-   None\n',
    },
    'empty_hash_vs_empty_hash': {
        'result': '  {}\n',
    },
    'empty_hash_vs_empty_hash_noU': {
        'result': '',
    },
    'empty_hash_vs_empty_list': {
        'result': '- {}\n+ []\n',
    },
    'empty_hash_vs_hash_with_one_key': {
        'result': "+ {'one'}\n+   1\n",
    },
    'empty_hash_vs_hash_with_one_key_noA': {
        'result': '',
    },
    'empty_list_vs_deeply_nested_list': {
        'result': '+ [0]\n+   [[0, 1]]\n',
    },
    'empty_list_vs_empty_hash': {
        'result': '- []\n+ {}\n',
    },
    'empty_list_vs_empty_list': {
        'result': '  []\n',
    },
    'empty_list_vs_empty_list_noU': {
        'result': '',
    },
    'empty_list_vs_list_with_one_item': {
        'result': '+ [0]\n+   0\n',
    },
    'empty_list_vs_list_with_one_item_noA': {
        'result': '',
    },
    'empty_string_vs_0': {
        'result': "- ''\n+ 0\n",
    },
    'empty_string_vs_text': {
        'result': '# <str>\n  @@ -1 +1,2 @@\n- \n+ A\n+ B\n',
    },
    'empty_string_vs_undef': {
        'result': "- ''\n+ None\n",
    },
    'escaped_symbols': {
        'result': "  {'\\n'}\n-   '\\r\\n'\n+   '\\n'\n",
    },
    'frozenset_extended': {
        'result': '# <frozenset>\n  1\n+ 2\n',
    },
    'frozensets_lcs': {
        'result': '# <frozenset>\n- 1\n  2\n+ 3\n',
    },
    'hash_with_one_key_vs_empty_hash': {
        'result': "- {'one'}\n-   1\n",
    },
    'hash_with_one_key_vs_empty_hash_noR': {
        'result': '',
    },
    'hashes_with_different_value_onlyU': {
        'result': "  {'one'}\n    1\n",
    },
    'hashes_with_one_different_value_noN': {
        'result': "  {'one'}\n-   1\n",
    },
    'hashes_with_one_different_value_noO': {
        'result': "  {'one'}\n+   2\n",
    },
    'inf_vs_inf': {
        'result': '  inf\n',
    },
    'line_added_to_empty_string': {
        'result': '# <str>\n  @@ -1 +1,2 @@\n  \n+ \n',
    },
    'list_with_one_item_vs_empty_list': {
        'result': '- [0]\n-   0\n',
    },
    'list_with_one_item_vs_empty_list_noR': {
        'result': '',
    },
    'lists_LCS_added_items': {
        'result': '+ [0]\n+   0\n+ [1]\n+   1\n  [2]\n    2\n  [3]\n    3\n+ [4]\n+   4\n  [5]\n    5\n+ [6]\n+   6\n+ [7]\n+   7\n',
    },
    'lists_LCS_added_items_noU': {
        'result': '+ [0]\n+   0\n+ [1]\n+   1\n+ [2]\n+   4\n+ [3]\n+   6\n+ [4]\n+   7\n',
    },
    'lists_LCS_changed_items': {
        'result': '  [0]\n    0\n  [1]\n    1\n  [2]\n-   2\n+   9\n  [3]\n-   3\n+   9\n  [4]\n    4\n  [5]\n-   5\n+   9\n  [6]\n    6\n  [7]\n    7\n',
    },
    'lists_LCS_changed_items_noOU': {
        'result': '  [2]\n+   9\n  [3]\n+   9\n  [5]\n+   9\n',
    },
    'lists_LCS_changed_items_noU': {
        'result': '  [2]\n-   2\n+   9\n  [3]\n-   3\n+   9\n  [5]\n-   5\n+   9\n',
    },
    'lists_LCS_complex': {
        'result': "- [0]\n-   'a'\n  [1]\n    'b'\n  [2]\n    'c'\n+ [3]\n+   'd'\n  [4]\n    'e'\n  [5]\n-   'h'\n+   'f'\n  [6]\n    'j'\n+ [7]\n+   'k'\n  [8]\n    'l'\n  [9]\n    'm'\n  [10]\n-   'n'\n+   'r'\n  [11]\n-   'p'\n+   's'\n+ [12]\n+   't'\n",
    },
    'lists_LCS_complex_noAU': {
        'result': "- [0]\n-   'a'\n  [4]\n-   'h'\n+   'f'\n  [8]\n-   'n'\n+   'r'\n  [9]\n-   'p'\n+   's'\n",
    },
    'lists_LCS_complex_noRU': {
        'result': "+ [3]\n+   'd'\n  [4]\n-   'h'\n+   'f'\n+ [6]\n+   'k'\n  [8]\n-   'n'\n+   'r'\n  [9]\n-   'p'\n+   's'\n+ [10]\n+   't'\n",
    },
    'lists_LCS_complex_noU': {
        'result': "- [0]\n-   'a'\n+ [3]\n+   'd'\n  [4]\n-   'h'\n+   'f'\n+ [6]\n+   'k'\n  [8]\n-   'n'\n+   'r'\n  [9]\n-   'p'\n+   's'\n+ [10]\n+   't'\n",
    },
    'lists_LCS_complex_onlyU': {
        'result': "  [1]\n    'b'\n  [2]\n    'c'\n  [3]\n    'e'\n  [5]\n    'j'\n  [6]\n    'l'\n  [7]\n    'm'\n",
    },
    'lists_LCS_removed_items': {
        'result': '- [0]\n-   0\n- [1]\n-   1\n  [2]\n    2\n  [3]\n    3\n- [4]\n-   4\n  [5]\n    5\n- [6]\n-   6\n- [7]\n-   7\n',
    },
    'lists_LCS_removed_items_noU': {
        'result': '- [0]\n-   0\n- [1]\n-   1\n- [4]\n-   4\n- [6]\n-   6\n- [7]\n-   7\n',
    },
    'lists_with_one_different_item': {
        'result': '  [0]\n-   0\n+   1\n',
    },
    'lists_with_one_different_item_noN': {
        'result': '  [0]\n-   0\n',
    },
    'lists_with_one_different_item_noO': {
        'result': '  [0]\n+   1\n',
    },
    'mixed_specific_structures': {
        'result': '  (0)\n-   ()\n+   frozenset()\n  (1)\n#   <set>\n+   True\n',
    },
    'nan_vs_0.0_nans_equal_opt_enabled': {
        'result': '- nan\n+ 0.0\n',
    },
    'nan_vs_None_nans_equal_opt_enabled': {
        'result': '- nan\n+ None\n',
    },
    'nan_vs_nan_nans_equal_opt_disabled': {
        'result': '- nan\n+ nan\n',
    },
    'nan_vs_nan_nans_equal_opt_enabled': {
        'result': '  nan\n',
    },
    'nan_vs_nan_nans_equal_opt_enabled_noU': {
        'result': '',
    },
    'nested_hashes': {
        'result': "+ {'four'}\n+   4\n  {'one'}\n    1\n- {'three'}\n-   3\n  {'two'}\n    {'nine'}\n-     9\n+     8\n    {'ten'}\n      10\n",
    },
    'nested_hashes_noU': {
        'result': "+ {'four'}\n+   4\n- {'three'}\n-   3\n  {'two'}\n    {'nine'}\n-     9\n+     8\n",
    },
    'nested_hashes_with_one_different_value': {
        'result': "  {'one'}\n    {'two'}\n      {'three'}\n-       3\n+       4\n",
    },
    'nested_hashes_with_one_equal_value': {
        'result': "  {'one': {'two': {'three': 3}}}\n",
    },
    'nested_hashes_with_one_equal_value_noU': {
        'result': '',
    },
    'nested_lists': {
        'result': "  [0]\n    0\n  [1]\n    [[100]]\n  [2]\n    [0]\n      20\n    [1]\n-     '30'\n+     '31'\n  [3]\n-   4\n+   5\n",
    },
    'nested_lists_noU': {
        'result': "  [2]\n    [1]\n-     '30'\n+     '31'\n  [3]\n-   4\n+   5\n",
    },
    'nested_lists_with_one_different_item': {
        'result': '  [0]\n    [0]\n-     0\n+     1\n',
    },
    'nested_lists_with_one_equal_item': {
        'result': '  [[0]]\n',
    },
    'nested_lists_with_one_equal_item_noU': {
        'result': '',
    },
    'nested_mixed_structures': {
        'result': "  {'one'}\n    [0]\n      {'two'}\n        {'three'}\n          [0]\n            7\n          [1]\n-           4\n+           3\n    [1]\n      8\n",
    },
    'nested_mixed_structures_noOU': {
        'result': "  {'one'}\n    [0]\n      {'two'}\n        {'three'}\n          [1]\n+           3\n",
    },
    'one_item_changed_in_the_middle_of_list': {
        'result': '  [0]\n    0\n  [1]\n-   1\n+   9\n  [2]\n    2\n',
    },
    'one_item_changed_in_the_middle_of_list_noN': {
        'result': '  [0]\n    0\n  [1]\n-   1\n  [2]\n    2\n',
    },
    'one_item_changed_in_the_middle_of_list_noNO': {
        'result': '  [0]\n    0\n  [2]\n    2\n',
    },
    'one_item_changed_in_the_middle_of_list_noO': {
        'result': '  [0]\n    0\n  [1]\n+   9\n  [2]\n    2\n',
    },
    'one_item_changed_in_the_middle_of_list_noU': {
        'result': '  [1]\n-   1\n+   9\n',
    },
    'one_item_inserted_in_the_middle_of_list': {
        'result': '  [0]\n    0\n+ [1]\n+   1\n  [2]\n    2\n',
    },
    'one_item_inserted_in_the_middle_of_list_noA': {
        'result': '  [0]\n    0\n  [1]\n    2\n',
    },
    'one_item_inserted_in_the_middle_of_list_noU': {
        'result': '+ [1]\n+   1\n',
    },
    'one_item_popped_from_list': {
        'result': '  [0]\n    0\n- [1]\n-   1\n',
    },
    'one_item_popped_from_list_noU': {
        'result': '- [1]\n-   1\n',
    },
    'one_item_pushed_to_list': {
        'result': '  [0]\n    0\n+ [1]\n+   1\n',
    },
    'one_item_pushed_to_list_noU': {
        'result': '+ [1]\n+   1\n',
    },
    'one_item_removed_from_the_middle_of_list': {
        'result': '  [0]\n    0\n- [1]\n-   1\n  [2]\n    2\n',
    },
    'one_item_removed_from_the_middle_of_list_noR': {
        'result': '  [0]\n    0\n  [2]\n    2\n',
    },
    'one_item_removed_from_the_middle_of_list_noU': {
        'result': '- [1]\n-   1\n',
    },
    'one_item_shifted_from_list': {
        'result': '- [0]\n-   0\n  [1]\n    1\n',
    },
    'one_item_shifted_from_list_noU': {
        'result': '- [0]\n-   0\n',
    },
    'one_item_unshifted_to_list': {
        'result': '+ [0]\n+   0\n  [1]\n    1\n',
    },
    'one_item_unshifted_to_list_noU': {
        'result': '+ [0]\n+   0\n',
    },
    'one_key_added_to_subhash': {
        'result': "  {'one'}\n+   {'three'}\n+     3\n    {'two'}\n      2\n",
    },
    'one_key_added_to_subhash_noU': {
        'result': "  {'one'}\n+   {'three'}\n+     3\n",
    },
    'one_key_removed_from_subhash': {
        'result': "  {'one'}\n-   {'three'}\n-     3\n    {'two'}\n      2\n",
    },
    'one_key_removed_from_subhash_noU': {
        'result': "  {'one'}\n-   {'three'}\n-     3\n",
    },
    'quote_symbols': {
        'result': '  {\'"double"\'}\n-   \'""\'\n+   \'"\'\n  {"\'single\'"}\n-   "\'\'"\n+   "\'"\n  {\'`backticks`\'}\n-   \'``\'\n+   \'`\'\n',
    },
    'ranges_different': {
        'result': '- range(0, 4)\n+ range(0, 5)\n',
    },
    'ranges_equal': {
        'result': '  range(0, 4)\n',
    },
    'redefined_depth': {
        'result': '-       0\n+       1\n',
    },
    'set_extended': {
        'result': '# <set>\n  1\n+ 2\n',
    },
    'sets_empty_diff': {
        'result': '',
    },
    'sets_lcs': {
        'result': '# <set>\n- 1\n  2\n+ 3\n',
    },
    'sets_lcs_noAR': {
        'result': '# <set>\n  2\n',
    },
    'sets_lcs_noU': {
        'result': '# <set>\n- 1\n+ 3\n',
    },
    'sets_lcs_trimR': {
        'result': '# <set>\n- 1\n  2\n+ 3\n',
    },
    'simple_strings_in_text_mode': {
        'result': "- 'bar'\n+ 'baz'\n",
    },
    'str_vs_bytes': {
        'result': "- 'a'\n+ b'a'\n",
    },
    'subhash_emptied': {
        'result': "  {'one'}\n-   {'two'}\n-     2\n",
    },
    'subhash_emptied_noR': {
        'result': '',
    },
    'subhash_filled': {
        'result': "  {'one'}\n+   {'two'}\n+     2\n",
    },
    'subhash_filled_noA': {
        'result': '',
    },
    'sublist_emptied': {
        'result': '  [0]\n-   [0]\n-     0\n',
    },
    'sublist_emptied_noR': {
        'result': '',
    },
    'sublist_filled': {
        'result': '  [0]\n+   [0]\n+     0\n',
    },
    'sublist_filled_noA': {
        'result': '',
    },
    'text_equal': {
        'result': "  'A\\nB\\nC'\n",
    },
    'text_equal_noU': {
        'result': '',
    },
    'text_lcs': {
        'result': '# <str>\n  @@ -1,3 +1,2 @@\n  A\n- B\n  C\n',
    },
    'text_line_added': {
        'result': '# <str>\n  @@ -1,2 +1,3 @@\n+ A\n  B\n  C\n',
    },
    'text_line_changed': {
        'result': '# <str>\n  @@ -1,3 +1,3 @@\n  A\n- B\n+ b\n  C\n',
    },
    'text_line_changed_ctx_0': {
        'result': '# <str>\n  @@ -2 +2 @@\n- B\n+ b\n',
    },
    'text_line_removed': {
        'result': '# <str>\n  @@ -1,3 +1,2 @@\n  A\n- B\n  C\n',
    },
    'text_multiple_hunks': {
        'result': '# <str>\n  @@ -1 +1 @@\n+ A\n  @@ -3 +4 @@\n- C\n',
    },
    'text_trailing_newlines': {
        'result': '# <str>\n  @@ -1,3 +1,3 @@\n  A\n- B\n+ b\n  \n',
    },
    'text_vs_empty_string': {
        'result': '# <str>\n  @@ -1,2 +1 @@\n- A\n- B\n+ \n',
    },
    'tuple_extended': {
        'result': '  (0)\n    1\n+ (1)\n+   2\n',
    },
    'tuples_lcs': {
        'result': '+ (0)\n+   0\n  (1)\n    1\n  (2)\n    2\n  (3)\n-   4\n+   3\n- (4)\n-   5\n',
    },
    'tuples_lcs_noOU': {
        'result': '+ (0)\n+   0\n  (2)\n+   3\n- (3)\n-   5\n',
    },
    'type_hints_disabled': {
        'result': '  @@ -1,2 +1,2 @@\n- two\n+ 2\n  lines\n',
    },
    'undef_vs_0': {
        'result': '- None\n+ 0\n',
    },
    'undef_vs_empty_hash': {
        'result': '- None\n+ {}\n',
    },
    'undef_vs_empty_hash_noNO': {
        'result': '',
    },
    'undef_vs_empty_list': {
        'result': '- None\n+ []\n',
    },
    'undef_vs_empty_string': {
        'result': "- None\n+ ''\n",
    },
    'undef_vs_negative_number': {
        'result': '- None\n+ -1\n',
    },
    'undef_vs_undef': {
        'result': '  None\n',
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
            print(f'========== {name} ==========')
        print(RESULTS[name].get('result'), end='')
