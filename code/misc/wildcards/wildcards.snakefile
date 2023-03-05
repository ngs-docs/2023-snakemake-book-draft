# ANCHOR: all-files
files, = glob_wildcards('letters-only-{word}.txt')
# ANCHOR_END: all-files
print(files)
assert files == ['abc2', 'abc-xyz', 'abc']

# ANCHOR: letters-only
letters_only, = glob_wildcards('letters-only-{name,[a-zA-Z]+}.txt')
# ANCHOR_END: letters-only
print(letters_only)

assert 'abc' in letters_only
assert not 'abc2' in letters_only, letters_only

# ANCHOR: letters-only-2
letters_only, = glob_wildcards('letters-only-{name,[^0-9]+}.txt')
# ANCHOR_END: letters-only-2
print(letters_only)

assert 'abc' in letters_only
assert 'abc-xyz' in letters_only
assert not 'abc2' in letters_only

# ANCHOR: all-txt
all_txt_files, = glob_wildcards('{filename}.txt')
# ANCHOR_END: all-txt

assert 'data/datafile' in all_txt_files

# ANCHOR: no-subdir
this_dir_only, = glob_wildcards('{filename,[^/]+}.txt')
# ANCHOR_END: no-subdir

assert 'data/datafile' not in this_dir_only
