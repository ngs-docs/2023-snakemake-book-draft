# ANCHOR: letters-only
letters_only, = glob_wildcards('letters-only-{name,[a-zA-Z]+}.txt')
# ANCHOR_END: letters-only

assert 'abc' in letters_only
assert not 'abc2' in letters_only, letters_only

# ANCHOR: all-txt
all_txt_files, = glob_wildcards('{filename}.txt')
# ANCHOR_END: all-txt

assert 'data/datafile' in this_dir_only

# ANCHOR: no-subdir
this_dir_only, = glob_wildcards('{filename,[^/]+}.txt')
# ANCHOR_END: no-subdir

assert 'data/datafile' not in this_dir_only
