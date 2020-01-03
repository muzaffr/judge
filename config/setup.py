from os.path import join, splitext, pardir, abspath
from os import makedirs
from hashlib import sha256
from subprocess import run
import pickle
import json
import sys
sys.path.append("..")
from judge import Test

with open("config.json") as the_file:
    config = json.load(the_file)

base = join(abspath(pardir), "data")
makedirs(join(base, "hashes"), exist_ok=True)
makedirs(join(base, "tests"), exist_ok=True)

for action, password in config["passwords"].items():
    with open(join(pardir, "data", "hashes", action), 'w') as the_file:
        the_file.write(sha256(password.encode("utf-8")).hexdigest())

del config["passwords"]

tests = []
tests_dir = abspath(join(pardir, "data", "tests"))

for index, test in enumerate(config["tests"]):

    name, score = test
    stem, ext = splitext(name)

    if ext == ".txt":
        with open(join("tests", name), 'rb') as the_file:
            content = the_file.read().replace(b"\r\n", b"\n")
        with open(join(tests_dir, name), 'wb') as the_file:
            the_file.write(content)
        is_gen = False

    elif ext == ".cpp":
        run(["g++", join("tests", name), "-o", join(tests_dir, stem+".out"), "-std=c++17"])
        name = stem + ".out"
        is_gen = True

    else:
        raise RuntimeError

    tests.append(Test(index+1, join("data", "tests", name), score, is_gen))

config["tests"] = tests

run(["g++", config.pop("checker_source"), "-o", join(pardir, "data", "checker"), "-std=c++17"])

with open(join(pardir, "data", "metadata.pkl"), 'wb') as the_file:
    pickle.dump(config, the_file, -1)
