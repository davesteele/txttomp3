#!/usr/bin/python3

import hashlib
import os

basedir = "."

def set_base_dir(dir):
    global basedir
    basedir = dir


def get_hash(*args):

    key = "|".join([x.__repr__() for x in args]).encode()
    return hashlib.sha1(key).hexdigest()


def get_hash_path(*args):
    hash = get_hash(*args)

    hash_path = os.path.join(basedir, hash[0:2], hash[2:4], hash[4:])
    return hash_path


def set_cache(data, *keys):
    path = get_hash_path(*keys)
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(path, "wb") as fp:
        fp.write(data)


def get_cache(*keys):
    path = get_hash_path(*keys)

    if not os.path.exists(path):
        return None

    return open(path, "rb").read()


def cache(f):
    def wrapper(*args, **kwargs):
        cache_data = get_cache(*args)
        if cache_data is not None:
            return cache_data

        cache_data = f(*args, **kwargs)
        if cache_data is not None:
            set_cache(cache_data, *args)

        return cache_data

    return wrapper
