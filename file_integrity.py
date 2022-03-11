#!/usr/bin/python3
# https://codereview.stackexchange.com/questions/147056/short-script-to-hash-files-in-a-directory

import os
import os.path
import xxhash
import csv
import shutil
from datetime import datetime

# recursive file listing
#rootPath = ('D:/misc')
#p = Path(rootPath).glob('**/*')
#fileList = [x for x in p if x.is_file()]


def list_files_recursive(path):
    files = []
    # r = root, d = directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    lst = [file for file in files]
    return lst


top_directory = "D:\\misc"
def get_hashes():
    fileList = list_files_recursive(top_directory)
    list_of_hashes = []
    for each_file in fileList:
        hash_fn = xxhash.xxh128()
        modTime = os.path.getmtime(each_file)
        with open(each_file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_fn.update(chunk)

        #list_of_hashes.append([each_file, hash_fn.hexdigest(), modTime])
        list_of_hashes.append('{};{};{}\n'.format(each_file, hash_fn.hexdigest(), round(modTime)))
    return list_of_hashes

def write_hashes():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    global hashes_csv_file
    hashes_csv_file = ('D:\\misc\\hashes_' + date_time + '.csv')
    hashes = get_hashes()
    with open(hashes_csv_file, 'w') as f:
        for final_values in hashes:
            #jsonString = json.dumps(hash_fn)
            #f.write(jsonString)
            f.write(final_values)
            #writer = csv.writer(f, delimiter = ";")
            #writer = csv.writer(f)
            #writer.writerow(final_values)

write_hashes()
