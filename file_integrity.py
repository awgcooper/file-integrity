#!/usr/bin/python3
# https://codereview.stackexchange.com/questions/147056/short-script-to-hash-files-in-a-directory

import os.path
import xxhash
import datetime
import pickle


def list_files_recursive(path):
    files = []
    # r = root, d = directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    lst = [file for file in files]
    return lst


def get_hashes():
    root_path = ('D:\\misc')
    file_list = list_files_recursive(root_path)
    filelist_dict = dict.fromkeys(file_list)
    for key_filename in filelist_dict:
        hash_fn = xxhash.xxh128()
        with open(key_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_fn.update(chunk)
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(key_filename))
        filelist_dict.update({key_filename:[ hash_fn.hexdigest(), mod_time ]})
    return filelist_dict


datefmt = lambda x: x.strftime("%Y-%m-%d")
today = datefmt(datetime.date.today())
yesterday = datefmt(datetime.date.today() - datetime.timedelta(days=1))
file_parts = [ 'D:\\misc\\hashes_', today, yesterday, '.pkl' ]
file_today = file_parts[0] + file_parts[1] + file_parts[3]
file_yesterday = file_parts[0] + file_parts[2] + file_parts[3]
dict_filelist_today = get_hashes()
with open(file_today, 'wb') as fp:
    pickle.dump(dict_filelist_today, fp, protocol=pickle.HIGHEST_PROTOCOL)

#print(get_hashes())

# load pickle file from yesterday back into dictionary
with open(file_yesterday, 'rb') as f:
    dict_filelist_yesterday = pickle.load(f)

#print(dict_filelist_yesterday)

# access hashes
for k, v in dict_filelist_today.items():
    print(v[0])

# access mod_time
for k, v in dict_filelist_today.items():
    print(v[1])
