#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:26:49 2019

@author: kuangchen
"""

import os
from multiprocessing import Pool
from itertools import islice

def new_file(path):
    print('Create empty file {}'.format(path))
    open(path,'w').close()

def save_data_list(data_list, data_path, mode='w', sep=u' '):
    with open(data_path, mode) as f:
        for line in data_list:
            content = sep.join([u'{}'.format(data) for data in line]).encode('utf8') + '\n'
            f.write(content)
        print("{} line size:{} to {}".format('Add' if mode == 'a' else 'Save', 
                                             len(data_list), data_path))

def read_data_list(data_path, sample_num=-1, sep=None, function=None, workers=1):
    print('Parse data from %s' % data_path)
    data_list = []
    count = 0
    with open(data_path, 'r') as f:
        for line in f:
            line = line.decode('utf8').strip()
            data_list.append(line)
            count += 1
            if sample_num > 0 and count >= sample_num:
                break
    if sep is not None:
        data_list = [data.split(sep) for data in data_list]
    if function is not None:
        if workers == 1:
            data_list = map(function, data_list)
        else:
            pool = Pool(workers)
            data_list = pool.map(function, data_list)
            pool.close()
            pool.join()
    print('Read {} lines'.format(count))
    return data_list

def remove_files_in_path(path_or_files):
    if isinstance(path_or_files, str):
        files = os.listdir(path_or_files)
        print('Remove {} files in '.format(len(files)) + path_or_files)
    if isinstance(path_or_files, list):
        files = path_or_files
        print('Remove file: ', path_or_files)
    for file_name in files:
        file_path = os.path.join(path_or_files, file_name)
        if not os.path.isdir(file_path):
            os.remove(file_path)

def next_n_lines(file_opened, N, sep=None):
    if sep is not None:
        return [line.decode('utf8').strip().split(sep) for line in islice(file_opened, N)]
    else:
        return [line.decode('utf8').strip() for line in islice(file_opened, N)]

if __name__ == '__main__':
    pass