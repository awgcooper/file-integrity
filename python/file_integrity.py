#!/usr/bin/python3
# https://codereview.stackexchange.com/questions/147056/short-script-to-hash-files-in-a-directory

import datetime
from pathlib import Path
import xxhash
import os.path
import dill


# create dictionary with list values { filename: [xxhash, modification time] }
def dict_today():
    root_path = ('D:/files')
    p = Path(root_path).glob('**/*')
    file_list = [x for x in p if x.is_file()]
    filelist_dict = dict.fromkeys(file_list)
    for key_filename in filelist_dict:
        hash_fn = xxhash.xxh128()
        with open(key_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_fn.update(chunk)
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(key_filename))
        filelist_dict.update({key_filename:[ hash_fn.hexdigest(), mod_time ]})
    return filelist_dict


# save today's dictionary to file
def save_today():
    dict_filelist_today = dict_today()
    file_today = filebase + today + '.pickle'
    with open(file_today, 'wb') as f:
        dill.dump(dict_filelist_today, f)


# load file from yesterday back into dictionary
def dict_yesterday():
    file_yesterday = filebase + yesterday + '.pickle'
    with open(file_yesterday, 'rb') as f:
        dict_filelist_yesterday = dill.load(f)
    return dict_filelist_yesterday


# compare two dictionaries looking for corrupt files
# defined as same name, same mtime, different hash
# results printed to text file
def corrupt_files(dict1, dict2):
    corrupt = [ ]
    for d1key, d1val in dict1.items():
        d2val = (dict2.get(d1key))
        if d2val == None:
            pass
        elif d1val[0] != d2val[0] and d1val[1] == d2val[1]:
            corrupt.append([str(d1key), ['today', [str(d1val[0]),
            str(d1val[1])]], ['yesterday', [str(d2val[0]), str(d2val[1])]]])
    return corrupt


# dictionaries for today and yesterday converted to sets
# sets can be subtracted from one another to find differences
# today - yesterday = new files; yesterday - today = deleted files
# results printed to text file
def files_add_del(dict1, dict2):
    dict1_keys = set(dict1.keys())
    dict2_keys = set(dict2.keys())
    new = dict1_keys - dict2_keys
    deleted = dict2_keys - dict1_keys
    return new, deleted


def write_to_file(report, heading, file_delta):
    if heading == '-- CORRUPT FILES --':
        with open(report, 'w') as f:
            f.write(heading + '\n')
        with open(report, 'a') as f:
            if not file_delta:
                a = '{{ NONE }}'
                f.write(a + '\n')
            else:
                for entry in file_delta:
                    f.write(str(entry) + '\n')
    else:
        with open(report, 'a') as f:
            f.write('\n\n' + heading + '\n')
        with open(report, 'a') as f:
            for j in sorted(file_delta):
                a = '{0}\n'.format(str(j).replace(str(j.anchor), ''))
                f.write(a)


# date formatting
datefmt = lambda x: x.strftime("%Y-%m-%d")
today = datefmt(datetime.date.today())
yesterday = datefmt(datetime.date.today() - datetime.timedelta(days=1))
filebase = 'D:/misc/pickle/hashes_'
report = 'D:/misc/pickle/report_' + today + '.txt'


# run functions
save_today()                                      # save today's file list
dict1 = dict_today()                              # load today's  to dict
dict2 = dict_yesterday()                          # load yesterday's list to dict
corrupt = corrupt_files(dict1, dict2)             # create list of corrupt files
new = (files_add_del(dict1, dict2)[0])            # create set of new files
deleted = (files_add_del(dict1, dict2)[1])        # create set of deleted files
write_to_file(report, '-- CORRUPT FILES --', corrupt)
write_to_file(report, '-- NEW FILES --', new)
write_to_file(report, '-- DELETED FILES --', deleted)
