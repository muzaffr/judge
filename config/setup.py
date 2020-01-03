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

target = join(abspath(pardir), "data")
makedirs(join(target, "hashes"), exist_ok=True)
makedirs(join(target, "tests"), exist_ok=True)

for action, password in config["passwords"].items():
    with open(join(target, "hashes", action), 'w') as the_file:
        the_file.write(sha256(password.encode("utf-8")).hexdigest())

del config["passwords"]

tests = []

for index, test in enumerate(config["tests"]):

    name, score = test
    stem, ext = splitext(name)

    if ext == ".txt":
        with open(join("tests", name), 'rb') as the_file:
            content = the_file.read().replace(b"\r\n", b"\n")
        with open(join(target, "tests", name), 'wb') as the_file:
            the_file.write(content)
        is_gen = False

    elif ext == ".cpp":
        run(["g++", join("tests", name), "-o", join(target, "tests", stem+".out"), "-std=c++17"])
        name = stem + ".out"
        is_gen = True

    else:
        raise RuntimeError

    tests.append(Test(index+1, join("data", "tests", name), score, is_gen))

config["tests"] = tests

run(["g++", config.pop("checker_source"), "-o", join(target, "checker"), "-std=c++17"])

with open(join(target, "metadata.pkl"), 'wb') as the_file:
    pickle.dump(config, the_file, -1)
