#!/usr/bin/python3
# https://codereview.stackexchange.com/questions/147056/short-script-to-hash-files-in-a-directory

import datetime
from pathlib import Path
import xxhash
import os.path
import dill


# date formatting
datefmt = lambda x: x.strftime("%Y-%m-%d")
today = datefmt(datetime.date.today())
yesterday = datefmt(datetime.date.today() - datetime.timedelta(days=1))


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
    file_today = 'D:/misc/hashes_' + today + '.pickle'
    with open(file_today, 'wb') as f:
        dill.dump(dict_filelist_today, f)


# load file from yesterday back into dictionary
def dict_yesterday():
    file_yesterday = 'D:/misc/hashes_' + yesterday + '.pickle'
    with open(file_yesterday, 'rb') as f:
        dict_filelist_yesterday = dill.load(f)
    return dict_filelist_yesterday


# compare two dictionaries looking for corrupt files
# defined as same name, same mtime, different hash
# results printed to text file
def corrupt_files():
    newlist = [ ]
    for d1key, d1val in dict1.items():
        d2val = (dict2.get(d1key))
        if d2val == None:
            pass
        elif d1val[0] != d2val[0] and d1val[1] == d2val[1]:
            newlist.append([str(d1key), ['today', [str(d1val[0]),
            str(d1val[1])]], ['yesterday', [str(d2val[0]), str(d2val[1])]]])
    heading = 'CORRUPT FILES:'
    with open('1.txt', 'w') as f:
        f.write(heading)
        f.write('\n')
    with open('1.txt', 'a') as f:
        if not newlist:
            a = '{{ NONE }}'
            f.write(a)
            f.write('\n')
        else:
            for entry in newlist:
                f.write(str(entry))
                f.write('\n')


# dictionaries for today and yesterday converted to sets
# sets can be subtracted from one another to find differences
# today - yesterday = new files; yesterday - today = deleted files
# results printed to text file
def files_add_del(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    heading = 'NEW FILES:'
    with open('1.txt', 'a') as f:
        f.write('\n\n')
        f.write(heading)
        f.write('\n')
    with open('1.txt', 'a') as f:
        for j in sorted(added):
            a = '{0}\n'.format(str(j).replace(str(j.anchor), ''))
            f.write(a)
    heading = 'DELETED FILES:'
    with open('1.txt', 'a') as f:
        f.write('\n\n')
        f.write(heading)
        f.write('\n')
    with open('1.txt', 'a') as f:
        for j in sorted(removed):
            a = '{0}\n'.format(str(j).replace(str(j.anchor), ''))
            f.write(a)


save_today()                # save today's file list to pickle file
dict1 = dict_today()        # load today's list from pickle file to dict
dict2 = dict_yesterday()    # load yesterday's list from pickle file to dict
corrupt_files()             # check for corrupt files
files_add_del(dict1, dict2) # check for new and deleted files
