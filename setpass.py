#!/usr/bin/python3

from sys import argv
from hashlib import sha256
from os.path import join

with open(join("data", "hashes", argv[1]), 'w') as the_file:
    the_file.write(sha256(argv[2].encode("utf-8")).hexdigest())
